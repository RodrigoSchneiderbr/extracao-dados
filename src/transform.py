import pandas as pd
import json
import os
import s3fs
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timezone
from config import get_minio_client
from dotenv import load_dotenv

load_dotenv()

def run_transformation():
    print("Iniciando a transformação dos dados...")
    s3_client = get_minio_client()
    bucket_name = "datalake-crypto"
    
    agora = datetime.now(timezone.utc)
    raw_prefix = f"raw/year={agora.year}/month={agora.strftime('%m')}/day={agora.strftime('%d')}/"
    print(f"Procurando arquivos em: {raw_prefix}")
    
    # Leitura dos dados brutos
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=raw_prefix)
    
    if 'Contents' not in response:
        print("Nenhum dado encontrado para transformar na partição de hoje.")
        return
    
    all_data = []
    for obj in response['Contents']:
        file_key = obj['Key']
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = json.loads(file_obj['Body'].read().decode('utf-8'))
        all_data.append(file_content)
        
    print(f"{len(all_data)} arquivos lidos com sucesso. Consolidando...")
    
    # Tratamento no Pandas
    df = pd.json_normalize(all_data)
    df['extracted_at'] = pd.to_datetime(df['extracted_at'])
    
    df['year'] = df['extracted_at'].dt.strftime('%Y')
    df['month'] = df['extracted_at'].dt.strftime('%m')
    df['day'] = df['extracted_at'].dt.strftime('%d')
    
    #  Conversão para Tabela PyArrow
    table = pa.Table.from_pandas(df)
    
    #  Configuração do FileSystem (s3fs) apontando para o MinIO
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': os.getenv('MINIO_ENDPOINT')},
        key=os.getenv('MINIO_ACCESS_KEY'),
        secret=os.getenv('MINIO_SECRET_KEY')
    )
    
    # 5. Escrita automática do Dataset via PyArrow
    print("Salvando no MinIO via PyArrow Dataset...")
    pq.write_to_dataset(
        table,
        root_path=f"{bucket_name}/trusted",
        partition_cols=['year', 'month', 'day'],
        filesystem=fs,
        existing_data_behavior='overwrite_or_ignore' 
    )
    
    print("Processo de Transformação finalizado com sucesso!")

if __name__ == "__main__":
    run_transformation()