import os
from analisador_lexico import leitura

current = f'{os.getcwd()}/exemplos'
for file_path in (os.listdir(current)):
    if (file_path.endswith('-saida.txt') or not file_path.endswith(".txt")): continue
    with open(f'{current}/{file_path}', 'r') as file:
        leitura(file)
        file.close()