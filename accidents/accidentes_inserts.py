import pandas as pd
import re
from pathlib import Path

def extract_ids_from_sql(file_path):
    """Extrai IDs de um arquivo SQL com múltiplos INSERTs por linha"""
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Verifica se a linha contém tuplas de inserção
                if line.startswith("(") or line.startswith("INSERT INTO"):
                    # Extrai todas as tuplas da linha (cada uma entre parênteses)
                    matches = re.findall(r'\(([^)]+)\)', line)
                    for match in matches:
                        fields = match.split(",")
                        if fields:
                            id_value = fields[0].strip()
                            # Tenta converter para int
                            if id_value.isdigit():
                                ids.append(int(id_value))
        return ids
    except FileNotFoundError:
        print(f"Aviso: Arquivo {file_path} não encontrado.")
        return None


def safe_numeric_conversion(value):
    """Converte valores para numéricos de forma segura, lidando com formatos com ponto como separador de milhar"""
    if pd.isna(value) or value == "NULL" or str(value).strip() == "":
        return "NULL"
    try:
        # Remove separadores de milhar e converte vírgula decimal
        clean_value = str(value).strip().replace('.', '').replace(',', '.')
        if '.' in clean_value:
            return float(clean_value)
        return int(clean_value)
    except ValueError:
        return "NULL"

def format_sql_value(value):
    """Formata valores para o SQL, tratando strings, números e NULLs"""
    if value == "NULL" or pd.isna(value):
        return "NULL"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return f"'{str(value).replace("'", "''")}'"

# 1. Configuração de caminhos
base_path = Path(r"C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2")
input_csv = base_path / "accidents" / "ACCIDENTS_filtrado.csv"
output_sql = base_path / "accidents" / "accidents_inserts.sql"

# 2. Carregar os IDs das tabelas relacionadas
locations_sql = base_path / "locations" / "locations_inserts.sql"
weather_sql = base_path / "weather" / "weather_inserts.sql"
features_sql = base_path / "road_features" / "road_features_inserts.sql"

location_ids = extract_ids_from_sql(locations_sql)
weather_ids = extract_ids_from_sql(weather_sql)
feature_ids = extract_ids_from_sql(features_sql)

if location_ids is None or weather_ids is None or feature_ids is None:
    print("Erro: Não foi possível carregar todos os arquivos de IDs necessários.")
    exit()

# 3. Carregar o CSV de acidentes (sem definir o tipo de Distance aqui)
try:
    df = pd.read_csv(input_csv, dtype={
        'Accident_ID': 'Int64',
        'Severity': 'Int64',
        'Start_Time': 'str',
        'End_Time': 'str',
        'Description': 'str',
        'Location_ID': 'Int64',
        'Weather_ID': 'Int64',
        'Year': 'Int64'
    })
except FileNotFoundError:
    print(f"Erro: Arquivo {input_csv} não encontrado.")
    exit()

# 4. Limpeza dos dados
df = df.where(pd.notnull(df), None)

# 5. Gerar Accident_ID sequencial (se não existir)
if "Accident_ID" not in df.columns:
    print("Coluna 'Accident_ID' não encontrada. Criando IDs sequenciais.")
    df["Accident_ID"] = range(1, len(df) + 1)
else:
    # Preencher com valores sequenciais apenas se estiverem ausentes
    if pd.isna(df["Accident_ID"].iloc[0]) or df["Accident_ID"].iloc[0] == "":
        df["Accident_ID"] = range(1, len(df) + 1)

# 6. Atribuir IDs das tabelas relacionadas
if len(location_ids) < len(df):
    print(f"Aviso: Menos Location IDs ({len(location_ids)}) que acidentes ({len(df)}). Preenchendo com NULL.")
    location_ids.extend([None] * (len(df) - len(location_ids)))
if len(weather_ids) < len(df):
    print(f"Aviso: Menos Weather IDs ({len(weather_ids)}) que acidentes ({len(df)}). Preenchendo com NULL.")
    weather_ids.extend([None] * (len(df) - len(weather_ids)))
if len(feature_ids) < len(df):
    print(f"Aviso: Menos Feature IDs ({len(feature_ids)}) que acidentes ({len(df)}). Preenchendo com NULL.")
    feature_ids.extend([None] * (len(df) - len(feature_ids)))

df['Location_ID'] = location_ids[:len(df)]
df['Weather_ID'] = weather_ids[:len(df)]
df['Feature_ID'] = feature_ids[:len(df)]

# 7. Converter campos para formato SQL válido
df["Start_Time"] = df["Start_Time"].apply(lambda x: format_sql_value(x))
df["End_Time"] = df["End_Time"].apply(lambda x: format_sql_value(x))
df["Description"] = df["Description"].apply(lambda x: format_sql_value(x))

# 8. Tratar campos numéricos
numeric_cols = ["Severity", "Distance(mi)", "Year"]
for col in numeric_cols:
    df[col] = df[col].apply(safe_numeric_conversion)

# 9. Gerar arquivo SQL no formato correto para Workbench
with open(output_sql, "w", encoding="utf-8") as f:
    f.write("-- INSERT statements for ACCIDENTS table\n")
    f.write(f"-- Total records: {len(df)}\n\n")
    f.write("INSERT INTO accidents (id, Severity, Start_Time, End_Time, Distance, Description, Year, Weather_ID, Location_ID, Feature_ID) VALUES\n")
    
    values = []
    for _, row in df.iterrows():
        values.append(
            f"({format_sql_value(row['Accident_ID'])}, "
            f"{format_sql_value(row['Severity'])}, "
            f"{format_sql_value(row['Start_Time'])}, "
            f"{format_sql_value(row['End_Time'])}, "
            f"{format_sql_value(row['Distance(mi)'])}, "
            f"{format_sql_value(row['Description'])}, "
            f"{format_sql_value(row['Year'])}, "
            f"{format_sql_value(row['Weather_ID'])}, "
            f"{format_sql_value(row['Location_ID'])}, "
            f"{format_sql_value(row['Feature_ID'])})"
        )
    
    block_size = 500
    for i in range(0, len(values), block_size):
        block = values[i:i+block_size]
        f.write(",\n".join(block))
        if i+block_size < len(values):
            f.write(",\n")
        else:
            f.write(";\n")

print(f"\nResumo da geração:")
print(f"Total de registros processados: {len(df)}")
print(f"Location_IDs atribuídos: {sum(pd.notna(df['Location_ID']))}")
print(f"Weather_IDs atribuídos: {sum(pd.notna(df['Weather_ID']))}")
print(f"Feature_IDs atribuídos: {sum(pd.notna(df['Feature_ID']))}")
print(f"Arquivo gerado em: {output_sql}")
