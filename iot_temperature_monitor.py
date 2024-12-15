import time
import random
import threading
import json
import requests
import paho.mqtt.client as mqtt

# ==========================
# GLOBAL CONFIGURATION
# ==========================
THRESHOLD = 30  # Temperature alert threshold (in °C)
SEND_INTERVAL = 5  # Time interval to send data (seconds)
LOG_FILE = "temperature_log.txt"

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/sensor/temperature"

# REST API Endpoint
API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"  # Placeholder API

# ==========================
# TEMPERATURE SENSOR SIMULATION
# ==========================
def read_temperature():
    """
    Simulate reading data from a temperature sensor.
    Returns a random temperature value in Celsius.
    """
    return round(random.uniform(20, 40), 2)  # Simulated temperature range: 20°C to 40°C

# ==========================
# LOGGING MODULE
# ==========================
def log_data(temperature):
    """
    Log temperature data to a file with timestamps.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Temperature: {temperature}°C\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)
    print(f"✅ Data Logged: {log_entry.strip()}")

# ==========================
# ALERT MODULE
# ==========================
def check_alert(temperature):
    """
    Check if the temperature exceeds the threshold and trigger an alert.
    """
    if temperature > THRESHOLD:
        print(f"🚨 ALERT: High Temperature Detected! {temperature}°C exceeds {THRESHOLD}°C")

# ==========================
# HTTP COMMUNICATION MODULE
# ==========================
def send_data_to_server(temperature):
    """
    Send temperature data to a REST API server.
    """
    payload = {
        "sensor_id": "TEMP_SENSOR_01",
        "temperature": temperature,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers={"Content-Type": "application/json"})
        if response.status_code == 201 or response.status_code == 200:
            print(f"📡 Data Sent to Server: {payload}")
        else:
            print(f"❌ Server Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error Sending Data: {e}")

# ==========================
# MQTT MODULE
# ==========================
def mqtt_publish(client, temperature):
    """
    Publish temperature data to an MQTT broker.
    """
    message = json.dumps({
        "sensor_id": "TEMP_SENSOR_01",
        "temperature": temperature,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    })
    client.publish(MQTT_TOPIC, message)
    print(f"📤 MQTT Published: {message}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("🔗 Connected to MQTT Broker")
    else:
        print(f"❌ Failed to connect to MQTT Broker: {rc}")

# ==========================
# MAIN IOT FUNCTION
# ==========================
def main():
    # MQTT Client Setup
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_thread = threading.Thread(target=mqtt_client.loop_start)
        mqtt_thread.daemon = True
        mqtt_thread.start()
    except Exception as e:
        print(f"❌ Error Connecting to MQTT Broker: {e}")
    
    print("\n🔧 IoT Temperature Monitoring System Started")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            # Simulate Sensor Reading
            temperature = read_temperature()
            print(f"🌡️ Current Temperature: {temperature}°C")

            # Process Data
            log_data(temperature)
            check_alert(temperature)

            # Send Data to Server
            send_data_to_server(temperature)

            # Publish Data via MQTT
            mqtt_publish(mqtt_client, temperature)

            # Wait before next reading
            time.sleep(SEND_INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 IoT Temperature Monitoring System Stopped")
        mqtt_client.disconnect()

# ==========================
# RUN APPLICATION
# ==========================
if __name__ == "__main__":
    main()
