from confluent_kafka import Producer
from pydantic import BaseModel


class PushModel(BaseModel):
    timestamp: int
    level: str
    message: str

conf = {
    'bootstrap.servers': '127.0.0.1:9092',
}
producer = Producer(conf)
topic= 'topic'

def delivery_report(err, msg):
    if err:
        print(f"Failed to deliver message: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_messages(producer, keys):
    for key in keys:
        value = PushModel(timestamp=1234, level="test", message="test")
        producer.produce(topic, value.model_dump_json(), key=key, callback=delivery_report)
    producer.flush()

if __name__ == "__main__":
    keys = ['Amy', 'Brenda', 'Cindy']
    keys = ['1']
    send_messages(producer, keys)
