import csv

# 1. Acesse os CSVs
arquivo_repetido = r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\lixo\repetidos_com_nomes.csv'
arquivo_corrigido = r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\lixo\AIRPORTS _CORRIGIDO.csv'
saida_filtrada = r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\airports\AIRPORTS_COM_NOME.csv'
saida_indices = r'C:\Users\leolo\OneDrive\Documentos\Faculdade\Mundo2\airports\indices_sem_nome.txt'

# Passo 1: Criar dicionário com nomes dos aeroportos
nomes_por_codigo = {}

with open(arquivo_repetido, newline='', encoding='utf-8') as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        codigo = linha['Airport_Code']
        nome = linha['Airport_Name'].strip()
        if nome:
            nomes_por_codigo[codigo] = nome

# Passo 2: Ler AIRPORTS_CORRIGIDO.csv e filtrar/remover os sem nome
linhas_filtradas = []
indices_removidos = []

with open(arquivo_corrigido, newline='', encoding='utf-8') as f:
    leitor = list(csv.DictReader(f))
    cabecalho = leitor[0].keys() if leitor else []

    for i, linha in enumerate(leitor):
        codigo = linha['Airport_Code']
        # Verifica se temos o nome no dicionário ou se já existe na linha
        if codigo in nomes_por_codigo:
            linha['Airport_Name'] = nomes_por_codigo[codigo]
            linhas_filtradas.append(linha)
        elif 'Airport_Name' in linha and linha['Airport_Name'].strip():
            linhas_filtradas.append(linha)
        else:
            indices_removidos.append(i)

# Passo 3: Escrever novo CSV com nomes completos
with open(saida_filtrada, 'w', newline='', encoding='utf-8') as f:
    escritor = csv.DictWriter(f, fieldnames=cabecalho)
    escritor.writeheader()
    escritor.writerows(linhas_filtradas)

# Passo 4: Salvar os índices dos aeroportos sem nome
with open(saida_indices, 'w') as f:
    for indice in indices_removidos:
        f.write(f"{indice}\n")

print(f"Processamento concluído! {len(linhas_filtradas)} aeroportos com nome, {len(indices_removidos)} removidos por falta de nome.")