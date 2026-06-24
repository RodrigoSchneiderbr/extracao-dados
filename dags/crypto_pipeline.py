from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configurações padrão de comportamento da DAG
default_args = {
    'owner': 'engenheiro_dados',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 23),
    'retries': 1, 
    'retry_delay': timedelta(minutes=2),
}

# Definindo a DAG e o agendamento 
with DAG(
    'crypto_datalake_pipeline',
    default_args=default_args,
    description='Pipeline End-to-End de Extração e Transformação',
    schedule_interval='@hourly', 
    catchup=False,
    tags=['crypto', 'minio', 'portfolio']
) as dag:

    # Tarefa 1: Executa o script de Extração
    task_extract = BashOperator(
        task_id='extrair_dados_api',
        bash_command='cd /opt/airflow && python src/extract.py'
    )

    # Tarefa 2: Executa o script de Transformação
    task_transform = BashOperator(
        task_id='transformar_para_parquet',
        bash_command='cd /opt/airflow && python src/transform.py'
    )

    # ordem das dags
    task_extract >> task_transform