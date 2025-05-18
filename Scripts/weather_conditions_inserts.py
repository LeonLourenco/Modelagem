import pandas as pd
from paths import PATHS 

# Lê o CSV pulando as 2 primeiras linhas de metadados
df_raw = pd.read_csv(
    PATHS['weather_conditions_input'], 
    skiprows=2, 
    header=None, 
    names=['Description']
)

# Remove espaços e normaliza
df_raw['Description'] = df_raw['Description'].astype(str).str.strip()

# Remove duplicatas mantendo a primeira ocorrência
unique_conditions = df_raw.drop_duplicates().reset_index(drop=True)

# Cria os IDs para cada condição única
unique_conditions.insert(0, 'id', range(1, len(unique_conditions) + 1))

# =====================
# 1. Gera os INSERTs da tabela weather_conditions (IDs únicos e descrições)
# =====================
with open(PATHS['weather_conditions_insert'], 'w', encoding='utf-8') as f:
    f.write("INSERT INTO WEATHER_CONDITIONS (id, Description) VALUES\n")
    
    rows = []
    for _, row in unique_conditions.iterrows():
        desc = row['Description'].replace("'", "''")  # Escapar aspas simples
        rows.append(f"({row['id']}, '{desc}')")
    
    f.write(",\n".join(rows))
    f.write(";\n")

# =====================
# 2. Gera INSERTs para weather_conditions_events
# =====================

# Cria um dicionário para mapear descrição -> ID único
desc_to_id = dict(zip(unique_conditions['Description'], unique_conditions['id']))

with open(PATHS['weather_conditions_events'], 'w', encoding='utf-8') as f:
    for idx, row in df_raw.reset_index().iterrows():  # Garante que o índice seja sequencial
        event_id = idx + 1
        weather_id = desc_to_id[row['Description']]  # Pega o ID correspondente à descrição
        f.write(
            f"INSERT INTO WEATHER_CONDITIONS_EVENTS (Event_ID, Weather_Condition_ID) VALUES ({event_id}, {weather_id});\n"
        )

print("Scripts gerados com sucesso!")