import pandas as pd
from pathlib import Path

def extract_ids_from_sql(file_path):
    """Extrai IDs de um arquivo SQL de INSERTs de forma mais robusta"""
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "INSERT INTO" in line and "VALUES" in line:
                    # Extrai o primeiro valor após VALUES (que deve ser o ID)
                    first_value = line.split("VALUES")[1].split(",")[0].strip()
                    # Remove parênteses e aspas se existirem
                    clean_id = first_value.replace("(", "").replace(")", "").replace("'", "")
                    if clean_id.isdigit():
                        ids.append(int(clean_id))
        return ids
    except FileNotFoundError:
        print(f"Aviso: Arquivo {file_path} não encontrado.")
        return []

# 1. Configurar caminhos de forma segura (usando pathlib)
base_path = Path(r"C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2")
input_csv = base_path / "road_features" / "ROAD_FEATURES_filtrado.csv"
output_sql = base_path / "road_features" / "road_features_inserts.sql"
accidents_sql = base_path / "accidents" / "accidents_inserts.sql"

# 2. Carregar os dados do CSV com tipos explícitos para evitar warnings
dtype_spec = {
    0: 'object', 1: 'object', 2: 'object', 3: 'object', 4: 'object',
    5: 'object', 6: 'object', 7: 'object', 8: 'object', 9: 'object',
    10: 'object', 11: 'object', 12: 'object', 13: 'object', 14: 'object'
}

df = pd.read_csv(
    input_csv,
    skiprows=2,
    header=None,
    names=[
        "Feature_ID", "Accident_ID", "Amenity", "Bump", "Crossing", 
        "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout", 
        "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
    ],
    dtype=dtype_spec,
    low_memory=False
)

# 3. Limpeza dos dados
df = df.fillna("NULL")
df = df.apply(lambda x: x.astype(str).str.strip())

# 4. Carregar os Accident_IDs reais
try:
    accident_ids = extract_ids_from_sql(accidents_sql)
    if not accident_ids:
        print("Aviso: Nenhum Accident_ID válido encontrado no arquivo SQL. Usando IDs do CSV.")
    elif len(accident_ids) >= len(df):
        df["Accident_ID"] = accident_ids[:len(df)]
    else:
        print(f"Aviso: Há mais features ({len(df)}) do que acidentes ({len(accident_ids)}). Ajustando...")
        df = df.head(len(accident_ids))
        df["Accident_ID"] = accident_ids
except FileNotFoundError:
    print("Aviso: Arquivo de acidentes não encontrado. Usando Accident_ID do CSV.")

# 5. Processar colunas booleanas de forma mais robusta
bool_cols = ["Amenity", "Bump", "Crossing", "Give_Way", "Junction", 
             "No_Exit", "Railway", "Roundabout", "Station", "Stop", 
             "Traffic_Calming", "Traffic_Signal", "Turning_Loop"]

for col in bool_cols:
    df[col] = df[col].apply(
        lambda x: "TRUE" if str(x).upper() == "TRUE" else 
                 "FALSE" if str(x).upper() == "FALSE" else 
                 "NULL"
    )

# 6. Gerar Feature_IDs sequenciais (se não existirem)
if df["Feature_ID"].iloc[0] == "NULL":
    df["Feature_ID"] = range(1, len(df) + 1)

# 7. Gerar arquivo SQL
with open(output_sql, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        def format_sql_value(val):
            if val == "NULL":
                return "NULL"
            elif val in ["TRUE", "FALSE"]:
                return val
            elif str(val).isdigit():
                return str(val)
            else:
                return f"'{val}'"
        
        f.write(
            "INSERT INTO ROAD_FEATURES (Feature_ID, Accident_ID, Amenity, Bump, Crossing, "
            "Give_Way, Junction, No_Exit, Railway, Roundabout, Station, Stop, "
            "Traffic_Calming, Traffic_Signal, Turning_Loop) VALUES ("
            f"{format_sql_value(row['Feature_ID'])}, {format_sql_value(row['Accident_ID'])}, "
            f"{format_sql_value(row['Amenity'])}, {format_sql_value(row['Bump'])}, "
            f"{format_sql_value(row['Crossing'])}, {format_sql_value(row['Give_Way'])}, "
            f"{format_sql_value(row['Junction'])}, {format_sql_value(row['No_Exit'])}, "
            f"{format_sql_value(row['Railway'])}, {format_sql_value(row['Roundabout'])}, "
            f"{format_sql_value(row['Station'])}, {format_sql_value(row['Stop'])}, "
            f"{format_sql_value(row['Traffic_Calming'])}, {format_sql_value(row['Traffic_Signal'])}, "
            f"{format_sql_value(row['Turning_Loop'])});\n"
        )

print(f"Arquivo {output_sql} gerado com {len(df)} registros.")