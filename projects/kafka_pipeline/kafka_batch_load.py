import json

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.dates import days_ago

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from kafka import KafkaConsumer
from datetime import datetime, timedelta
import io

TOPIC = 'customer_log'
KAFKA_BROKER = 'broker:9094'
BUCKET = "kafka-pipeline"

def process_kafka_messages(**kwargs):

    messages = kwargs['task_instance'].xcom_pull(task_ids='monitor_kafka')

    s3_hook = S3Hook("s3_connection")


    json_bytes = json.dumps(messages).encode("utf-8")
    filebuffer = io.BytesIO(json_bytes)
    filebuffer.seek(0)

    s3_hook.load_file_obj(
        file_obj=filebuffer,
        key=f"bucket/data_{int(datetime.now().timestamp())}.json",
        bucket_name=BUCKET,
        replace=True,
    )


def consume_kafka_messages(kafka_topic: str, kafka_servers: str, target_message_count: int = 10):
    consumer = KafkaConsumer(
    TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='group2',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    messages = []
    for msg in consumer:
        print(f"Received message: {msg.value}")
        messages.append(msg.value)
        if len(messages) >= target_message_count:
            break

    consumer.close()
    return messages

class KafkaMessageCounterSensor(BaseSensorOperator):

    def __init__(self, kafka_topic:str, target_message_count:int, kafka_servers: str, **kwargs):
        """
        Custom sensor to count messages in a Kafka topic.

        :param kafka_topic: The Kafka topic to monitor.
        :param target_message_count: The target number of messages to check for.
        :param kafka_servers: The Kafka broker addresses.
        """
        super().__init__(**kwargs)
        self.kafka_topic = kafka_topic
        self.target_message_count = target_message_count
        self.kafka_servers = kafka_servers
        self.messages = []

    """
    Custom sensor to count messages in Kafka topic.
    """
    def poke(self, context):
        self.messages = consume_kafka_messages(
            kafka_topic=self.kafka_topic,
            kafka_servers=self.kafka_servers,
            target_message_count=self.target_message_count
        )

        if len(self.messages) >= self.target_message_count:
            context['task_instance'].xcom_push(
                key='kafka_messages',
                value=self.messages[:self.target_message_count]
            )
            return True
        return False

    def execute(self, context):
        if self.poke(context):
            return self.messages
        raise ValueError("Not enough messages in Kafka topic")

default_args = { 'owner': 'vl' }

with DAG(
    dag_id='kafka_batch_processing_dag',
    default_args=default_args,
    catchup=False,
    schedule_interval='@continuous',
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    tags=['kafka_pipeline'],
) as dag:

    monitor_kafka = KafkaMessageCounterSensor(
        task_id='monitor_kafka',
        kafka_topic=TOPIC,
        kafka_servers=KAFKA_BROKER,
        target_message_count=50,
        mode='reschedule',
        poke_interval=10

    )


    process_messages = PythonOperator(
        task_id='process_kafka_messages',
        python_callable=process_kafka_messages,
        provide_context=True
    )

    monitor_kafka  >> process_messages

