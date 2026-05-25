# Pipeline de Dados - Análise de Fraude e Crédito

Este projeto consiste na implementação de um pipeline de dados automatizado e conteinerizado para a importação, limpeza, validação de qualidade (Data Quality) e transformação de dados transacionais financeiros. 

A solução foi projetada utilizando boas práticas de Engenharia de Dados, garantindo o isolamento do ambiente com Docker, tratamento de exceções e a geração de métricas de observabilidade para os dados processados.

---

## 🛠️ Tecnologias e Arquitetura

* **Linguagem Principal:** Python 3.11
* **Processamento de Dados:** Pandas (manipulação eficiente de DataFrames em memória)
* **Conteinerização:** Docker (isolamento completo de dependências)
* **Estrutura de Pastas:**
    * `quarentena/`: Onde são depositados os relatórios de erros e anomalias de qualidade dos dados.
    * `raw/`: Onde reside o arquivo bruto original enviado para o desafio.
    * `spec/`: Onde ficam as especificações e as tabelas-resultado geradas prontas para consumo.

---

## 📂 Estrutura do Projeto

A estrutura de diretórios na sua pasta de trabalho `/mnt/c/projetos/localiza/` está organizada exatamente da seguinte forma:

```text
localiza/
├── quarentena/                 # Diretório de observabilidade
│   └── anomalias_report.txt    # Relatório detalhado de qualidade dos dados
├── raw/                        # Diretório com o arquivo bruto de origem
│   └── df_fraud_credit.csv     # Base de dados original
├── spec/                       # Diretório com as tabelas-resultado geradas
│   ├── tabela_regiao_risco.csv # Resultado 1: Média de risco por região
│   └── tabela_top3_vendas.csv  # Resultado 2: Top 3 endereços em vendas recentes
├── docker-compose.yml          # Manifesto de configuração do container Docker
├── Dockerfile                  # Receita de construção da imagem Docker
├── pipeline.py                 # Script principal com a lógica de Data Quality e ETL
└── Readme.md                   # Documentação do projeto