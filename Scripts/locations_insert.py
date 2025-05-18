import pandas as pd
from paths import PATHS 

# 1. Função para carregar códigos de aeroporto
def load_airport_codes(path):
    try:
        df_airports = pd.read_csv(path)
        return dict(enumerate(df_airports['Airport_Code'].tolist(), start=1))
    except FileNotFoundError:
        print(f"Aviso: Arquivo {path} não encontrado. Airport_Code será NULL.")
        return {}

# Configuração de caminhos via config_paths
input_path = PATHS['locations_input']
output_path = PATHS['locations_insert']
airport_codes_path = PATHS['airport_events']

try:
    # 2. Carregar e preparar dados
    df_locations = pd.read_csv(input_path, skiprows=2, header=None, names=[
        "Original_ID", "Street", "City", "County", "State", 
        "Zipcode", "Country", "Airport_Code"
    ]).fillna("NULL").apply(lambda x: x.astype(str).str.strip())

    # 3. Adicionar ID sequencial
    df_locations["id"] = range(1, len(df_locations) + 1)

    # 4. Mapear Airport_Codes
    airport_map = load_airport_codes(airport_codes_path)
    df_locations['Airport_Code'] = df_locations['id'].map(
        lambda x: airport_map.get(x, "NULL")
    )

    # 5. Formatar Zipcodes
    df_locations['Zipcode'] = df_locations['Zipcode'].str.replace(r'-\d+$', '', regex=True)

    # 6. Gerar SQL no formato especificado
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("-- INSERT statements for LOCATIONS table\n")
        f.write(f"-- Total records: {len(df_locations)}\n\n")
        f.write("INSERT INTO location (id, Street, City, County, State, Zipcode, Country, Airport_Code) VALUES\n")
        
        # Função para formatar valores SQL
        def sql_val(x):
            if x == "NULL":
                return "NULL"
            try:
                float(x)  # Testa se é número
                return x
            except ValueError:
                return f"'{x.replace("'", "''")}'"
        
        # Gerar todos os valores
        values = []
        for _, row in df_locations.iterrows():
            values.append(
                f"({row['id']}, {sql_val(row['Street'])}, {sql_val(row['City'])}, "
                f"{sql_val(row['County'])}, {sql_val(row['State'])}, "
                f"{sql_val(row['Zipcode'])}, {sql_val(row['Country'])}, "
                f"{sql_val(row['Airport_Code'])})"
            )
        
        f.write(",\n".join(values))
        f.write(";\n")

    # Relatório final
    print(f"Arquivo gerado: {output_path}")
    print(f"Total de registros: {len(df_locations)}")
    print(f"Airport_Codes atribuídos: {sum(df_locations['Airport_Code'] != 'NULL')}")

except Exception as e:
    print(f"Erro: {e}")