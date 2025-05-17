import pandas as pd
from config_paths import PATHS 

# Lê o CSV pulando as 2 primeiras linhas de metadados
df_raw = pd.read_csv(PATHS['weather_conditions_input'], skiprows=2, header=None, names=['Description'])

# Remove espaços e normaliza
df_raw['Description'] = df_raw['Description'].astype(str).str.strip()

# Remove duplicatas mantendo a primeira ocorrência
unique_conditions = df_raw.drop_duplicates().reset_index(drop=True)

# Cria os IDs para cada condição única
unique_conditions.insert(0, 'id', range(1, len(unique_conditions) + 1))

# =====================
# 1. Gera os INSERTs da tabela weather_conditions no formato desejado
# =====================
with open(PATHS['weather_conditions_output'], 'w', encoding='utf-8') as f:
    # Escreve o início do comando INSERT
    f.write("INSERT INTO weather_conditions (id, description) VALUES\n")
    
    # Prepara todas as linhas de valores
    rows = []
    for _, row in unique_conditions.iterrows():
        desc = row['Description'].replace("'", "''")  # Escapar aspas simples
        rows.append(f"({row['id']}, '{desc}')")
    
    # Junta todas as linhas com vírgulas e quebra de linha
    f.write(",\n".join(rows))
    
    # Finaliza com ponto-e-vírgula
    f.write(";\n")

print("Script de INSERT gerado com sucesso!")