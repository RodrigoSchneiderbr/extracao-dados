import requests
import json
from datetime import datetime, timezone
from config import get_minio_client

def run_extraction():
    print("Buscando dados da API...")
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    # Captura o timestaamp
    agora = datetime.now(timezone.utc)
    data['extracted_at'] = agora.strftime('%Y-%m-%d %H:%M:%S')
    
    s3_client = get_minio_client()
    #sugestão nome
    bucket_name = "datalake-crypto"
    
    # Congelada no nível do dia
    # Exemplo: raw/year=2026/month=06/day=24 pode ser da maneira que desejar
    partition_path = f"raw/year={agora.year}/month={agora.strftime('%m')}/day={agora.strftime('%d')}"
    
    # O ARQUIVO: Ganha a hora/minuto/segundo para evitar sobrescrever dados do mesmo dia
    
    file_name = f"crypto_{agora.strftime('%H%M%S')}.json"
    
    # Caminho final completo
    file_path = f"{partition_path}/{file_name}"
    
    print(f"Enviando para o MinIO: {file_path}")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_path,
        Body=json.dumps(data)
    )
    print("Extração concluída com sucesso!")

if __name__ == "__main__":
    run_extraction()