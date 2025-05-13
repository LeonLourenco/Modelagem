import csv
from collections import defaultdict

def encontrar_combinacoes_repetidas(caminho_entrada, caminho_saida, coluna1, coluna2):
    contador = defaultdict(int)
    
    # Ler o arquivo e contar as ocorrências
    with open(caminho_entrada, mode='r') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            combinacao = (linha[coluna1], linha[coluna2])
            contador[combinacao] += 1

    # Filtrar apenas as combinações repetidas
    repetidos = {k: v for k, v in contador.items() if v > 1}
    total_repetidos = len(repetidos)

    # Escrever os resultados no arquivo de saída
    with open(caminho_saida, mode='w', newline='') as arquivo_saida:
        escritor = csv.writer(arquivo_saida)
        escritor.writerow(['Airport_Code', 'Timezone', 'Ocorrencias'])
        
        for combo, quantidade in sorted(repetidos.items()):
            escritor.writerow([combo[0], combo[1], quantidade])

    return total_repetidos, sum(repetidos.values()) - total_repetidos

# Configurações
caminho_csv = 'airports\AIRPORTS _CORRIGIDO.csv'  # Arquivo de entrada
arquivo_saida = 'repetidos.csv' # Arquivo de saída
coluna1 = 'Airport_Code'
coluna2 = 'Timezone'

# Processar o arquivo
total_combinacoes, total_repeticoes = encontrar_combinacoes_repetidas(
    caminho_csv, arquivo_saida, coluna1, coluna2
)

# Exibir resultados
print(f"\nRelatório de combinações repetidas:")
print(f"- Total de combinações diferentes que se repetem: {total_combinacoes}")
print(f"- Total de ocorrências repetidas: {total_repeticoes}")
print(f"- Arquivo com detalhes salvo em: {arquivo_saida}")

# Mostrar conteúdo do arquivo gerado (opcional)
print("\nConteúdo do arquivo gerado:")
with open(arquivo_saida, mode='r') as arquivo:
    print(arquivo.read())