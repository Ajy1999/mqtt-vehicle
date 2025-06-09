import time
import json
import random
from datetime import datetime
import paho.mqtt.client as mqtt

# MQTT Setup
BROKER = "mqtt.eclipseprojects.io"

TOPIC = "vehicular/data/VH123"

client = mqtt.Client(client_id="VehiclePublisher")
client.connect(BROKER)

# Simulated starting point (Berlin)
lat = 52.5200
lon = 13.4050

def simulate_vehicle_data():
    global lat, lon

    # Simulate gradual GPS movement
    lat += random.uniform(-0.0005, 0.0005)
    lon += random.uniform(-0.0005, 0.0005)

    return {
        "vehicle_id": "VH123",
        "speed": round(random.gauss(65, 10), 2),  # in km/h
        "engine_temp": round(random.uniform(70, 100), 2),  # add this field
        "engine_rpm": random.randint(1000, 4000),
        "fuel_level": round(random.uniform(10.0, 100.0), 1),
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "acceleration": round(random.uniform(-3.0, 3.0), 2),
        "brake_status": random.choice([True, False]),
        "gear_position": random.choice(["P", "R", "N", "D"]),
        "timestamp": time.time()
    }

try:
    print("🚗 Vehicle simulator started...")
    while True:
        data = simulate_vehicle_data()
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(2)  # send every 2 seconds
except KeyboardInterrupt:
    print("Simulation stopped.")
    client.disconnect()
