import pandas as pd

# ================= CONFIGURAÇÕES =================
# Arquivos de entrada
ARQUIVO_AEROPORTOS = r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\airports\AIRPORTS_COM_NOME.csv'
ARQUIVO_INDICES = r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\airports\indices_sem_nome.txt'

# Lista de outras tabelas para filtrar
OUTRAS_TABELAS = [
    r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\weather_conditions\WEATHER_CONDITIONS.csv',
    r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\weather\WEATHER.csv',
    r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\road_features\ROAD_FEATURES.csv',
    r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\locations\LOCATIONS.csv',
    r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\day_periods\DAY_PERIODSDAY_PERIODS.csv',
    r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\accidents\ACCIDENTS.csv'
]

# ================= FUNÇÃO PRINCIPAL =================
def main():
    # 1. LER ÍNDICES PARA REMOVER
    with open(ARQUIVO_INDICES, "r") as f:
        indices_para_remover = sorted([int(linha.strip()) for linha in f if linha.strip().isdigit()])
    
    # 2. PROCESSAR AEROPORTOS E GERAR INSERTS SQL
    processar_aeroportos(ARQUIVO_AEROPORTOS, indices_para_remover)
    
    # 3. FILTRAR OUTRAS TABELAS
    for tabela_path in OUTRAS_TABELAS:
        filtrar_tabela(tabela_path, indices_para_remover)

# ================= FUNÇÕES AUXILIARES =================
def processar_aeroportos(caminho_aeroportos, indices_remover):
    # Ler e limpar dados
    df = pd.read_csv(caminho_aeroportos)
    df['Airport_Code'] = df['Airport_Code'].astype(str).str.strip()
    df['Timezone'] = df['Timezone'].astype(str).str.strip()
    df['Airport_Name'] = df['Airport_Name'].fillna('').astype(str).str.strip()
    
    # Remover duplicatas
    df_unico = df.drop_duplicates(subset=["Airport_Code", "Timezone", "Airport_Name"])
    
    # Gerar INSERTs SQL
    with open("airports/airport_inserts.sql", "w", encoding="utf-8") as f:
        for _, row in df_unico.iterrows():
            code = row["Airport_Code"].replace("'", "''")
            timezone = row["Timezone"].replace("'", "''")
            name = row["Airport_Name"].replace("'", "''")
            f.write(f"INSERT INTO AIRPORTS (Airport_Code, Timezone, Airport_Name) VALUES ('{code}', '{timezone}', '{name}');\n")
    
    print("INSERTs de AIRPORTS gerados em 'airports/airport_inserts.sql'")
    
    # Gerar airport_events.csv com IDs
    code_to_id = {code: i for i, code in enumerate(df_unico["Airport_Code"], start=1)}
    event_df = df[['Airport_Code']].copy()
    event_df['Airport_ID'] = event_df['Airport_Code'].map(code_to_id)
    event_df_filtrado = event_df.drop(index=indices_remover, errors='ignore').reset_index(drop=True)
    event_df_filtrado.to_csv("airports/airport_events.csv", index=False)
    
    print("'airports/airport_events.csv' gerado com Airport_IDs atualizados")

def filtrar_tabela(caminho_tabela, indices_remover):
    df = pd.read_csv(caminho_tabela)
    nome_saida = caminho_tabela.replace(".csv", "_filtrado.csv")
    
    df_filtrado = df.drop(index=indices_remover, errors='ignore').reset_index(drop=True)
    df_filtrado.to_csv(nome_saida, index=False)
    
    print(f"Tabela '{caminho_tabela}' filtrada e salva como '{nome_saida}'")

# Executar o programa
if __name__ == "__main__":
    main()