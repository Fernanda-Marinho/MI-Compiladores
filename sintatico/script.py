import os
from inspections import CONSTS_BLOCK

directory = f'{os.getcwd()}/sintatico/files'

############ script para ler os tokens de uma colecao de objetos

token_collection = []
for file in (os.listdir(directory)):
    with open(f'{directory}/{file}','r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.split(' ')
            token = dict(
                n_line = line[0],
                token_class = line[1],
                token_text = line[2]
            )
            token_collection.append(token)

for token in token_collection:
    print(token)

'''
for file in (os.listdir(directory)):
    with open(f'{directory}/{file}','r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # chamar a função de inicio de analise para a linha
            # print(CONSTS_BLOCK(line))

'''
