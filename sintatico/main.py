import os



directory = f'{os.getcwd()}/files'


lista = []

for file in (os.listdir(directory)):
    with open(f'{directory}/{file}','r') as f:
        lines = f.readlines()
        for line in lines:
            valor = line.split(",")[1].strip()
            lista.append(valor)

''''bloco = False
abreChave = False
for i in lista:
    if bloco == True:
        if i == "{":
            abreChave = True
            if abreChave == False:
                abreChave = True
            elif abreChave == True:
                print("erro! esperava }")
                abreChave = False
        elif i == "}":
            if abreChave == True:
                abreChave = False 
                print("sucesso")
    if i == "const":
        bloco = True'''
            

