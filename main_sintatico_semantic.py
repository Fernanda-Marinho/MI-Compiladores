import os
from mef import analisar_lexico
from sintatic_semantic import AnaliseSintatica
from sintatic_semantic import * 


# executar analise lexica
analisar_lexico()

# gerar coleção de tokens [lista de dicionarios]
directory = f'{os.getcwd()}/files'
"""def get_token_collection():
    list = []
    for file_path in (os.listdir(directory)):
        if ((not (file_path.endswith('-lexico.txt') or file_path.endswith('-lexico0.txt'))) or not file_path.endswith(".txt")): 
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
    return list"""

def get_token_collection(file_path):
    token_collection = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(' ')
            if len(line) < 3 or line[2].startswith('//'):
                continue
            token = dict(
                n_line=line[0],
                token_class=line[1],
                token_text=line[2]
            )
            token_collection.append(token)
    return token_collection

# print(*get_token_collection()[0], sep='\n')

"""def generate_analysis_output():
    global sintatico;
    sintatico = AnaliseSintatica(get_token_collection()[0])
    result = sintatico.start()
    success = ('A análise sintática foi concluída com sucesso =)')
    newfile = open('project_analysis_output.txt', 'w')
    if result == '': newfile.write(success)
    else: newfile.write(result)
    print(result)"""

#global erro 

def generate_analysis_output(input_file, output_file):
    sintatico = AnaliseSintatica(get_token_collection(input_file))
    result, erro = sintatico.start()
    #print(erro)
    with open(output_file, 'w') as newfile:
        if result == '':
            newfile.write('A análise sintática foi concluída com sucesso =)')
        else:
            newfile.write(result)
    return erro 
    #print(f"Análise sintática concluída para {input_file}. Resultados salvos em {output_file}")


# Iterar sobre os arquivos no diretório
for file_path in os.listdir(directory):
    if file_path.endswith('-lexico.txt') and not file_path.endswith('-saida.txt'):
        input_file = f'{directory}/{file_path}'
        output_file = f'{directory}/{file_path.replace("-lexico.txt", "-saida.txt")}'
        e = generate_analysis_output(input_file, output_file)

        with open(output_file, 'w') as newfile:
            if not e:
                newfile.write('A análise semântica foi concluída com sucesso =)')
            else:
                newfile.write('\n'.join(e))
        

#generate_analysis_output()


