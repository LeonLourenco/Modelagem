import pandas as pd

# Carrega o arquivo com os nomes dos aeroportos
repetidos_df = pd.read_csv('repetidos_com_nomes.csv')

# Filtra os códigos que não têm nome associado (NaN ou string vazia)
missing_names = repetidos_df[repetidos_df['Airport_Name'].isna() | (repetidos_df['Airport_Name'] == '')]

# Se quiser apenas os códigos sem nome:
missing_codes = missing_names['Airport_Code'].unique()

print("Códigos de aeroporto sem nome encontrado:")
print(missing_codes)

# Opcional: salva em um novo arquivo CSV
missing_names.to_csv('codigos_sem_nome.csv', index=False)