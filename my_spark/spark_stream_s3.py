from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

import os 
from dotenv import load_dotenv

def on_termination(query):
    print("Stream has finished!")

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# Define schema (1NF: Flattened)
schema = StructType([
    StructField("gender", StringType(), True),
    StructField("name", StructType([
        StructField("title", StringType(), True),
        StructField("first", StringType(), True),
        StructField("last", StringType(), True)
    ]), True),
    StructField("location", StructType([
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("country", StringType(), True)
    ]), True),
    StructField("email", StringType(), True),
    StructField("login", StructType([
        StructField("uuid", StringType(), True),  # User ID (Primary Key)
        StructField("username", StringType(), True),
        StructField("password", StringType(), True)
    ]), True),
    StructField("dob", StructType([
        StructField("date", StringType(), True),
        StructField("age", IntegerType(), True)
    ]), True),
    StructField("registered", StructType([
        StructField("date", StringType(), True),
        StructField("age", IntegerType(), True)
    ]), True),
    StructField("phone", StringType(), True),
    StructField("nat", StringType(), True)
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-broker:9092") \
    .option("subscribe", "user_data_topic") \
    .option("startingOffsets", "earliest") \
    .load()

print("Stream loaded successfully!")

# Convert JSON string to structured format
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select(
        col("data.login.uuid").alias("user_id"),  # Primary Key (First Column)
        col("data.gender"),
        col("data.name.title"),
        col("data.name.first").alias("first_name"),
        col("data.name.last").alias("last_name"),
        col("data.location.city"),
        col("data.location.state"),
        col("data.location.country"),
        col("data.email"),
        col("data.login.username"),
        col("data.login.password"),
        col("data.dob.date").alias("dob_date"),
        col("data.dob.age").alias("dob_age"),
        col("data.registered.date").alias("registered_date"),
        col("data.registered.age").alias("registered_age"),
        col("data.phone"),
        col("data.nat")
    )

load_dotenv("opt/bitnami/.env")

s3_output_path = os.getenv("s3_output_path")

query = json_df.writeStream \
    .format("parquet") \
    .option("path", s3_output_path) \
    .option("checkpointLocation", "./random_users_checkpoints/") \
    .option("compression", "snappy") \
    .outputMode("append") \
    .start()

# Attach termination listener
query.awaitTermination()
query.onQueryTermination(on_termination)


# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 /opt/bitnami/my_spark/spark_stream.py
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 /opt/bitnami/my_spark/spark_stream_s3.py
