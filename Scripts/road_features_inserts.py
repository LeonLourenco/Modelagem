import pandas as pd
from paths import PATHS

def process_road_features():
    try:
        # Configurar pandas para evitar warnings de downcasting
        pd.set_option('future.no_silent_downcasting', True)
        
        # Carregar dados do CSV com os cabeçalhos corretos
        df = pd.read_csv(
            PATHS['road_features_input'],
            skiprows=2,  # Pular linha de cabeçalho original
            header=None,
            names=[
                "Feature_ID", "Amenity", "Bump", "Crossing", "Give_Way", 
                "Junction", "No_Exit", "Railway", "Roundabout", "Station", 
                "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
            ],
            dtype='str'
        )
        
        # Converter colunas booleanas para 0/1 sem downcasting
        bool_cols = ["Amenity", "Bump", "Crossing", "Give_Way", "Junction",
                    "No_Exit", "Railway", "Roundabout", "Station", "Stop",
                    "Traffic_Calming", "Traffic_Signal", "Turning_Loop"]
        
        for col in bool_cols:
            # Converter para maiúsculas e mapear valores
            df[col] = df[col].str.upper().map({
                'TRUE': 1,
                'FALSE': 0,
            }).fillna(0).astype(int)
        
        # =============================================
        # 1. Processar linhas únicas para ROAD_FEATURES
        # =============================================
        
        # Encontrar linhas únicas baseadas nas features
        df_unique = df[bool_cols].drop_duplicates().reset_index(drop=True)
        
        # Gerar IDs numéricos simples começando em 1
        df_unique.insert(0, 'id', range(1, len(df_unique) + 1))
        
        # Gerar arquivo SQL para ROAD_FEATURES
        with open(PATHS['road_features_insert'], "w", encoding="utf-8") as f:
            f.write("-- INSERT statements for ROAD_FEATURES table\n")
            f.write("-- Generated from unique road features combinations\n\n")
            f.write("INSERT INTO ROAD_FEATURES (\n")
            f.write("    id, Amenity, Bump, Crossing, Give_Way, Junction,\n")
            f.write("    No_Exit, Railway, Roundabout, Station, Stop,\n")
            f.write("    Traffic_Calming, Traffic_Signal, Turning_Loop\n) VALUES\n")
            
            # Gerar linhas de valores
            rows = []
            for _, row in df_unique.iterrows():
                values = [
                    str(row['id']),  # ID numérico
                    str(row['Amenity']),
                    str(row['Bump']),
                    str(row['Crossing']),
                    str(row['Give_Way']),
                    str(row['Junction']),
                    str(row['No_Exit']),
                    str(row['Railway']),
                    str(row['Roundabout']),
                    str(row['Station']),
                    str(row['Stop']),
                    str(row['Traffic_Calming']),
                    str(row['Traffic_Signal']),
                    str(row['Turning_Loop'])
                ]
                rows.append(f"({', '.join(values)})")
            
            # Escrever em blocos de 500 para evitar linhas muito longas
            for i in range(0, len(rows), 500):
                block = rows[i:i+500]
                f.write(",\n".join(block))
                f.write(";\n" if i+500 >= len(rows) else ",\n")

        # =============================================
        # 2. Gerar arquivo de eventos (mapeamento original)
        # =============================================
        
        # Criar dicionário para mapear features -> ID único
        feature_to_id = {}
        for _, row in df_unique.iterrows():
            # Criar chave única baseada nas features
            key = tuple(row[bool_cols].values)
            feature_to_id[key] = row['id']
        
        # Gerar mapeamento para o arquivo de eventos
        event_data = []
        for original_pos, original_row in df.iterrows():
            # Criar chave para a linha atual
            current_key = tuple(original_row[bool_cols].values)
            
            # Obter ID correspondente
            feature_id = feature_to_id[current_key]
            
            event_data.append({
                'Original_Position': original_pos + 1,  # Posição no arquivo original (1-based)
                'Road_Feature_ID': feature_id  # ID da combinação única
            })
        
        # Converter para DataFrame e salvar como CSV
        event_df = pd.DataFrame(event_data)
        event_df.to_csv(PATHS['road_features_events'], index=False)
        
        print(f"Arquivos gerados com sucesso:")
        print(f"- {PATHS['road_features_insert']}: {len(df_unique)} registros únicos")
        print(f"- {PATHS['road_features_events']}: {len(df)} eventos mapeados")

    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        raise

if __name__ == "__main__":
    process_road_features()