from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello, World!")

DAG_ID = "hello_task"
tags = ['test_dags']

default_args = {
    'owner': 'vl',
    'start_date': datetime(2021, 1, 1),
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval='@daily',
    tags=tags
) as dag:
    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=hello_world,

    )

    hello_task