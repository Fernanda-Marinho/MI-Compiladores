import os
from mef import analisar_lexico

# executar analise lexica
analisar_lexico()

# gerar coleção de tokens [lista de dicionarios]

directory = f'{os.getcwd()}/testes'
############ função para gerar lista de tokens a partir do arquivo
def get_token_collection():
    for file_path in (os.listdir(directory)):
        if ((not (file_path.endswith('-saida.txt') or file_path.endswith('-saida0.txt'))) or not file_path.endswith(".txt")): 
            continue
        token_collection = []
        with open(f'{directory}/{file_path}','r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = line.split(' ')
                if (len(line) < 2): break
                token = dict(
                    n_line = line[0],
                    token_class = line[1],
                    token_text = line[2]
                )
                token_collection.append(token)
    return token_collection

# print(get_token_collection())

# TODO chamada do analisador sintatico
# sintatico.analisar_sintatico(get_token_collection)
