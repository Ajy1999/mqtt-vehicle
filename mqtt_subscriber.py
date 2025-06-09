import json
import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime


# MQTT Setup


conn = psycopg2.connect(
    dbname='vehicle_data',
    user='postgres',
    password='mysecretpassword',
    host='timescaledb',
    port=5432
)
cursor = conn.cursor()
BROKER = "mqtt.eclipseprojects.io"

TOPIC = "vehicular/data/VH123"

def on_connect(client, userdata, flags, rc, properties=None):
    print("📡 Connected to broker.")
    client.subscribe(TOPIC)

def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode('utf-8'))
        print(f"Received: {json.dumps(data, indent=2)}")
        # data
        vehicle_id = data["vehicle_id"]
        speed = data["speed"]
        engine_temp = data["engine_temp"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        timestamp = datetime.utcnow()
        cursor.execute("""
                    INSERT INTO vehicle_telemetry (time, vehicle_id, speed, engine_temp, latitude, longitude)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (timestamp, vehicle_id, speed, engine_temp, latitude, longitude))
        conn.commit()
        print(f"✅ Inserted data for vehicle: {vehicle_id} at {timestamp}")

    except Exception as e:
        print(f"❌ Error: {e}")

client = mqtt.Client(client_id="VehicleSubscriber")
client.connect(BROKER)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER)


try:
    print("🟢 Subscriber running... Press Ctrl+C to stop.")
    client.loop_forever()
except KeyboardInterrupt:
    print("🛑 Stopping subscriber...")
    client.disconnect()
    cursor.close()
    conn.close()