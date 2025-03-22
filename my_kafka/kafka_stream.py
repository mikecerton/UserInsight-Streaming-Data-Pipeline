from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

import os 
from dotenv import load_dotenv
import requests
import json

def fetch_api_data(api):  
    res = requests.get(api)
    res = res.json()
    res = res["results"][0]     
    return res

def create_kafka_topic(servers, cid, topic_name):
    admin_client = KafkaAdminClient(
    bootstrap_servers = servers,
    client_id = cid)

    topic = NewTopic(
        name = topic_name,
        num_partitions = 1,
        replication_factor = 1)

    try:
        admin_client.create_topics(new_topics = [topic], validate_only = False)
        print(f"Topic '{topic_name}' created successfully!")
    except TopicAlreadyExistsError:
        print(f"Topic '{topic_name}' already exists.")
    except Exception as e:
        print(f"Failed to create topic: {e}")

def stream_user_data(servers, topic_name, api):
    producer = KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    while True:
        data = fetch_api_data(api)
        print(f"Sending data: {data}") 
        producer.send(topic_name, value=data)
        print("send complete")
        producer.flush()
        # time.sleep(1)  # Optional: add a small delay to avoid flooding logs

if __name__ == "__main__":

    load_dotenv("/.env")

    servers = os.getenv("kafka_servers")
    cid = os.getenv("kafka_cid")
    topic_name = os.getenv("kafka_topic_name")
    api = os.getenv("link_api")

    create_kafka_topic(servers = servers,cid = cid, topic_name = topic_name)

    stream_user_data(servers = servers, topic_name = topic_name, api = api)

