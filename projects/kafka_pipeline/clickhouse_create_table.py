from airflow import DAG
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
from airflow.operators.python_operator import PythonOperator
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook
from airflow.utils.dates import days_ago


DAG_ID = "kafka_pipeline_create_table"
tags = ['test_dags']

default_args = {
    'owner': 'VL',
    'start_date': days_ago(1),
}


def click_create_kafka_sync():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            CREATE TABLE IF NOT EXISTS customer_log_in
            (
                name String,
                gender String,
                age Int32,
                price Int64,
                timestamp Int64
            )
            ENGINE = Kafka('broker:9094', 'customer_log', 'group1', 'JSONEachRow');
        '''
    )
    return records

def click_create_table():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            CREATE TABLE IF NOT EXISTS customer_log (
                name String,
                gender String,
                age Int32,
                price Int64,
                timestamp Int64
            ) 
            ENGINE = MergeTree()
            ORDER BY timestamp
            SETTINGS index_granularity = 8192;
        '''
    )
    return records

def click_create_mv():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            CREATE MATERIALIZED VIEW IF NOT EXISTS customer_log_tr TO customer_log AS SELECT * FROM customer_log_in;
        '''
    )
    return records

with DAG(
        dag_id=DAG_ID,
        schedule_interval=None,
        default_args=default_args,
        tags=['kafka_pipeline'],
) as dag:

    click_create_kafka_sync_task = PythonOperator(
        task_id='click_create_kafka_sync_task',
        python_callable=click_create_kafka_sync,
    )

    click_create_table_task = PythonOperator(
        task_id='click_create_table_task',
        python_callable=click_create_table,
    )

    click_create_mv_task = PythonOperator(
        task_id='click_create_mv_task',
        python_callable=click_create_mv,
    )


    click_create_kafka_sync_task >> click_create_table_task >> click_create_mv_task