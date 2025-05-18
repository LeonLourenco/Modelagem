import pandas as pd
import csv
from collections import defaultdict
from paths import PATHS

# ================= CONFIGURAÇÕES =================
ARQUIVO_AEROPORTOS = PATHS['airports_input']
DATABASE = PATHS['airports_database']
ARQUIVO_REPETIDOS = PATHS['airports_repetidos']
ARQUIVO_COM_NOMES = PATHS['repetidos_com_nomes']
ARQUIVO_FINAL = PATHS['airports_output']
ARQUIVO_INDICES = PATHS['indices_output']

OUTRAS_TABELAS = [
    PATHS['weather_conditions_input'],
    PATHS['weather_input'],
    PATHS['road_features_input'],
    PATHS['locations_input'],
    PATHS['day_periods_input'],
    PATHS['accidents_input']
]

# ================= FUNÇÃO PRINCIPAL =================
def main():
    # 1. Análise de combinações repetidas
    analisar_combinacoes_repetidas(ARQUIVO_AEROPORTOS)
    
    # 2. Adicionar nomes aos aeroportos repetidos
    adicionar_nomes_aeroportos(ARQUIVO_REPETIDOS, DATABASE)
    
    # 3. Processar arquivo principal e filtrar linhas sem nome
    indices_para_remover = processar_arquivo_principal(ARQUIVO_AEROPORTOS, ARQUIVO_COM_NOMES)
    
    # 4. Salvar índices para remover
    salvar_indices(indices_para_remover, ARQUIVO_INDICES)
    
    # 5. Filtrar outras tabelas
    for tabela_path in OUTRAS_TABELAS:
        filtrar_tabela(tabela_path, indices_para_remover)

# ================= FUNÇÕES DE PRÉ-PROCESSAMENTO =================
def analisar_combinacoes_repetidas(caminho_entrada):
    """Analisa combinações repetidas de Airport_Code e Timezone"""
    contador = defaultdict(int)
    
    with open(caminho_entrada, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            combinacao = (linha['Airport_Code'], linha['Timezone'])
            contador[combinacao] += 1

    repetidos = {k: v for k, v in contador.items() if v > 1}

    with open(ARQUIVO_REPETIDOS, mode='w', newline='', encoding='utf-8') as arquivo_saida:
        escritor = csv.writer(arquivo_saida)
        escritor.writerow(['Airport_Code', 'Timezone', 'Ocorrencias'])
        for combo, quantidade in sorted(repetidos.items()):
            escritor.writerow([combo[0], combo[1], quantidade])

    print(f"\nRelatório de combinações repetidas gerado em: {ARQUIVO_REPETIDOS}")

def adicionar_nomes_aeroportos(caminho_repetidos, caminho_original):
    """Adiciona nomes de aeroportos ao arquivo de repetidos"""
    airports_df = pd.read_csv(caminho_original)
    repetidos_df = pd.read_csv(caminho_repetidos)

    # Criar dicionários de mapeamento
    iata_to_name = dict(zip(airports_df['ident'], airports_df['name']))
    gps_to_name = dict(zip(airports_df['gps_code'], airports_df['name']))
    
    # Mapeamento manual para códigos específicos
    mapeamento_manual = {
        'K3A6': 'Pacific City State Airport',
        'KATT': 'Central City Municipal - Larry Reineke Field',
        'KCQT': 'Pacific Valley Aviation Airport',
        'KMCJ': 'Salina Municipal Airport'
    }

    def get_airport_name(code):
        # Primeiro verifica no mapeamento manual
        if code in mapeamento_manual:
            return mapeamento_manual[code]
        # Depois nos dicionários automáticos
        if code in iata_to_name:
            return iata_to_name[code]
        elif code in gps_to_name:
            return gps_to_name[code]
        return None

    # Aplicar a função para obter os nomes
    repetidos_df['Airport_Name'] = repetidos_df['Airport_Code'].apply(get_airport_name)
    
    # Identificar códigos ainda sem nome para relatório
    missing = repetidos_df[repetidos_df['Airport_Name'].isna()]
    if not missing.empty:
        print("\nCódigos de aeroporto sem nome encontrado:")
        print(missing['Airport_Code'].unique())
    
    # Salvar o arquivo com nomes
    repetidos_df.to_csv(ARQUIVO_COM_NOMES, index=False, encoding='utf-8')
    print(f"\nNomes de aeroportos adicionados em: {ARQUIVO_COM_NOMES}")

def processar_arquivo_principal(caminho_entrada, caminho_repetidos):
    """Processa o arquivo principal e retorna índices sem nome"""
    # Criar dicionário com nomes dos aeroportos
    nomes_por_codigo = {}
    
    with open(caminho_repetidos, newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            codigo = linha['Airport_Code']
            nome = linha['Airport_Name'].strip()
            if nome:
                nomes_por_codigo[codigo] = nome

    # Processar arquivo principal
    linhas_filtradas = []
    indices_removidos = []
    
    with open(caminho_entrada, newline='', encoding='utf-8') as f:
        leitor = list(csv.DictReader(f))
        cabecalho = leitor[0].keys() if leitor else []

        for i, linha in enumerate(leitor):
            codigo = linha['Airport_Code']
            if codigo in nomes_por_codigo:
                linha['Airport_Name'] = nomes_por_codigo[codigo]
                linhas_filtradas.append(linha)
            elif 'Airport_Name' in linha and linha['Airport_Name'].strip():
                linhas_filtradas.append(linha)
            else:
                indices_removidos.append(i)

    # Escrever novo CSV com nomes completos
    with open(ARQUIVO_FINAL, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=cabecalho)
        escritor.writeheader()
        escritor.writerows(linhas_filtradas)

    print(f"\nArquivo principal processado em: {ARQUIVO_FINAL}")
    print(f"Total de aeroportos removidos por falta de nome: {len(indices_removidos)}")
    
    return indices_removidos

def salvar_indices(indices, caminho_saida):
    """Salva os índices para remover em arquivo"""
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        for indice in indices:
            f.write(f"{indice}\n")
    print(f"Índices para remover salvos em: {caminho_saida}")

def filtrar_tabela(caminho_tabela, indices_remover):
    """Filtra outras tabelas removendo os índices especificados"""
    df = pd.read_csv(caminho_tabela, low_memory=False)
    nome_saida = caminho_tabela.with_name(caminho_tabela.stem + "_filtrado.csv")
    df_filtrado = df.drop(index=indices_remover, errors='ignore').reset_index(drop=True)
    df_filtrado.to_csv(nome_saida, index=False)
    print(f"Tabela '{caminho_tabela}' filtrada e salva como '{nome_saida}'")

if __name__ == "__main__":
    main()