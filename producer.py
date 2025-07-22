from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime
import os
from dotenv import load_dotenv

# Memuat isi dari file .env
load_dotenv()

# --- Configuration ---
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC_NAME = os.getenv("KAFKA_TOPIC_NAME")  # auto created by Kafka if it doesn't exist
# http://5.189.154.248:8080 -> kafka ui
# --- Producer Initialization ---
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    # dict -> json string -> bytes
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Daftar Device ID
DEVICE_IDS = [f'device_{i}' for i in range(1, 6)]

def generate_sensor_data(device_id=None):
    """
    Fungsi untuk menghasilkan data sensor IoT secara acak.
    Jika device_id tidak diberikan, dipilih secara acak.
    """
    if device_id is None:
        device_id = random.choice(DEVICE_IDS)
    return {
        'device_id': device_id,
        'temperature': round(random.uniform(20.0, 35.0), 2),
        'humidity': round(random.uniform(30.0, 80.0), 2),
        'timestamp': datetime.utcnow().isoformat()
    }

def produce_loop(interval=1):
    """Fungsi utama untuk menjalankan Kafka Producer"""
    print("Kafka IoT Sensor Producer is running...")
    try:
        while True:
            data = generate_sensor_data()
            producer.send(TOPIC_NAME, value=data)
            print(f"[{datetime.now().isoformat()}] Sent: {data}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Producer stopped by user.")
    finally:
        producer.close()

if __name__ == '__main__':
    produce_loop()

