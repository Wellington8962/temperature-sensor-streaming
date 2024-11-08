import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

def generate_sensor_data():
    sensor_id = f"sensor_{random.randint(1, 10)}"
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    temperature = round(random.uniform(15.0, 30.0), 2)
    status = random.choice(["OK", "WARNING", "FAULT"])
    humidity = f"{random.randint(30, 70)}%"
    battery_level = f"{random.randint(50, 100)}%"

    data = {
        "sensor_id": sensor_id,
        "date": date_str,
        "time": time_str,
        "temperature": str(temperature),
        "status": status,
        "humidity": humidity,
        "battery_level": battery_level
    }
    return data

if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    try:
        while True:
            data = generate_sensor_data()
            producer.send('dados_sensores', value=data)
            print(f"Sent data: {data}")
            time.sleep(3)  # Envia dados a cada 3 segundos
    except KeyboardInterrupt:
        print("Producer stopped.")
    finally:
        producer.close()
