import pandas as pd

# 1. Carregar os códigos de aeroporto do AIRPORTS_COM_NOME.csv
def load_airport_codes(csv_path):
    try:
        df_airports = pd.read_csv(csv_path)
        # Criar mapeamento: número da linha → Airport_Code
        return dict(enumerate(df_airports['Airport_Code'].tolist(), start=1))
    except FileNotFoundError:
        print(f"Aviso: Arquivo {csv_path} não encontrado. Nenhum Airport_Code será adicionado.")
        return {}

# 2. Carregar o CSV de LOCATIONS
df_locations = pd.read_csv("locations\LOCATIONS_filtrado.csv", skiprows=2, header=None, names=[
    "Location_ID_Original", "Street", "City", "County", "State", 
    "Zipcode", "Country", "Airport_Code"
])

# 3. Limpeza dos dados
df_locations = df_locations.fillna("NULL")
df_locations = df_locations.apply(lambda x: x.astype(str).str.strip())

# 4. Gerar Location_ID sequencial (1, 2, 3...)
df_locations["Location_ID"] = range(1, len(df_locations) + 1)

# 5. Carregar os códigos de aeroporto (mapeamento: número da linha → Airport_Code)
airport_codes = load_airport_codes(r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\airports\AIRPORTS_COM_NOME.csv')

# 6. Atribuir Airport_Code com base no Location_ID (se existir no mapeamento)
for index, row in df_locations.iterrows():
    location_id = row['Location_ID']
    if location_id in airport_codes:
        df_locations.at[index, 'Airport_Code'] = airport_codes[location_id]

# 7. Tratar Zipcodes (remover extensão "-XXXX" se houver)
df_locations['Zipcode'] = df_locations['Zipcode'].str.replace(r'-\d+$', '', regex=True)

# 8. Gerar arquivo SQL
with open("locations_inserts.sql", "w", encoding="utf-8") as f:
    for _, row in df_locations.iterrows():
        # Função para formatar valores SQL corretamente
        def format_sql_value(val):
            if val == "NULL":
                return "NULL"
            elif str(val).replace('.', '', 1).isdigit():
                return str(val)
            else:
                return f"'{val}'"
        
        # Monta o INSERT
        f.write(
            "INSERT INTO LOCATIONS (Location_ID, Street, City, County, State, "
            "Zipcode, Country, Airport_Code) VALUES ("
            f"{format_sql_value(row['Location_ID'])}, {format_sql_value(row['Street'])}, "
            f"{format_sql_value(row['City'])}, {format_sql_value(row['County'])}, "
            f"{format_sql_value(row['State'])}, {format_sql_value(row['Zipcode'])}, "
            f"{format_sql_value(row['Country'])}, {format_sql_value(row['Airport_Code'])});\n"
        )

print(f"Arquivo locations_inserts.sql gerado com {len(df_locations)} registros.")
print(f"Airport_Codes atribuídos: {sum(df_locations['Airport_Code'] != 'NULL')}")