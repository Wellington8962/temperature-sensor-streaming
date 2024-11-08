# Kafka and Spark Streaming Challenge: Temperature Sensor Simulation with Cassandra Integration

This project aims to simulate a temperature sensor data pipeline, utilizing **Apache Kafka** to stream real-time data, **Apache Spark Streaming** to process the data, and **Apache Cassandra** to store the processed data. The entire pipeline is implemented in Python using **PySpark**.

## Challenge Description

### Steps of the Challenge

1. **Install Apache Kafka**: Set up the Kafka environment with Zookeeper and create a specific topic for the temperature sensor data.

2. **Create a Temperature Sensor Data Producer in Python**: Develop a producer that sends temperature sensor data messages to Kafka. Each message contains:
   - **Sensor ID**: A unique identifier for each sensor.
   - **Date**: The date of the reading in `YYYY-MM-DD` format.
   - **Time**: The time of the reading in `HH:MM:SS` format.
   - **Temperature**: The temperature reading.
   - **Status**: The status of the sensor (e.g., "OK", "FAULT", "WARNING").
   - **Humidity**: The humidity percentage.
   - **Battery Level**: The battery level percentage of the sensor.

   > **Note**: The `Faker` library or custom data generation logic can be used to simulate the sensor data.

3. **Set Up Apache Cassandra**: Install and configure Apache Cassandra. Create a keyspace and a table to store the sensor data with an appropriate schema design.

4. **Create a Spark Streaming Consumer in PySpark**: Develop a PySpark application that consumes the temperature sensor data from Kafka, processes it if necessary, and writes it to the Cassandra database.

   - **Transformation**: Data can be transformed or filtered as required before storing. For example, converting data types, filtering out faulty readings, or aggregating data.

---

## Project Structure

- `producer_sensor_data.py`: Python script that acts as a producer, sending simulated temperature sensor data to the Kafka topic.
- `consumer_sensor_streaming.py`: PySpark script that acts as a consumer, reads the sensor data from Kafka, processes it, and writes the data to Cassandra.
- `requirements.txt`: File containing the project dependencies for easy environment setup.
- `README.md`: Instructions and details about the project.

---

## Prerequisites

- Python 3.10
- Apache Kafka and Zookeeper installed and configured
- Apache Cassandra installed and configured
- Apache Spark with PySpark
- Virtual environment set up with the project dependencies

---

## Execution Instructions

### 1. Environment Setup

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```
3. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Start Apache Kafka and Zookeeper

> **Note**: Ensure that Apache Kafka is installed on your machine.

1. **Start Zookeeper**:
   ```bash
   $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties
   ```
2. **In another terminal, start the Kafka server**:
   ```bash
   $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties
   ```
3. **Create the `dados_sensores` topic**:
   ```bash
   $KAFKA_HOME/bin/kafka-topics.sh --create --topic dados_sensores --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

### 3. Set Up Apache Cassandra

1. **Start Cassandra**:
   ```bash
   cassandra -f
   ```
2. **Access the Cassandra Query Language Shell (cqlsh)**:
   ```bash
   cqlsh
   ```
3. **Create the keyspace and table**:
   ```sql
   CREATE KEYSPACE sensores_de_temperatura WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

   USE sensores_de_temperatura;

   CREATE TABLE sensores (
       sensor_id text,
       date text,
       time text,
       battery_level text,
       humidity text,
       status text,
       temperature text,
       PRIMARY KEY (sensor_id, date, time)
   ) WITH CLUSTERING ORDER BY (date ASC, time ASC);
   ```

### 4. Execute the Temperature Sensor Data Producer and the Spark Streaming Consumer

1. **Run the `producer_sensor_data.py` script to generate and send the simulated sensor data to Kafka**:
   ```bash
   python3 producer_sensor_data.py
   ```
2. **Run the PySpark consumer with the Cassandra and Kafka connectors to process the messages**:
   ```bash
   spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 consumer_sensor_streaming.py
   ```
   > **Note**: Ensure that the versions of the connectors match your Spark and Scala versions.

### 5. Verify Data in Cassandra

1. **Access `cqlsh`**:
   ```bash
   cqlsh
   ```
2. **Query the sensor data table**:
   ```sql
   USE sensores_de_temperatura;

   SELECT * FROM sensores;
   ```
   You should see the sensor data that was sent from Kafka and processed by Spark Streaming.

---

## Conclusion

This project demonstrates the integration of Apache Kafka, Apache Spark Streaming, and Apache Cassandra to process and store real-time temperature sensor data. This setup is useful for simulating IoT scenarios and can be expanded for real-world applications involving real-time data processing and analytics.

---

## Additional Notes

- **Stopping Services**: To stop any of the services (Zookeeper, Kafka, Cassandra, Producer, or Consumer), press `Ctrl + C` in the terminal where the service is running. This safely terminates the service if you need to stop it due to an error or for any other reason.
- **Monitoring**: Use the Spark UI (usually accessible at `http://localhost:4040`) to monitor the Spark Streaming application.
- **Error Handling**: Implement error handling and logging in your scripts to catch and troubleshoot any issues that may arise during execution.

---

## Project Dependencies

The `requirements.txt` file includes the following dependencies:

```
Package          Version
---------------- -----------
cassandra-driver 3.29.2
click            8.1.7
cqlsh            6.2.0
geomet           0.2.1.post1
kafka-python     2.0.2
pure-sasl        0.6.2
six              1.16.0
wcwidth          0.2.13
```

Ensure these are installed in your virtual environment.

---

## Repository

[Temperature Sensor Streaming Repository](https://github.com/Wellington8962/temperature-sensor-streaming)

---