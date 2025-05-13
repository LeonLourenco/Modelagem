import pandas as pd

# Carrega os arquivos CSV
airports_df = pd.read_csv(r'C:\Users\leolo\Downloads\airports.csv')
repetidos_df = pd.read_csv('repetidos.csv')

# Primeiro cria um dicionário de mapeamento entre o código IATA (ident) e o nome do aeroporto
iata_to_name = dict(zip(airports_df['ident'], airports_df['name']))

# Depois cria um dicionário de fallback usando gps_code
gps_to_name = dict(zip(airports_df['gps_code'], airports_df['name']))

# Função para buscar o nome do aeroporto com fallback
def get_airport_name(code):
    # Primeiro tenta encontrar no dicionário principal (ident)
    if code in iata_to_name:
        return iata_to_name[code]
    # Se não encontrar, tenta no dicionário de fallback (gps_code)
    elif code in gps_to_name:
        return gps_to_name[code]
    # Se não encontrar em nenhum, retorna None ou um valor padrão
    else:
        return None

# Adiciona uma nova coluna 'Airport_Name' ao dataframe repetidos_df
repetidos_df['Airport_Name'] = repetidos_df['Airport_Code'].apply(get_airport_name)

# Exibe o resultado
print(repetidos_df)

# Salva o resultado em um novo arquivo CSV, se necessário
repetidos_df.to_csv('repetidos_com_nomes.csv', index=False)