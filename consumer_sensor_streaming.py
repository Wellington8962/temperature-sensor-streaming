from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType
from pyspark.sql.functions import from_json, col

def write_to_cassandra(batch_df, batch_id):
    batch_df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="sensores", keyspace="sensores_de_temperatura") \
        .save()

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("KafkaToCassandra") \
        .master("local[*]") \
        .config("spark.cassandra.connection.host", "localhost") \
        .config("spark.cassandra.connection.port", "9042") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "dados_sensores"

    sensor_schema = StructType() \
        .add("sensor_id", StringType()) \
        .add("date", StringType()) \
        .add("time", StringType()) \
        .add("battery_level", StringType()) \
        .add("humidity", StringType()) \
        .add("status", StringType()) \
        .add("temperature", StringType())

    sensor_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "latest") \
        .load()

    sensor_data_df = sensor_df.selectExpr("CAST(value AS STRING) as json") \
        .select(from_json(col("json"), sensor_schema).alias("data")) \
        .select("data.*")

    query = sensor_data_df.writeStream \
        .foreachBatch(write_to_cassandra) \
        .outputMode("update") \
        .start()

    query.awaitTermination()
