import pandas as pd
import os
from paths import PATHS  

# 1. Configuração de caminhos via config_paths
input_path = PATHS['day_periods_input']
output_path_main = PATHS['day_periods_insert']
output_path_events = PATHS['day_periods_events']

# 1. Leitura e preparação dos dados
try:
    # Lê o CSV pulando as 2 primeiras linhas
    df_raw = pd.read_csv(input_path, skiprows=2, header=None, names=[
        'Sunrise_Sunset', 'Civil_Twilight', 'Nautical_Twilight', 'Astronomical_Twilight'
    ])
    
    # Limpeza dos dados
    df_raw = df_raw.apply(lambda x: x.astype(str).str.strip())
    unique_periods = df_raw.drop_duplicates().reset_index(drop=True)
    unique_periods.insert(0, 'id', range(1, len(unique_periods) + 1))

    # Mapeamento para os IDs
    period_map = {
        tuple(row[1:]): row[0] for row in unique_periods.itertuples(index=False)
    }
    df_raw['id'] = df_raw.apply(lambda x: period_map.get(tuple(x[['Sunrise_Sunset', 'Civil_Twilight', 'Nautical_Twilight', 'Astronomical_Twilight']])), axis=1)

except Exception as e:
    print(f"Erro no processamento inicial: {e}")
    exit()

# 2. Geração do SQL para day_periods
try:
    with open(output_path_main, "w", encoding="utf-8") as f:
        f.write("INSERT INTO DAY_PERIODS (id, Sunrise_Sunset, Civil_Twilight, Nautical_Twilight, Astronomical_Twilight) VALUES\n")
        
        values = []
        for _, row in unique_periods.iterrows():
            vals = [
                str(row['id']),
                f"'{row['Sunrise_Sunset'].replace("'", "''")}'",
                f"'{row['Civil_Twilight'].replace("'", "''")}'",
                f"'{row['Nautical_Twilight'].replace("'", "''")}'",
                f"'{row['Astronomical_Twilight'].replace("'", "''")}'"
            ]
            values.append(f"({', '.join(vals)})")
        
        f.write(",\n".join(values))
        f.write(";\n")
    
    print(f"Main SQL gerado: {os.path.abspath(output_path_main)}")

except Exception as e:
    print(f"Erro ao gerar main SQL: {e}")

# 3. Geração do SQL para PERIOD_EVENTS (se existirem IDs mapeados)
if 'id' in df_raw.columns and not df_raw['id'].isnull().all():
    try:
        with open(output_path_events, "w", encoding="utf-8") as f:
            # Cabeçalho para múltiplos INSERTs (opcional)
            f.write("-- Inserções para tabela PERIOD_EVENTS\n")
            f.write("-- Referenciando IDs de day_periods\n\n")
            
            for idx, row in df_raw.iterrows():
                f.write(
                    f"INSERT INTO PERIOD_EVENTS (Event_ID, day_period_id) VALUES ({idx + 1}, {row['id']});\n"
                )
        
        print(f"Events SQL gerado: {os.path.abspath(output_path_events)}")
        print(f"Total de eventos: {len(df_raw)}")
    
    except Exception as e:
        print(f"Erro ao gerar events SQL: {e}")
else:
    print("Aviso: Não foi possível gerar PERIOD_EVENTS - IDs não encontrados ou inválidos")

print("Processo concluído.")