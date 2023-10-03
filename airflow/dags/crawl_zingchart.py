from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.crawl_top_music_zingmp3 import extract_zingchart


default_args = {
    "depends_on_past": False,
    "email": ["ldtrung.nino@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    default_args=default_args,
    dag_id='crawl_ranking_zingchart',
    description='Crawl Rank music zingchart.',
    start_date=datetime(2021, 10, 6),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='extract_zingchart',
        python_callable=extract_zingchart
    )

    task1