import pandas as pd
import os
from pathlib import Path

# Configuração de caminhos
base_path = Path(r"C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2")
input_path = base_path / "weather" / "WEATHER_filtrado.csv"
output_path = base_path / "weather" / "weather_inserts.sql"
weather_events_path = base_path / "weather_conditions" / "weather_events_inserts.sql"
period_events_path = base_path / "day_periods" / "period_events_inserts.sql"

# Carrega o CSV da tabela WEATHER, ignorando as duas primeiras linhas
try:
    df = pd.read_csv(input_path, skiprows=2, header=None, names=[
        "Weather_Timestamp", "Temperature", "Humidity", "Pressure",
        "Visibility", "Wind_Direction", "Wind_Speed",
        "Precipitation", "Weather_Condition_ID", "Day_Period_ID"
    ])
    
    # Limpa espaços em branco e trata dados faltantes
    df = df.fillna("NULL")
    df = df.apply(lambda x: x.astype(str).str.strip())

    # Lê os arquivos EVENTS para obter os IDs corretos baseados na posição
    try:
        with open(weather_events_path, "r", encoding="utf-8") as f:
            weather_event_ids = [
                int(line.split("VALUES")[1].split(",")[1].strip().rstrip(");"))
                for line in f.readlines() if line.startswith("INSERT")
            ]

        with open(period_events_path, "r", encoding="utf-8") as f:
            period_event_ids = [
                int(line.split("VALUES")[1].split(",")[1].strip().rstrip(");"))
                for line in f.readlines() if line.startswith("INSERT")
            ]
    except Exception as e:
        print(f"Erro ao ler arquivos de eventos: {e}")
        exit()

    # Verifica se o número de IDs corresponde ao número de linhas
    if len(weather_event_ids) != len(df) or len(period_event_ids) != len(df):
        print(f"Erro: Número de IDs não corresponde ao número de linhas no CSV")
        print(f"Weather IDs: {len(weather_event_ids)}, Period IDs: {len(period_event_ids)}, CSV Rows: {len(df)}")
        exit()

    # Atribui os IDs estrangeiros para cada linha
    df["Weather_Condition_ID"] = weather_event_ids
    df["Day_Period_ID"] = period_event_ids
    df.insert(0, "Weather_ID", range(1, len(df) + 1))

    # Gera o script de INSERTs em um único comando
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("-- INSERT statements for WEATHER table\n")
        f.write("-- Generated automatically from WEATHER_filtrado.csv\n\n")
        
        f.write("INSERT INTO WEATHER (Weather_ID, Weather_Timestamp, Temperature, Humidity, Pressure, ")
        f.write("Visibility, Wind_Direction, Wind_Speed, Precipitation, Weather_Condition_ID, Day_Period_ID) VALUES\n")
        
        # Função para converter valores para formato SQL
        def sql_val(x):
            if x == "NULL":
                return "NULL"
            try:
                # Tenta converter para float (para números com decimais)
                float_val = float(x)
                return str(float_val)
            except ValueError:
                # Se não for número, trata como string
                return f"'{x.replace("'", "''")}'"
        
        # Gera todos os valores em um único bloco
        values = []
        for _, row in df.iterrows():
            values.append(
                f"({row['Weather_ID']}, {sql_val(row['Weather_Timestamp'])}, {sql_val(row['Temperature'])}, "
                f"{sql_val(row['Humidity'])}, {sql_val(row['Pressure'])}, {sql_val(row['Visibility'])}, "
                f"{sql_val(row['Wind_Direction'])}, {sql_val(row['Wind_Speed'])}, {sql_val(row['Precipitation'])}, "
                f"{row['Weather_Condition_ID']}, {row['Day_Period_ID']})"
            )
        
        f.write(",\n".join(values))
        f.write(";\n")

    print(f"Arquivo {output_path} gerado com sucesso.")
    print(f"Total de registros inseridos: {len(df)}")

except Exception as e:
    print(f"Erro no processamento: {e}")