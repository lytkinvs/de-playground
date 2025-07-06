from airflow import DAG
from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
from airflow.operators.python_operator import PythonOperator
from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook
from airflow.utils.dates import days_ago


DAG_ID = "kafka_pipeline_drop_table"
tags = ['test_dags']

default_args = {
    'owner': 'VL',
    'start_date': days_ago(1),
}


def click_drop_kafka_sync():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            DROP TABLE IF EXISTS customer_log_in
        '''
    )
    return records

def click_drop_table():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            DROP TABLE IF EXISTS customer_log 
        '''
    )
    return records

def click_drop_mv():
    ch_hook = ClickHouseHook(clickhouse_conn_id='clickhouse_conn')

    records = ch_hook.execute(
        '''
            DROP TABLE IF EXISTS consumer_log_tr;
        '''
    )
    return records

with DAG(
        dag_id=DAG_ID,
        schedule_interval=None,
        default_args=default_args,
        tags=['kafka_pipeline'],
        catchup=False,
) as dag:

    click_drop_kafka_sync_task = PythonOperator(
        task_id='click_drop_kafka_sync_task',
        python_callable=click_drop_kafka_sync,
    )

    click_drop_table_task = PythonOperator(
        task_id='click_drop_table_task',
        python_callable=click_drop_table,
    )

    click_drop_mv_task = PythonOperator(
        task_id='click_drop_mv_task',
        python_callable=click_drop_mv,
    )


    click_drop_kafka_sync_task >> click_drop_table_task >> click_drop_mv_task