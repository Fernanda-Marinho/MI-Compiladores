import os
from mef import analisar_lexico
from sintatico import AnaliseSintatica

# executar analise lexica
analisar_lexico()

# gerar coleção de tokens [lista de dicionarios]

directory = f'{os.getcwd()}/testes'
############ função para gerar lista de tokens a partir do arquivo
def get_token_collection():
    list = []
    for file_path in (os.listdir(directory)):
        if ((not (file_path.endswith('-saida.txt') or file_path.endswith('-saida0.txt'))) or not file_path.endswith(".txt")): 
            continue
        token_collection = []
        with open(f'{directory}/{file_path}','r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                line = line.split(' ')
                if (len(line) < 3 or line[2].startswith('//')): continue
                token = dict(
                    n_line = line[0],
                    token_class = line[1],
                    token_text = line[2]
                )
                token_collection.append(token)
                list.append(token_collection)
    return list

# print(get_token_collection())

# TODO chamada do analisador sintatico
sintatico = AnaliseSintatica(get_token_collection()[0])
sintatico.start()
# sintatico.analisar_sintatico(get_token_collection)
