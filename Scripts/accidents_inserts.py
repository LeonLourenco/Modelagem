import pandas as pd
import re
from datetime import datetime
from paths import PATHS

def extract_ids_from_sql(file_path):
    """Extrai IDs de arquivos SQL no formato específico"""
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('('):
                    # Extrai o primeiro valor entre parênteses (o ID)
                    match = re.match(r'\((\d+)', line.strip())
                    if match:
                        ids.append(match.group(1))
        return ids
    except Exception as e:
        print(f"Erro ao ler {file_path}: {str(e)}")
        return []

def extract_ids_from_csv(file_path):
    """Extrai IDs de arquivos CSV no formato específico"""
    try:
        df = pd.read_csv(file_path)
        if 'Road_Feature_ID' in df.columns:
            return df['Road_Feature_ID'].astype(str).tolist()
        return []
    except Exception as e:
        print(f"Erro ao ler {file_path}: {str(e)}")
        return []

def clean_id(value):
    """Limpa IDs removendo aspas e espaços"""
    if pd.isna(value) or value in ['', 'NULL']:
        return None
    return str(value).strip().replace("'", "").replace('"', '')

def format_timestamp(value):
    """Converte string de data para formato TIMESTAMP do MySQL, removendo timezone"""
    try:
        # Remove a parte do timezone (-05:00)
        dt_str = re.sub(r'[+-]\d{2}:\d{2}$', '', str(value)).strip()
        return f"'{datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')}'"
    except Exception as e:
        print(f"Erro ao formatar timestamp {value}: {str(e)}")
        return 'NULL'

def clean_distance(value):
    """Limpa e converte valores de distância"""
    if pd.isna(value) or str(value).upper() == 'NULL':
        return None
    try:
        # Remove pontos que podem ser separadores de milhares
        clean_val = str(value).replace('.', '').replace(',', '.')
        return float(clean_val)
    except:
        return None

def format_sql_value(value, field_type):
    """Formata valores para o SQL conforme o tipo de campo"""
    if pd.isna(value) or str(value).upper() == 'NULL' or value == '':
        return 'NULL'
    
    if field_type == 'string':
        return f"'{str(value).replace("'", "''")}'"
    elif field_type == 'timestamp':
        return format_timestamp(value)
    elif field_type == 'year':
        return str(int(value)) if str(value).isdigit() else 'NULL'
    else:  # number
        return str(value)

# Carregar IDs das tabelas relacionada
location_ids = extract_ids_from_sql(PATHS['locations_insert']) 
feature_ids = extract_ids_from_csv(PATHS['road_features_events'])
weather_ids = extract_ids_from_sql(PATHS['weather_insert'])

print(f"IDs coletados - Locations: {len(location_ids)}, Weather: {len(weather_ids)}, Features: {len(feature_ids)}")

# Carregar e preparar dados do arquivo de acidentes
try:
    # Carregar CSV de acidentes
    df = pd.read_csv(PATHS['accidents_input'], dtype={
        'Accident_ID*': 'str',
        'Severity': 'Int64',
        'Start_Time': 'str',
        'End_Time': 'str',
        'Distance(mi)': 'str',  # Mudamos para str para fazer a limpeza manual
        'Description': 'str',
        'Location_ID**': 'str',
        'Feature_ID*': 'str',
        'Weather_ID**': 'str',
        'Year': 'Int64'
    })
    
    # Renomear colunas para nomes mais limpos
    df = df.rename(columns={
        'Accident_ID*': 'Accident_ID',
        'Distance(mi)': 'Distance',
        'Location_ID**': 'Location_ID',
        'Feature_ID*': 'Feature_ID',
        'Weather_ID**': 'Weather_ID'
    })
    
    # Verificar consistência dos IDs
    min_length = min(len(df), len(location_ids), len(weather_ids), len(feature_ids))
    if min_length < len(df):
        print(f"Aviso: Ajustando para {min_length} registros devido a IDs relacionados insuficientes")
        df = df.head(min_length)
        location_ids = location_ids[:min_length]
        weather_ids = weather_ids[:min_length]
        feature_ids = feature_ids[:min_length]
    
    # Atribuir IDs - numéricos simples começando em 1
    df['id'] = range(1, len(df) + 1)
    
    # Preencher IDs relacionados
    df['Location_ID'] = [location_ids[i] if i < len(location_ids) else None for i in range(len(df))]
    df['Weather_ID'] = [weather_ids[i] if i < len(weather_ids) else None for i in range(len(df))]
    df['Feature_ID'] = [feature_ids[i] if i < len(feature_ids) else None for i in range(len(df))]
    
    # Limpar e converter distância
    df['Distance'] = df['Distance'].apply(clean_distance)
    
    # Converter distância para metros (se necessário)
    df['Distance'] = df['Distance'].apply(lambda x: round(float(x) * 1609.34, 2) if pd.notna(x) else None)
    
    # Gerar SQL
    with open(PATHS['accidents_output'], "w", encoding="utf-8") as f:
        f.write("-- INSERT statements for ACCIDENTS table\n")
        f.write("-- Generated from filtered accidents data\n\n")
        f.write("INSERT INTO ACCIDENTS (\n")
        f.write("    id, Severity, Start_Time, End_Time, Distance, \n")
        f.write("    Description, Year, Weather_ID, Location_ID, Feature_ID\n) VALUES\n")
        
        values = []
        for _, row in df.iterrows():
            values.append(
                f"({format_sql_value(row['id'], 'number')}, "
                f"{format_sql_value(row['Severity'], 'number')}, "
                f"{format_sql_value(row['Start_Time'], 'timestamp')}, "
                f"{format_sql_value(row['End_Time'], 'timestamp')}, "
                f"{format_sql_value(row['Distance'], 'number')}, "
                f"{format_sql_value(row['Description'], 'string')}, "
                f"{format_sql_value(row['Year'], 'year')}, "
                f"{format_sql_value(row['Weather_ID'], 'string')}, "
                f"{format_sql_value(row['Location_ID'], 'string')}, "
                f"{format_sql_value(row['Feature_ID'], 'string')})"
            )
        
        # Escrever em blocos de 500 para evitar linhas muito longas
        for i in range(0, len(values), 500):
            block = values[i:i+500]
            f.write(",\n".join(block))
            f.write(";\n" if i+500 >= len(values) else ",\n")
            
    print(f"\nArquivo SQL gerado com sucesso: {PATHS['accidents_output']}")
    print(f"Total de registros: {len(df)}")
    print("\nResumo de IDs relacionados:")
    print(f"- Locations: {df['Location_ID'].notnull().sum()} válidos (ex: {df['Location_ID'].iloc[0]})")
    print(f"- Weather: {df['Weather_ID'].notnull().sum()} válidos (ex: {df['Weather_ID'].iloc[0]})")
    print(f"- Road Features: {df['Feature_ID'].notnull().sum()} válidos (ex: {df['Feature_ID'].iloc[0]})")

except Exception as e:
    print(f"Erro durante o processamento: {str(e)}")