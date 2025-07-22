-- Buat tabel metadata perangkat
CREATE TABLE farhan_device_metadata (
    device_id VARCHAR(50) PRIMARY KEY,
    device_name VARCHAR(100),
    location VARCHAR(100),
    manufacturer VARCHAR(100)
);

-- Buat tabel untuk data sensor
CREATE TABLE farhan_iot_sensor_readings (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50),
    device_name VARCHAR(100),
    temperature FLOAT,
    humidity FLOAT,
    timestamp TIMESTAMP,
    location VARCHAR(100),
    manufacturer VARCHAR(100),
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy data for device metadata
INSERT INTO farhan_device_metadata (device_id, device_name, location, manufacturer) VALUES
('device_1', 'Temperature Sensor Room 1', 'Building A 1st Floor', 'Acme Corp'),
('device_2', 'Humidity Sensor Warehouse', 'North Warehouse', 'SensorTech'),
('device_3', 'Outdoor Environment Sensor', 'Front Garden', 'EnvSense'),
('device_4', 'Server Room Sensor', 'Server Room', 'DataCool'),
('device_5', 'Laboratory Sensor', 'Chemistry Lab', 'SciTech');