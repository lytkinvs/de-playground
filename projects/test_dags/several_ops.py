import random

from typing import Dict, Any

from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


DAG_ID = "call_several_methods"

def callback_one():
    return "one"
def callback_two():
    return "two"

callbacks = dict(zip(["callback_one", "callback_two"],
                  [callback_one, callback_two]))



dag = DAG(
    dag_id=DAG_ID,
    max_active_runs=1,
    concurrency=3,
    schedule_interval="0 4 * * *",
    start_date=days_ago(1),
    tags=["test_dags"]
)


def download_data() -> None:
    return random.randint(0, 5)


def train_model(**kwargs) -> Dict[str, Any]:

    model_name = kwargs["callback_name"]
    funcs = {}
    funcs[f"{model_name}"] = callbacks[model_name]()

    return funcs


def save_results(**kwargs) -> None:

    ti = kwargs["ti"]
    result = ti.xcom_pull(
        task_ids=[f"task_train_model_{model_name}" for model_name in callbacks.keys()]
    )
    print(result)


task_download_data = PythonOperator(task_id="task_download_data",
                                     python_callable=download_data,
                                     dag=dag)

training_model_tasks = [
    PythonOperator(
        task_id=f"task_train_model_{model_name}",
        python_callable=train_model,
        dag=dag,
        provide_context=True,
        op_kwargs={"callback_name": model_name})
    for model_name in callbacks.keys()
]

task_save_results = PythonOperator(task_id="task_save_results",
                                   python_callable=save_results,
                                   dag=dag, provide_context=True)

task_download_data >> training_model_tasks >> task_save_results