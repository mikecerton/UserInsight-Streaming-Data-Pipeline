pip install -r /opt/bitnami/requirements.txt

for i in $(seq 10 -1 1); do
    echo "start in : $i"
    sleep 1
dones

echo "_____Ready for run spark_stream_s3.py_____"

# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5 /opt/bitnami/my_spark/spark_stream_s3.py