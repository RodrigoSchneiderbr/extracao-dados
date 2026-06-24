import os
import boto3
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (esta no gitignore entao precisar criar)
load_dotenv()

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=os.getenv('MINIO_ENDPOINT'),
        aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('MINIO_SECRET_KEY')
    )