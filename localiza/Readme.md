# Pipeline de Dados - Análise de Fraude e Crédito

Este projeto consiste na implementação de um pipeline de dados automatizado e conteinerizado para a importação, limpeza, validação de qualidade (Data Quality) e transformação de dados transacionais financeiros. 

A solução foi projetada utilizando boas práticas de Engenharia de Dados, garantindo o isolamento do ambiente com Docker, tratamento de exceções e a geração de métricas de observabilidade para os dados processados.

---

## 🛠️ Tecnologias e Arquitetura

* **Linguagem Principal:** Python 3.11
* **Processamento de Dados:** Pandas (manipulação eficiente de DataFrames em memória)
* **Conteinerização:** Docker (isolamento completo de dependências)
* **Estrutura de Pastas (Padrão Medalhão Simplificado):**
    * `Camada Raw`: Onde reside o arquivo bruto original.
    * `Camada Processed`: Onde são salvas as tabelas-resultado prontas para consumo de BI.
    * `Camada Quarantine`: Onde são depositados os relatórios de erros e anomalias de qualidade.

---

## 📂 Estrutura do Projeto

Após o processamento, a estrutura de diretórios na sua pasta de trabalho `/mnt/c/projetos/localiza/` ficará organizada da seguinte forma:

```text
/mnt/c/projetos/localiza/
├── df_fraud_credit.csv         # Arquivo bruto de origem (Base de dados)
├── pipeline.py                 # Script com a lógica de Data Quality e ETL
├── docker-compose.yml          # Manifesto de configuração do container Docker
├── processed/                  # Diretório com as tabelas-resultado (Gerado automaticamente)
│   ├── tabela_regiao_risco.csv
│   └── tabela_top3_vendas.csv
└── quarantine/                 # Diretório de observabilidade (Gerado automaticamente)
    └── anomalies_report.txt    # Relatório detalhado de qualidade dos dados