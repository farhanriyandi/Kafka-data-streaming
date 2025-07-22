# Kafka-data-streaming
## Requirements
* Python
* Postgresql

1. Buatlah tabel ```farhan_device_metadata``` dan tabel ```farhan_iot_sensor_readings``` di dalam database PostgreSQL dengan menjalankan perintah SQL yang terdapat pada file ddl.sql

2. Buat virtual Environment
  ```
    python3 -m venv .venv
    source .venv/bin/activate
  ```
3. Install dependencies:
   ```
     pip install -r requirements.txt
   ```  
4. Buat file .env masukan sesuai dengan KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_NAME, KAFKA_CONSUMER_GROUP, POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD yang dimiliki.
   ```
    KAFKA_BOOTSTRAP_SERVERS=YOUR_KAFKA_BOOTSTRAP_SERVERS
    KAFKA_TOPIC_NAME=YOUR_KAFKA_TOPIC_NAME
    KAFKA_CONSUMER_GROUP=YOUR_KAFKA_CONSUMER

    POSTGRES_HOST=YOUR_POSTGRES_HOST
    POSTGRES_DB=YOUR_POSTGRES_DB}
    POSTGRES_USER=YOUR_POSTGRES_USER}
    POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
   ```
5. run producer.py
   ```
     python3 producer.py
   ```
   Output:

   <img width="795" height="104" alt="image" src="https://github.com/user-attachments/assets/0f4cc72f-54f8-45c0-8f12-e05a7a972bf6" />

  
6. run consumer_etl.py
   ```
     python3 consumer_etl.py
   ```
   Output:

   <img width="139" height="119" alt="image" src="https://github.com/user-attachments/assets/f492aef7-e650-4eca-a6d1-fca5521a5c21" />

6. Lihat tabel farhan_iot_sensor_readings

   <img width="809" height="272" alt="image" src="https://github.com/user-attachments/assets/9233a9f2-0d2e-41eb-9aa8-571d429e1bcc" />


