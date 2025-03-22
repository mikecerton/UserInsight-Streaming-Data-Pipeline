pip install -r requirements.txt

for i in $(seq 5 -1 1); do
    echo "start in : $i"
    sleep 1
done

echo "_____Running kafka_stream.py_____"

python /my_kafka/kafka_stream.py

tail -f /dev/null