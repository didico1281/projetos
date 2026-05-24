# Data Pipeline Challenge - Fraud & Credit Analysis

Este projeto consiste na implementação de um pipeline de dados automatizado e conteinerizado para importação, limpeza, validação de qualidade (Data Quality) e transformação de dados transacionais financeiros.

O desafio foi desenhado seguindo as melhores práticas de Engenharia de Dados, garantindo resiliência, validação de métricas de conformidade e facilidade de execução em qualquer ambiente.

---

## 🛠️ Stack Tecnológico e Arquitetura

* **Linguagem de Processamento:** Python 3.11 com a biblioteca **Pandas** para manipulação eficiente de DataFrames.
* **Conteinerização:** **Docker & Docker Compose** para isolamento de ambiente, garantindo que o pipeline rode sem a necessidade de instalar dependências locais na máquina hospedeira.
* **Camadas de Dados (Medalhão Simplificado):**
    * `Raw`: Dados brutos recebidos para processamento.
    * `Processed`: Tabelas-resultado prontas para consumo analítico.
    * `Quarantine`: Armazenamento de relatórios de métricas de qualidade e anomalias.

---

## 📐 Estrutura do Projeto

A estrutura de pastas no diretório de trabalho do projeto está organizada da seguinte forma:

```text
/mnt/c/projetos/localiza/
├── df_fraud_credit.csv         # Arquivo bruto de origem (Base de dados)
├── pipeline.py                 # Script core com a lógica de DQ, Limpeza e ETL
├── docker-compose.yml          # Manifesto do Docker para orquestração local
├── processed/                  # Diretório com as tabelas-resultado (Gerado pelo pipeline)
│   ├── tabela_regiao_risco.csv
│   └── tabela_top3_vendas.csv
└── quarantine/                 # Diretório de observabilidade (Gerado pelo pipeline)
    └── anomalies_report.txt    # Relatório com métricas de qualidade dos dados

> 📌 **Nota sobre a Fonte de Dados (Google Drive):**
> O link fornecido no escopo do desafio aponta para um diretório compartilhado (Folder). 
> Para garantir a resiliência do pipeline contra restrições de API e permissões de download de pastas do Google Drive, 
> o script foi desenhado com um mecanismo de *fallback* automático. 
> Caso o download direto seja interrompido, o pipeline busca e processa o arquivo `df_fraud_credit.csv` presente na raiz do diretório local.