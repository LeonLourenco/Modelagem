import pandas as pd

# Carrega o CSV da tabela WEATHER, ignorando as duas primeiras linhas (nome da tabela e cabeçalhos com *)
df = pd.read_csv("weather\WEATHER_filtrado.csv", skiprows=2, header=None, names=[
    "Weather_Timestamp", "Temperature", "Humidity", "Pressure",
    "Visibility", "Wind_Direction", "Wind_Speed",
    "Precipitation", "Weather_Condition_ID", "Day_Period_ID"
])

# Limpa espaços em branco e trata dados faltantes
df = df.fillna("NULL")
df = df.apply(lambda x: x.astype(str).str.strip())

# Lê os arquivos EVENTS para obter os IDs corretos baseados na posição
with open("weather_conditions\weather_events_inserts.sql", "r", encoding="utf-8") as f:
    weather_event_ids = [
        int(line.split("VALUES")[1].split(",")[1].strip().rstrip(");"))
        for line in f.readlines()
    ]

with open("day_periods\period_events_inserts.sql", "r", encoding="utf-8") as f:
    period_event_ids = [
        int(line.split("VALUES")[1].split(",")[1].strip().rstrip(");"))
        for line in f.readlines()
    ]

# Atribui os IDs estrangeiros para cada linha
df["Weather_Condition_ID"] = weather_event_ids
df["Day_Period_ID"] = period_event_ids
df.insert(0, "Weather_ID", range(1, len(df) + 1))

# Gera o script de INSERTs
with open("weather_inserts.sql", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        # Converte NULLs de string para valor nulo SQL
        def sql_val(x): return "NULL" if x == "NULL" else f"'{x}'" if not x.replace('.', '', 1).isdigit() else x
        f.write(
            f"INSERT INTO WEATHER (Weather_ID, Weather_Timestamp, Temperature, Humidity, Pressure, "
            f"Visibility, Wind_Direction, Wind_Speed, Precipitation, Weather_Condition_ID, Day_Period_ID) "
            f"VALUES ({row['Weather_ID']}, {sql_val(row['Weather_Timestamp'])}, {sql_val(row['Temperature'])}, "
            f"{sql_val(row['Humidity'])}, {sql_val(row['Pressure'])}, {sql_val(row['Visibility'])}, "
            f"{sql_val(row['Wind_Direction'])}, {sql_val(row['Wind_Speed'])}, {sql_val(row['Precipitation'])}, "
            f"{row['Weather_Condition_ID']}, {row['Day_Period_ID']});\n"
        )

print("Arquivo weather_inserts.sql gerado com sucesso.")
