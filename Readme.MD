# 🚀 Pipeline de Dados On-Premise: Crypto Data Lake


## 📌 Sobre o Projeto
Este projeto é um pipeline de Engenharia de Dados *End-to-End* construído com foco em portabilidade e boas práticas de arquitetura de Data Lakes. O objetivo é extrair dados de criptomoedas em tempo real, armazená-los de forma resiliente e processá-los para consumo analítico, contornando o clássico **"Small Files Problem"**.

Para evitar custos de nuvem e facilitar a avaliação, toda a infraestrutura da AWS (S3) foi emulada localmente utilizando **MinIO** via Docker. O código Python utiliza a biblioteca `boto3`, sendo 100% *Cloud-Ready* (pronto para migração para a AWS com a simples troca de variáveis de ambiente).

## 🏗️ Arquitetura de Dados

1. **Camada Raw (Ingestão):** Os dados são extraídos da API da CoinGecko e salvos em formato `JSON` na zona bruta do Data Lake, particionados por ano, mês e dia. A extração pode ocorrer múltiplas vezes ao dia sem sobrescrever dados anteriores.
2. **Camada Trusted (Processamento):** Um script em Pandas lê todos os pequenos arquivos JSON diários, achata (flatten) as estruturas aninhadas e os unifica em um único arquivo colunar otimizado (`.parquet`).
3. **Gerenciamento de Partições:** O PyArrow é utilizado para gerar as partições e os nomes dos arquivos Parquet de forma dinâmica e segura.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3
* **Infraestrutura:** Docker & MinIO (S3 API Compatible)
* **Manipulação de Dados:** Pandas, PyArrow
* **Interação Cloud:** Boto3, S3Fs
* **Testes:** Pytest (com Mocking de API)

## 📂 Estrutura do Repositório
```text
meu-portfolio-de/
├── src/
│   ├── config.py          # Configurações do cliente S3 (boto3)
│   ├── extract.py         # Consumo da API e carga na camada Raw (JSON)
│   └── transform.py       # Transformação e carga na camada Trusted (Parquet)
├── tests/
│   └── test_extract.py    # Testes unitários com simulação (Mock) da API
├── README.md
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
MINIO_ENDPOINT=http://localhost:9000
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

