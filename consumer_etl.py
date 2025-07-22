import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime
import os
from dotenv import load_dotenv

# Memuat isi dari file .env
load_dotenv()


# Konfigurasi untuk koneksi ke Kafka dan PostgreSQL
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP")

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_db_connection():
    """
    Fungsi untuk membuat koneksi ke database PostgreSQL
    Mengembalikan objek koneksi jika berhasil
    Akan menampilkan error dan raise exception jika gagal
    """
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        print("PostgreSQL connection successful.")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

def enrich_and_store(conn, sensor_data):
    """
    Fungsi untuk meng-enrich data sensor dengan metadata dari database
    dan menyimpan data yang sudah di-enrich ke tabel readings
    
    Parameters:
        conn: Koneksi database PostgreSQL
        sensor_data: Data sensor dari Kafka yang akan diproses
    
    Proses:
        1. Mengambil metadata device berdasarkan device_id
        2. Jika metadata tidak ditemukan, menggunakan nilai default
        3. Menyimpan data yang sudah di-enrich ke tabel farhan_iot_sensor_readings
    """    
    try:
        with conn.cursor() as cur:
            device_id = sensor_data['device_id']

            # Query enrichment data
            cur.execute(
                "SELECT device_name, location, manufacturer FROM farhan_device_metadata WHERE device_id = %s", 
                (device_id,)
            )
            result = cur.fetchone()

            if result:
                device_name, location, manufacturer = result
            else:
                device_name = "Unknown Device"
                location = "Unknown Location"
                manufacturer = "Unknown Manufacturer"

            # Insert into enriched readings table
            insert_query = """ 
                INSERT INTO farhan_iot_sensor_readings 
                (device_id, device_name, location, temperature, humidity, timestamp, manufacturer) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            record_to_insert = (
                device_id,
                device_name,
                location,
                sensor_data["temperature"],
                sensor_data["humidity"],
                sensor_data["timestamp"],
                manufacturer
            )
            
            cur.execute(insert_query, record_to_insert)
            conn.commit()
            print(f"Data stored for {device_id}")
            
    except Exception as e:
        print(f"Error in enrich_and_store: {e}")
        conn.rollback()
        raise

def main():
    """
    Fungsi utama yang menjalankan consumer Kafka dan memproses pesan
    Alur kerja:
        1. Membuat Kafka consumer
        2. Membuat koneksi ke database
        3. Mendengarkan pesan dari Kafka
        4. Untuk setiap pesan, memanggil fungsi enrich_and_store
        5. Menutup koneksi dan consumer ketika selesai
    """    
    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_CONSUMER_GROUP,
        auto_offset_reset="earliest",
        # auto_offset_reset="latest"
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    try:
        conn = get_db_connection()
        print("Consumer started. Listening for messages...")
        
        for message in consumer:
            try:
                sensor_data = message.value
                enrich_and_store(conn, sensor_data)
            except Exception as e:
                print(f"Error processing message: {e}")
                continue
                
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
        consumer.close()
        print("Resources closed.")

if __name__ == "__main__":
    main()