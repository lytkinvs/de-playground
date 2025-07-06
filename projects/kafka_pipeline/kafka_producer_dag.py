

import random
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable

from kafka import KafkaProducer
from pydantic import BaseModel



class OrderModel(BaseModel):
    id: int = 0
    name: str
    gender: str
    age: int
    price: int
    timestamp: int = 0

KAFKA_BROKER = 'broker:9094'
KAFKA_TOPIC = 'customer_log'

class KafkaProduceOperator(BaseOperator):
    """
    Custom operator to produce messages to Kafka.
    """
    @apply_defaults
    def __init__(self, kafka_broker, kafka_topic, num_records = 100, *args, **kwargs):
        super(KafkaProduceOperator, self).__init__(*args, **kwargs)
        self.kafka_broker = kafka_broker
        self.kafka_topic = kafka_topic
        self.num_records = num_records

    def execute(self, context):

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: v.encode('utf-8'),
        )
        pipeline_record_id = Variable.get("pipeline_record_id")
        id = int(pipeline_record_id)
        for i in range(self.num_records):

            # Create a random order
            order = OrderModel(
                id=id,
                name=
                random.choice(["Alice", "Bob", "Charlie", "David", "Eve"]) +
                " " +
                random.choice(["Smith", "Johnson", "Williams", "Jones", "Brown"]),
                age=random.randint(18, 65),
                price=random.randint(100, 1000),
                timestamp=int(datetime.now().timestamp()),
                gender=random.choice(["Male", "Female"]))

            id += 1
            producer.send(
                self.kafka_topic,
                value=order.model_dump_json()
            )


        Variable.set(key="pipeline_record_id", value=id)
        producer.flush()


default_args = { 'owner': 'vl', 'start_date': datetime(2023, 10, 1)}

with DAG(
    dag_id='kafka_pipeline_producer_dag',
    default_args=default_args,
    catchup=False,
    schedule_interval='*/1 * * * *',
    tags=['kafka_pipeline'],
) as dag:


    produce = KafkaProduceOperator(
        task_id='produce_to_kafka',
        kafka_broker=KAFKA_BROKER,
        kafka_topic=KAFKA_TOPIC,
        num_records=10,
    )

    produce
