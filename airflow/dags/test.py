from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    "depends_on_past": False,
    "email": ["ldtrung.nino@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


def print_current_time():
    print("Current time:", datetime.utcnow())


with DAG(
    default_args=default_args,
    dag_id='test',
    description='Create first dag using python operator',
    start_date=datetime(2021, 10, 6),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='print_datetime',
        python_callable=print_current_time
    )

    task1