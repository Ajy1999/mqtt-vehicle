# 🚗 MQTT Vehicle Telemetry with TimescaleDB

This project simulates vehicle telemetry data publishing and subscribing using MQTT. The telemetry data is stored in a TimescaleDB (PostgreSQL extension) running in Docker. The **publisher** simulates vehicle data and sends it via MQTT, while the **subscriber** receives this data and inserts it into the TimescaleDB database.

---

## 📁 Project Structure

- `vehicle_publisher.py` — Simulates vehicle data and publishes it to an MQTT topic.
- `mqtt_subscriber.py` — Subscribes to the MQTT topic and stores received data in TimescaleDB.
- `Dockerfile` — Builds the Docker image for publisher/subscriber.
- `docker-compose.yml` — Defines services for TimescaleDB, publisher, and subscriber.
- `requirements.txt` — Lists required Python packages.

---

## ✅ Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.13+ (optional, for local testing)
- MQTT broker: Public broker used (`mqtt.eclipseprojects.io`)

---

## 🚀 Setup & Run

1. **Clone the repo:**

    ```bash
    git clone https://github.com/Ajy1999/mqtt-vehicle.git
    cd mqtt-vehicle
    ```

2. **Build and start the containers:**

    ```bash
    docker-compose up --build
    ```

3. **Access TimescaleDB**

   - TimescaleDB will be available on `localhost:5432`.
   - Connect using tools like [DBeaver](https://dbeaver.io/) or `psql`.

4. **Verify Execution**

   - The **publisher** prints simulated vehicle JSON messages to the console.
   - The **subscriber** logs received messages and confirms inserts.
   - The `vehicle_telemetry` table in the `vehicle_data` database stores all records.

---

## 🛠️ Database Schema

```sql
CREATE TABLE vehicle_telemetry (
    time TIMESTAMPTZ NOT NULL,
    vehicle_id TEXT NOT NULL,
    speed FLOAT,
    engine_temp FLOAT,
    latitude FLOAT,
    longitude FLOAT
);

SELECT create_hypertable('vehicle_telemetry', 'time');
```
## 📊 Example Output

### Publisher Output:

```css
🚗 Vehicle simulator started...
Published: {"vehicle_id": "VH123", "speed": 65.23, "engine_temp": 85.1, ...}
Published: {"vehicle_id": "VH123", "speed": 62.45, "engine_temp": 88.7, ...}

```

### Subscriber Output:
```css
📡 Connected to broker.
Received: {
  "vehicle_id": "VH123",
  "speed": 65.23,
  "engine_temp": 85.1,
  ...
}
✅ Inserted data for vehicle: VH123 at 2025-06-10 14:25:33.132Z

```
## 🧭 Viewing Data with DBeaver
1. Open **DBeaver** and create a new PostgreSQL connection.
2. Use the following credentials: 
| Field    | Value              |
| -------- | ------------------ |
| Host     | `localhost`        |
| Port     | `5432`             |
| Database | `vehicle_data`     |
| User     | `postgres`         |
| Password | `mysecretpassword` |

3. Navigate to the vehicle_telemetry table and run:
```sql
SELECT * FROM vehicle_telemetry LIMIT 10;

```
You should now see real-time telemetry data being populated every few seconds.

## 📝 Notes
- The simulation uses a public MQTT broker, so message delivery is not guaranteed.
- This project is ideal for testing and learning, not for production use.
- You can easily extend this to support multiple vehicles or more telemetry fields.

## 📦 License
MIT – feel free to use, fork, and modify.