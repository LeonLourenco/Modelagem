import pandas as pd
import re
from pathlib import Path

def extract_ids_from_sql(file_path, id_column_name):
    """Extrai IDs de um arquivo SQL de INSERTs"""
    id_pattern = re.compile(rf"INSERT INTO \w+ \({id_column_name},.*?VALUES \((\d+)")
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = id_pattern.search(line)
                if match:
                    ids.append(int(match.group(1)))
        return ids
    except FileNotFoundError:
        print(f"Aviso: Arquivo {file_path} não encontrado. Usando NULL para {id_column_name}.")
        return []

def safe_numeric_conversion(value):
    """Converte valores para numéricos de forma segura"""
    if value == "NULL":
        return "NULL"
    try:
        # Remove pontos de milhar se existirem
        clean_value = str(value).replace('.', '')
        if '.' in clean_value:  # Se ainda tiver ponto decimal
            return float(clean_value)
        return int(clean_value)
    except ValueError:
        return "NULL"

# 1. Configuração de caminhos (usando Path para evitar problemas com barras)
base_path = Path(r"C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2")
input_csv = base_path / "accidents" / "ACCIDENTS_filtrado.csv"
output_sql = base_path / "accidents" / "accidents_inserts.sql"
weather_sql = base_path / "weather" / "weather_inserts.sql"
locations_sql = base_path / "locations" / "locations_inserts.sql"

# 2. Carregar os IDs das tabelas relacionadas
weather_ids = extract_ids_from_sql(weather_sql, "Weather_ID")
location_ids = extract_ids_from_sql(locations_sql, "Location_ID")

# 3. Carregar o CSV de acidentes
df = pd.read_csv(input_csv, skiprows=1, header=None, names=[
    "Accident_ID", "Severity", "Start_Time", "End_Time", "Distance(mi)",
    "Description", "Location_ID", "Weather_ID", "Year"
])

# 4. Limpeza dos dados
df = df.fillna("NULL")
df = df.apply(lambda x: x.astype(str).str.strip())

# 5. Gerar Accident_ID sequencial (se não existir)
if df["Accident_ID"].iloc[0] == "NULL":
    df["Accident_ID"] = range(1, len(df) + 1)

# 6. Atribuir Weather_ID e Location_ID sequencialmente
for i in range(len(df)):
    df.at[i, 'Weather_ID'] = weather_ids[i] if i < len(weather_ids) else "NULL"
    df.at[i, 'Location_ID'] = location_ids[i] if i < len(location_ids) else "NULL"

# 7. Converter campos de data para formato SQL válido
df["Start_Time"] = df["Start_Time"].apply(lambda x: f"'{x}'" if x != "NULL" else "NULL")
df["End_Time"] = df["End_Time"].apply(lambda x: f"'{x}'" if x != "NULL" else "NULL")

# 8. Tratar campos numéricos com conversão segura
numeric_cols = ["Severity", "Distance(mi)", "Year"]
for col in numeric_cols:
    df[col] = df[col].apply(safe_numeric_conversion)

# 9. Gerar arquivo SQL
with open(output_sql, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        def format_value(val):
            if val == "NULL":
                return "NULL"
            elif isinstance(val, (int, float)):
                return str(val)
            else:
                return f"'{val}'"
        
        f.write(
            "INSERT INTO ACCIDENTS (Accident_ID, Severity, Start_Time, End_Time, "
            "Distance_mi, Description, Location_ID, Weather_ID, Year) VALUES ("
            f"{format_value(row['Accident_ID'])}, {format_value(row['Severity'])}, "
            f"{row['Start_Time']}, {row['End_Time']}, "
            f"{format_value(row['Distance(mi)'])}, {format_value(row['Description'])}, "
            f"{format_value(row['Location_ID'])}, {format_value(row['Weather_ID'])}, "
            f"{format_value(row['Year'])});\n"
        )

print(f"Arquivo {output_sql} gerado com {len(df)} registros.")
print(f"Location_IDs atribuídos: {sum(df['Location_ID'] != 'NULL')}")
print(f"Weather_IDs atribuídos: {sum(df['Weather_ID'] != 'NULL')}")