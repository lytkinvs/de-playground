from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.models import Variable

def hello_world():
    V = Variable.get("V", deserialize_json=True)
    V['id'] += 1
    Variable.set(key="V", value=V, serialize_json=True)



DAG_ID = "hello_task"
tags = ['test_dags']

default_args = {
    'owner': 'vl',
    'start_date': datetime(2021, 1, 1),
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    start_date=datetime(2021, 1, 1),
    schedule_interval="0 0 * * *",
    catchup=False,
    tags=tags
) as dag:
    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=hello_world,

    )

    hello_task