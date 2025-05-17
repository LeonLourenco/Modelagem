import pandas as pd
import re
from config_paths import PATHS

def extract_ids_from_sql(file_path):
    """Extrai IDs de um arquivo SQL com múltiplos INSERTs por linha"""
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith("(") or line.startswith("INSERT INTO"):
                    matches = re.findall(r'\(([^)]+)\)', line)
                    for match in matches:
                        fields = match.split(",")
                        if fields:
                            id_value = fields[0].strip()
                            if id_value.isdigit():
                                ids.append(int(id_value))
        return ids
    except FileNotFoundError:
        print(f"Aviso: Arquivo {file_path} não encontrado.")
        return None

def format_sql_value(value):
    """Formata valores para o SQL, tratando strings, números e NULLs"""
    if value == "NULL" or pd.isna(value):
        return "NULL"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # Remove aspas extras que estavam sendo adicionadas
        return f"'{str(value).replace("'", "''")}'"

# Configuração de caminhos
input_csv = PATHS['accidents_input']
output_sql = PATHS['accidents_output']
locations_sql = PATHS['locations_output']
weather_sql = PATHS['weather_output']
features_sql = PATHS['road_features_output']

# Carregar IDs das tabelas relacionadas
location_ids = extract_ids_from_sql(locations_sql) or []
weather_ids = extract_ids_from_sql(weather_sql) or []
feature_ids = extract_ids_from_sql(features_sql) or []

# Carregar e preparar dados
try:
    df = pd.read_csv(input_csv, dtype={
        'Severity': 'Int64',
        'Start_Time': 'str',
        'End_Time': 'str',
        'Distance(mi)': 'float64',
        'Description': 'str',
        'Year': 'Int64'
    })
    
    # Gerar IDs sequenciais
    df["Accident_ID"] = range(1, len(df) + 1)
    
    # Atribuir IDs relacionados (preenchendo com NULL se necessário)
    df['Location_ID'] = [location_ids[i] if i < len(location_ids) else "NULL" for i in range(len(df))]
    df['Weather_ID'] = [weather_ids[i] if i < len(weather_ids) else "NULL" for i in range(len(df))]
    df['Feature_ID'] = [feature_ids[i] if i < len(feature_ids) else "NULL" for i in range(len(df))]
    
    # Converter distância para metros (se necessário)
    df['Distance(mi)'] = df['Distance(mi)'].apply(lambda x: round(float(x) * 1609.34, 2) if pd.notna(x) else "NULL")
    
    # Gerar SQL
    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("-- INSERT statements for ACCIDENTS table\n")
        f.write(f"-- Total records: {len(df)}\n\n")
        f.write("INSERT INTO accidents (id, Severity, Start_Time, End_Time, Distance, Description, Year, Weather_ID, Location_ID, Feature_ID) VALUES\n")
        
        values = []
        for _, row in df.iterrows():
            values.append(
                f"({row['Accident_ID']}, "
                f"{row['Severity']}, "
                f"{format_sql_value(row['Start_Time'])}, "
                f"{format_sql_value(row['End_Time'])}, "
                f"{row['Distance(mi)']}, "
                f"{format_sql_value(row['Description'])}, "
                f"{row['Year']}, "
                f"{row['Weather_ID']}, "
                f"{row['Location_ID']}, "
                f"{row['Feature_ID']})"
            )
        
        # Escrever em blocos de 500 para evitar linhas muito longas
        for i in range(0, len(values), 500):
            block = values[i:i+500]
            f.write(",\n".join(block))
            f.write(";\n" if i+500 >= len(values) else ",\n")
            
    print(f"Arquivo SQL gerado com sucesso: {output_sql}")

except Exception as e:
    print(f"Erro durante o processamento: {str(e)}")
    