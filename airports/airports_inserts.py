import pandas as pd
from pathlib import Path

# ================= CONFIGURAÇÕES =================
BASE_DIR = Path(r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2')

# Arquivos de entrada
ARQUIVO_AEROPORTOS = BASE_DIR / 'airports' / 'AIRPORTS_COM_NOME.csv'
ARQUIVO_INDICES = BASE_DIR / 'airports' / 'indices_sem_nome.txt'

# Lista de outras tabelas para filtrar
OUTRAS_TABELAS = [
    BASE_DIR / 'weather_conditions' / 'WEATHER_CONDITIONS.csv',
    BASE_DIR / 'weather' / 'WEATHER.csv',
    BASE_DIR / 'road_features' / 'ROAD_FEATURES.csv',
    BASE_DIR / 'locations' / 'LOCATIONS.csv',
    BASE_DIR / 'day_periods' / 'DAY_PERIODSDAY_PERIODS.csv',
    BASE_DIR / 'accidents' / 'ACCIDENTS.csv'
]

# ================= FUNÇÃO PRINCIPAL =================
def main():
    # 1. LER ÍNDICES PARA REMOVER
    with open(ARQUIVO_INDICES, "r") as f:
        indices_para_remover = sorted([int(linha.strip()) for linha in f if linha.strip().isdigit()])
    
    # 2. PROCESSAR AEROPORTOS
    processar_aeroportos(ARQUIVO_AEROPORTOS, indices_para_remover)
    
    # 3. FILTRAR OUTRAS TABELAS
    for tabela_path in OUTRAS_TABELAS:
        filtrar_tabela(tabela_path, indices_para_remover)

# ================= FUNÇÕES AUXILIARES =================
def processar_aeroportos(caminho_aeroportos, indices_remover):
    # Configuração para suprimir warnings específicos
    pd.options.mode.chained_assignment = None  # Desativa SettingWithCopyWarning
    
    # Ler CSV especificando dtype para evitar warnings
    df = pd.read_csv(caminho_aeroportos, dtype={
        'Airport_Code': 'str',
        'Timezone': 'str',
        'Airport_Name': 'str'
    })
    
    # Limpeza de dados
    df['Airport_Code'] = df['Airport_Code'].str.strip()
    df['Timezone'] = df['Timezone'].str.strip()
    df['Airport_Name'] = df['Airport_Name'].fillna('').str.strip()
    
    # Remover duplicatas
    df_unico = df.drop_duplicates(subset=["Airport_Code", "Timezone", "Airport_Name"])
    
    # Criar diretório se não existir
    (BASE_DIR / 'airports').mkdir(parents=True, exist_ok=True)
    
    # Gerar INSERTs SQL
    output_sql = BASE_DIR / 'airports' / 'airport_inserts.sql'
    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("-- INSERT statements for AIRPORTS table\n")
        f.write("-- Generated automatically from AIRPORTS_COM_NOME.csv\n\n")
        f.write("INSERT INTO AIRPORTS (Airport_Code, Timezone, Airport_Name) VALUES\n")
        
        values = []
        for _, row in df_unico.iterrows():
            code = row["Airport_Code"].replace("'", "''")
            timezone = row["Timezone"].replace("'", "''")
            name = row["Airport_Name"].replace("'", "''")
            values.append(f"('{code}', '{timezone}', '{name}')")
        
        f.write(",\n".join(values))
        f.write(";\n")
    
    print(f"INSERTs de AIRPORTS gerados em '{output_sql}'")
    
    # Gerar airport_events.csv
    code_to_id = {code: i for i, code in enumerate(df_unico["Airport_Code"], start=1)}
    event_df = df[['Airport_Code']].copy()
    event_df['Airport_ID'] = event_df['Airport_Code'].map(code_to_id)
    event_df_filtrado = event_df.drop(index=indices_remover, errors='ignore').reset_index(drop=True)
    
    output_csv = BASE_DIR / 'airports' / 'airport_events.csv'
    event_df_filtrado.to_csv(output_csv, index=False)
    
    print(f"'{output_csv}' gerado com Airport_IDs atualizados")

def filtrar_tabela(caminho_tabela, indices_remover):
    # Ler CSV com low_memory=False para evitar warnings
    df = pd.read_csv(caminho_tabela, low_memory=False)
    
    # Criar nome do arquivo de saída
    nome_saida = caminho_tabela.with_name(caminho_tabela.stem + "_filtrado.csv")
    
    # Filtrar e salvar
    df_filtrado = df.drop(index=indices_remover, errors='ignore').reset_index(drop=True)
    df_filtrado.to_csv(nome_saida, index=False)
    
    print(f"Tabela '{caminho_tabela}' filtrada e salva como '{nome_saida}'")

if __name__ == "__main__":
    main()