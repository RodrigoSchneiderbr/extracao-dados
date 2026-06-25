# 🚀 Pipeline de Dados On-Premise: Crypto Data Lake


## 📌 Sobre o Projeto
Este projeto é um pipeline de Engenharia de Dados *End-to-End* construído com foco em portabilidade e boas práticas de arquitetura de Data Lakes. O objetivo é extrair dados de criptomoedas em tempo real, armazená-los de forma resiliente e processá-los para consumo analítico, contornando o clássico **"Small Files Problem"**.

Para evitar custos de nuvem e facilitar a avaliação, toda a infraestrutura da AWS (S3) foi emulada localmente utilizando **MinIO** via Docker. O código Python utiliza a biblioteca `boto3`, sendo 100% *Cloud-Ready* (pronto para migração para a AWS com a simples troca de variáveis de ambiente).

## 🏗️ Arquitetura de Dados

1. **Camada Raw (Ingestão):** Os dados são extraídos da API da CoinGecko e salvos em formato `JSON` na zona bruta do Data Lake, particionados por ano, mês e dia. A extração pode ocorrer múltiplas vezes ao dia sem sobrescrever dados anteriores.
2. **Camada Trusted (Processamento):** Um script em Pandas lê todos os pequenos arquivos JSON diários, achata (flatten) as estruturas aninhadas e os unifica em um único arquivo colunar otimizado (`.parquet`).
3. **Gerenciamento de Partições:** O PyArrow é utilizado para gerar as partições e os nomes dos arquivos Parquet de forma dinâmica e segura.

## 🛠️ Tecnologias Utilizadas
* **Orquestração:** Apache Airflow 2.9 (LocalExecutor) + PostgreSQL 13
* **Linguagem:** Python 3
* **Infraestrutura:** Docker & MinIO (S3 API Compatible)
* **Manipulação de Dados:** Pandas, PyArrow
* **Interação Cloud:** Boto3, S3Fs

## 📂 Estrutura do Repositório
```text
pipeline-dados/
├── dags/
│   └── crypto_pipeline.py     # DAG do Airflow definindo a ordem e agendamento
├── src/
│   ├── config.py              # Credenciais e conexão boto3
│   ├── extract.py             # Ingestão de dados (API -> MinIO Raw)
│   └── transform.py           # Processamento e otimização (Raw -> MinIO Trusted Parquet)
├── tests/
│   └── test_extract.py        # Teste unitário da extração com Mock (Pytest)
├── docker-compose.yaml        # Infraestrutura como código (Airflow, MinIO, Postgres)
├── requirements.txt           # Dependências Python
└── README.md
```

##  Testar o projeto

Subir o docker-compose do MinOI

```text
docker-compose up -d
```
Acesse o painel do MinIO em http://localhost:9001 (Login: minioadmin / Senha: minioadmin) e crie um bucket chamado datalake-crypto.

##  Criar ambiente Virutal e instalar dependencias

```text
python -m venv venv
.venv/bin/activate 
pip install -r requirements.txt
```
Criar um arquivo .env na raiz

```text
MINIO_ENDPOINT=http://minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

##  Execução do Pipeline

```text
python src/extract.py
```
Aguardar uns segundos e testar.

```text
python src/transform.py
```
##  Execução do Pipeline com airflow

subir docker

```text
docker-compose up -d
```
Data Lake (MinIO): Acesse http://localhost:9001 (User: minioadmin / Pass: minioadmin). Crie um bucket chamado datalake-crypto ou como desejar mas precisa alterar o codigo.

Orquestrador (Airflow): Acesse http://localhost:8080 (User: admin / Pass: admin).

