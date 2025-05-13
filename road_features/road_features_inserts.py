import pandas as pd
from pathlib import Path

def extract_ids_from_sql(file_path):
    """Extrai IDs de um arquivo SQL de INSERTs no formato específico dos acidentes"""
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            in_insert = False
            for line in f:
                if "INSERT INTO" in line and "VALUES" in line:
                    in_insert = True
                    # Processa a primeira linha do INSERT
                    values_part = line.split("VALUES")[1].strip()
                    records = values_part.replace("(", "").split("),")
                    for record in records:
                        if record.strip():
                            first_value = record.split(",")[0].strip().replace("'", "")
                            if first_value.isdigit():
                                ids.append(int(first_value))
                elif in_insert and line.strip().startswith("("):
                    # Processa linhas adicionais do INSERT
                    records = line.strip().replace("(", "").split("),")
                    for record in records:
                        if record.strip():
                            first_value = record.split(",")[0].strip().replace("'", "")
                            if first_value.isdigit():
                                ids.append(int(first_value))
                elif in_insert and ";" in line:
                    in_insert = False
        return ids
    except FileNotFoundError:
        print(f"Aviso: Arquivo {file_path} não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao processar arquivo SQL: {e}")
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
        "id", "Accident_ID", "Amenity", "Bump", "Crossing", 
        "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout", 
        "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
    ],
    dtype=dtype_spec,
    low_memory=False
)

# 3. Limpeza dos dados
df = df.fillna("NULL")
df = df.apply(lambda x: x.astype(str).str.strip())

# 4. Carregar os Accident_IDs reais do arquivo SQL
try:
    accident_ids = extract_ids_from_sql(accidents_sql)
    print(f"Total de Accident_IDs encontrados: {len(accident_ids)}")  # Debug
    
    if not accident_ids:
        print("Aviso: Nenhum Accident_ID válido encontrado no arquivo SQL. Usando IDs do CSV.")
    else:
        # Verificar se temos Accident_IDs suficientes
        if len(accident_ids) < len(df):
            print(f"Aviso: Há mais features ({len(df)}) do que acidentes ({len(accident_ids)}). Ajustando...")
            df = df.head(len(accident_ids))
        
        # Atribuir os IDs sequencialmente
        df["Accident_ID"] = accident_ids[:len(df)]
        
except FileNotFoundError:
    print("Aviso: Arquivo de acidentes não encontrado. Usando Accident_ID do CSV.")

# 5. Processar colunas booleanas de forma mais robusta
bool_cols = ["Amenity", "Bump", "Crossing", "Give_Way", "Junction", 
             "No_Exit", "Railway", "Roundabout", "Station", "Stop", 
             "Traffic_Calming", "Traffic_Signal", "Turning_Loop"]

for col in bool_cols:
    df[col] = df[col].apply(
        lambda x: "TRUE" if str(x).upper() in ["TRUE", "T", "1", "YES", "Y"] else 
                 "FALSE" if str(x).upper() in ["FALSE", "F", "0", "NO", "N"] else 
                 "NULL"
    )

# 6. Gerar IDs sequenciais (se não existirem)
if df["id"].iloc[0] == "NULL":
    df["id"] = range(1, len(df) + 1)

# 7. Gerar arquivo SQL
with open(output_sql, "w", encoding="utf-8") as f:
    # Escrever cabeçalho de comentários
    f.write("-- INSERT statements for ROAD_FEATURES table\n")
    f.write(f"-- Total records: {len(df)}\n\n")
    
    f.write("INSERT INTO road_features (id, Accident_ID, Amenity, Bump, Crossing, ")
    f.write("Give_Way, Junction, No_Exit, Railway, Roundabout, Station, Stop, ")
    f.write("Traffic_Calming, Traffic_Signal, Turning_Loop) VALUES\n")
    
    # Gerar todas as linhas de valores
    rows = []
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
        
        row_values = [
            format_sql_value(row['id']),
            format_sql_value(row['Accident_ID']),
            format_sql_value(row['Amenity']),
            format_sql_value(row['Bump']),
            format_sql_value(row['Crossing']),
            format_sql_value(row['Give_Way']),
            format_sql_value(row['Junction']),
            format_sql_value(row['No_Exit']),
            format_sql_value(row['Railway']),
            format_sql_value(row['Roundabout']),
            format_sql_value(row['Station']),
            format_sql_value(row['Stop']),
            format_sql_value(row['Traffic_Calming']),
            format_sql_value(row['Traffic_Signal']),
            format_sql_value(row['Turning_Loop'])
        ]
        
        rows.append(f"({', '.join(row_values)})")
    
    # Escrever todas as linhas, separadas por vírgulas
    f.write(",\n".join(rows))
    f.write(";\n")

print(f"Arquivo {output_sql} gerado com {len(df)} registros.")