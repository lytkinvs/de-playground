from airflow import DAG
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
from airflow.operators.python_operator import PythonOperator
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook
from airflow.utils.dates import days_ago


DAG_ID = "click_create_table"
tags = ['test_dags']

default_args = {
    'owner': 'VL',
    'start_date': days_ago(1),
}


def click_create_table():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            CREATE TABLE example_table
            (
                uid String,
                gender_age String,
                timestamp Int64,
                url String
            )
            ENGINE = MergeTree()
            PARTITION BY toYYYYMM(toDate(timestamp/1000))
            PRIMARY KEY timestamp
            ORDER BY timestamp
            SETTINGS index_granularity = 8192
        '''
    )
    # print(f"Table created successfully: {records}")

with DAG(
        dag_id=DAG_ID,
        schedule_interval=None,
        default_args=default_args,
        tags =['test_dags']
) as dag:
    start = PythonOperator(
        task_id='create_table',
        python_callable=click_create_table,

    )
    start