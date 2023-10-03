import os



directory = f'{os.getcwd()}/files'


lista = []

for file in (os.listdir(directory)):
    with open(f'{directory}/{file}','r') as f:
        lines = f.readlines()
        for line in lines:
            valor = line.split(",")[1].strip()
            lista.append(valor)

bloco = False
fechaChave = False
possivel_bloco = False 
erroBloco = False
contador = -1
for i in lista:
    contador += 1
    if i == "const":
        if lista[contador+1] == "{":
            possivel_bloco = True
        else: 
            print("Erro. Esperava { e recebeu",lista[contador+1])
    elif i == "variables": 
        if lista[contador+1] == "{":
            possivel_bloco = True 
    elif i == "{":
        bloco = True 
    
    if bloco == True:  #aguardando um fecha chave 
        if i == "}":
            fechaChave = True
        elif i == "variables":
            if fechaChave == False:
                print("Erro. Esperava } e recebeu",i) #TODO como fazer printar a linha
                bloco = False 
    