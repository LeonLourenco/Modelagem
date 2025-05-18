import pandas as pd
from paths import PATHS 

def main():
    # 1. Processar aeroportos
    processar_aeroportos(PATHS['airports_output'])

def processar_aeroportos(caminho_aeroportos):
    # Ler e limpar dados
    df = pd.read_csv(caminho_aeroportos, dtype={
        'Airport_Code': 'str',
        'Timezone': 'str',
        'Airport_Name': 'str'
    })
    
    # Limpeza
    df['Airport_Code'] = df['Airport_Code'].str.strip()
    df['Timezone'] = df['Timezone'].str.strip()
    df['Airport_Name'] = df['Airport_Name'].fillna('').str.strip()
    
    # Aeroportos únicos 
    df_unico = df.drop_duplicates(subset=["Airport_Code", "Timezone", "Airport_Name"])
    
    # =====================
    # 1. INSERTs para AIRPORTS (apenas aeroportos únicos e filtrados)
    # =====================
    with open(PATHS['airports_insert'], "w", encoding="utf-8") as f:
        f.write("INSERT INTO AIRPORTS (Airport_Code, Name, Timezone) VALUES\n")
        
        values = []
        for _, row in df_unico.iterrows():
            code = row["Airport_Code"].replace("'", "''")
            name = row["Airport_Name"].replace("'", "''")
            timezone = row["Timezone"].replace("'", "''")
            values.append(f"('{code}', '{name}', '{timezone}')")
        
        f.write(",\n".join(values))
        f.write(";\n")
    
    # =====================
    # 2. Gera airport_events (ordem dos aeroportos)
    # =====================
    event_df = df[['Airport_Code']].copy()
    event_df['Event_ID'] = event_df.index + 1  # Ordem no arquivo 
    
    # Salva como CSV
    event_df[['Event_ID', 'Airport_Code']].to_csv(PATHS['airport_events'], index=False)
    
    print(f"Aeroportos únicos: {len(df_unico)}")
    print(f"Eventos gerados: {len(df)}")

if __name__ == "__main__":
    main()