from airflow import DAG
from datetime import datetime

from airflow.operators.python_operator import PythonOperator


DAG_ID = "without_schedule"
tags = ['test_dags']

def print_text():
    print("without schedule")

with DAG(
    dag_id=DAG_ID,
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    tags=tags,
    catchup=False
) as dag:
    train = PythonOperator(
        task_id="train_model_task",
        python_callable=print_text,
    )

    train