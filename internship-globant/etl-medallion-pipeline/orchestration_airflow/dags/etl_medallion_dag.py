from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id='etl_medallion_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['medallion', 'spark'],
) as dag:

    # The command now uses 'spark-submit' to run the script
    docker_exec_command = "docker exec jupyter_spark_lab spark-submit /home/jovyan/work/"

    run_bronze = BashOperator(
        task_id='run_bronze_layer',
        bash_command=f"{docker_exec_command}bronze.py",
    )

    run_silver = BashOperator(
        task_id='run_silver_layer',
        bash_command=f"{docker_exec_command}silver.py",
    )

    run_gold = BashOperator(
        task_id='run_gold_layer',
        bash_command=f"{docker_exec_command}gold.py",
    )

    run_bronze >> run_silver >> run_gold
