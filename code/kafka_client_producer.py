from kafka import KafkaProducer
from pydantic import BaseModel


class PushModel(BaseModel):
    timestamp: int
    level: str
    message: str

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8'),
)

for i in range(1000):
    topic= 'customer_log'
    value = PushModel(
        timestamp=1234567890,
        level='INFO',
        message='This is a test message'
    )

    producer.send(topic, value.model_dump_json())
producer.flush()
