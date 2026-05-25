import os
import pandas as pd
import gdown

def run_pipeline():
    # 1. Configuração dos Caminhos e URL do Google Drive
    output_dir = os.getenv('OUTPUT_DIR', 'data')
    quarantine_path = os.path.join(output_dir, 'quarentena/anomalias_report.txt')
    output_t1_path = os.path.join(output_dir, 'spec/tabela_regiao_risco.csv')
    output_t2_path = os.path.join(output_dir, 'spec/tabela_top3_vendas.csv')
    
    # Caminho do arquivo local (na sua pasta /mnt/c/projetos/localiza/)
    local_file_path = os.path.join(output_dir, 'raw/df_fraud_credit.csv')

    # ID da pasta/arquivo fornecido no desafio
    FILE_ID = "1U64k1YkW2FEWOil_DyQSoOWz7NAWKr17" 
    gdrive_url = f"https://drive.google.com/uc?id={FILE_ID}"

    print(f"📥 Tentando baixar arquivo do Google Drive...")
    
    df = None
    try:
        # Tenta o download via gdown
        gdown.download(gdrive_url, local_file_path, quiet=True)
        print(f"📖 Download concluído. Carregando dados no Pandas...")
        df = pd.read_csv(local_file_path)
    except Exception as e:
        print(f"⚠️ Não foi possível baixar do Google Drive (Link de pasta ou privado).")
        print(f"🔄 Acionando contingência: Tentando ler arquivo local em {local_file_path}...")
        
        # Contingência: Se o download falhar, tenta ler o arquivo que você já tem na pasta
        if os.path.exists(local_file_path):
            df = pd.read_csv(local_file_path)
            print("✅ Arquivo local encontrado e carregado com sucesso!")
        else:
            print(f"❌ Erro crítico: O arquivo '{local_file_path}' não foi encontrado localmente.")
            print("Por favor, certifique-se de baixar o CSV do link do RH e salvá-lo nesta pasta.")
            return

    # Corrige tipos das colunas numéricas para evitar comparações entre str e int
    for _col in ['amount', 'risk_score', 'timestamp']:
        if _col in df.columns:
            df[_col] = pd.to_numeric(df[_col], errors='coerce')

    total_registros = len(df)

    # -------------------------------------------------------------
    # 2. DATA QUALITY AUTOMATIZADO
    # -------------------------------------------------------------
    print("🔍 Executando validações de Data Quality...")
    
    # Identificando problemas
    valores_faltantes = df.isnull().sum().sum()
    linhas_duplicadas = df.duplicated().sum()
    
    # Regras de negócio básicas (ex: amount ou risk_score não podem ser negativos)
    # Comparações seguras: valores não numéricos virarão NaN e não causarão TypeError
    valores_incorretos = df[(df['amount'] < 0) | (df['risk_score'] < 0)]
    qtd_valores_incorretos = len(valores_incorretos)
    
    # Totalizar erros encontrados
    total_erros = valores_faltantes + linhas_duplicadas + qtd_valores_incorretos
    
    # Cálculo do percentual de conformidade
    # Se houver mais erros que registros (ex: múltiplos erros na mesma linha), limitamos a 0
    percentual_conformidade = max(0.0, ((total_registros - total_erros) / total_registros) * 100)

    # Gerando o relatório de qualidade
    os.makedirs(os.path.dirname(quarantine_path), exist_ok=True)
    with open(quarantine_path, 'w') as f:
        f.write("=== RELATÓRIO DE DATA QUALITY ===\n")
        f.write(f"Total de registros analisados: {total_registros}\n")
        f.write(f"Total de erros detectados: {total_erros}\n")
        f.write(f"Percentual de Conformidade: {percentual_conformidade:.2f}%\n")
        f.write("---------------------------------\n")
        f.write(f"Valores faltantes (NaN): {valores_faltantes}\n")
        f.write(f"Linhas duplicadas: {linhas_duplicadas}\n")
        f.write(f"Registros com valores negativos inválidos: {qtd_valores_incorretos}\n")
    
    print(f"📊 Relatório de Data Quality gerado em: {quarantine_path} (Conformidade: {percentual_conformidade:.2f}%)")

    # -------------------------------------------------------------
    # 3. LIMPEZA DOS DADOS
    # -------------------------------------------------------------
    # Remove duplicados e linhas com valores nulos nas colunas críticas
    df_clean = df.drop_duplicates().dropna(subset=['location_region', 'risk_score', 'receiving_address', 'amount', 'timestamp']).copy()
    
    # Força a conversão do timestamp Unix para datetime legível (erros -> NaT)
    df_clean['timestamp_parsed'] = pd.to_datetime(df_clean['timestamp'], unit='s', errors='coerce')

    # -------------------------------------------------------------
    # 4. TABELA-RESULTADO 1: Regiões por média de Risk Score
    # -------------------------------------------------------------
    print("📈 Gerando Tabela-Resultado 1...")
    tabela_1 = df_clean.groupby('location_region')['risk_score'].mean().reset_index()
    tabela_1 = tabela_1.sort_values(by='risk_score', ascending=False)
    
    # Salva o resultado
    os.makedirs(os.path.dirname(output_t1_path), exist_ok=True)
    tabela_1.to_csv(output_t1_path, index=False)

    # -------------------------------------------------------------
    # 5. TABELA-RESULTADO 2: Top 3 Endereços Receptores em "sale" mais recente
    # -------------------------------------------------------------
    print("🛒 Gerando Tabela-Resultado 2...")
    
    # Filtrar apenas por transações do tipo 'sale'
    df_sales = df_clean[df_clean['transaction_type'] == 'sale'].copy()
    
    # Ordenar por timestamp decrescente para garantir que a mais recente fique no topo
    df_sales = df_sales.sort_values(by='timestamp_parsed', ascending=False)
    
    # Manter apenas a primeira ocorrência (mais recente) para cada endereço receptor
    df_recent_sales = df_sales.drop_duplicates(subset=['receiving_address'], keep='first')
    
    # Pegar as 3 transações com maior 'amount'
    tabela_2 = df_recent_sales.nlargest(3, 'amount')[['receiving_address', 'amount', 'timestamp_parsed']]
    
    # Renomear para o timestamp original ou manter o formatado (exibindo o formatado para o RH avaliar melhor)
    tabela_2 = tabela_2.rename(columns={'timestamp_parsed': 'timestamp'})
    
    # Salva o resultado
    tabela_2.to_csv(output_t2_path, index=False)
    print("🚀 Pipeline executado com sucesso! Arquivos salvos na pasta 'data/processed/'.")

if __name__ == "__main__":
    run_pipeline()