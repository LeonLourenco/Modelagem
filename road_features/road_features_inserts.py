import pandas as pd
from config_paths import PATHS

def extract_ids_from_sql(file_path):
    """Extrai IDs de um arquivo SQL de INSERTs"""
    ids = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "INSERT INTO" in line and "VALUES" in line:
                    # Extrai valores entre parênteses
                    values_part = line.split("VALUES")[1].strip()
                    records = [r.strip() for r in values_part.replace("(", "").split("),") if r.strip()]
                    for record in records:
                        first_value = record.split(",")[0].strip().replace("'", "")
                        if first_value.isdigit():
                            ids.append(int(first_value))
        return ids
    except FileNotFoundError:
        print(f"Aviso: Arquivo {file_path} não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao processar arquivo SQL: {e}")
        return []

# Configuração de caminhos
input_csv = PATHS['road_features_input']
output_sql = PATHS['road_features_output']
accidents_sql = PATHS['accidents_output']

# Carregar dados do CSV
try:
    df = pd.read_csv(
        input_csv,
        skiprows=2,
        header=None,
        names=[
            "id", "Accident_ID", "Amenity", "Bump", "Crossing", 
            "Give_Way", "Junction", "No_Exit", "Railway", "Roundabout", 
            "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
        ],
        dtype='str'
    )
    
    # Limpeza dos dados
    df = df.fillna("NULL").apply(lambda x: x.str.strip())
    
    # Carregar Accident_IDs do arquivo SQL
    accident_ids = extract_ids_from_sql(accidents_sql)
    if accident_ids:
        if len(accident_ids) < len(df):
            print(f"Aviso: Menos acidentes ({len(accident_ids)}) que features ({len(df)}). Ajustando...")
            df = df.head(len(accident_ids))
        df["Accident_ID"] = accident_ids[:len(df)]
    else:
        print("Aviso: Usando IDs do CSV")
        df["Accident_ID"] = range(1, len(df) + 1)

    # Processar colunas booleanas (convertendo para TINYINT 0/1)
    bool_cols = ["Amenity", "Bump", "Crossing", "Give_Way", "Junction", 
                "No_Exit", "Railway", "Roundabout", "Station", "Stop", 
                "Traffic_Calming", "Traffic_Signal", "Turning_Loop"]
    
    for col in bool_cols:
        df[col] = df[col].apply(
            lambda x: 1 if str(x).upper() in ["TRUE", "T", "1", "YES", "Y"] else
                    0 if str(x).upper() in ["FALSE", "F", "0", "NO", "N"] else
                    "NULL"
        )

    # Gerar IDs sequenciais se não existirem
    if df["id"].iloc[0] == "NULL":
        df["id"] = range(1, len(df) + 1)

    # Gerar arquivo SQL
    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("-- INSERT statements for ROAD_FEATURES table\n")
        f.write(f"-- Total records: {len(df)}\n\n")
        f.write("INSERT INTO ROAD_FEATURES (id, Avenue, Bump, Crossing, Give_Way, ")
        f.write("Junction, No_Exit, Railway, Roundabout, Station, Stop, ")
        f.write("Traffic_Calming, Traffic_Signal, Turning_Loop) VALUES\n")
        
        # Gerar linhas de valores
        rows = []
        for _, row in df.iterrows():
            values = [
                str(row['id']),  # ID
                "0",  # Avenue (não presente no CSV)
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
        
        # Escrever em blocos de 500
        for i in range(0, len(rows), 500):
            block = rows[i:i+500]
            f.write(",\n".join(block))
            f.write(";\n" if i+500 >= len(rows) else ",\n")

    print(f"Arquivo {output_sql} gerado com {len(df)} registros.")

except Exception as e:
    print(f"Erro durante o processamento: {str(e)}")
    