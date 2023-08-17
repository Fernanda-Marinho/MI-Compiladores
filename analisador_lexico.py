reservadas = ["variables","const", "class", "methods", "objects", "main", "return", "if", "else", "then", "for","read", "print", "void", "int", "real", "boolean", "string", "true", "false"]
digito = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
letra = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y","z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L","M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
aritmeticos = ["+", "-", "/", "*", "++", "--"]
relacionais = ["!=", "==", "<", "<=", ">", ">=", "="]
logicos = ["!", "&&", "||"]
delimitadores = [";", ",", ".", "(", ")", "[", "]", "{", "}", "->"]
espaco = [" ", "\t","\n"]

'''entrada: handler de arquivo
    saida: lista com tokens identificados e erros
'''
def leitura (arquivo):
    acumulador = ''
    tokens = []
    n_linha = 0
    cont = 0 
    for linha in arquivo.read(): 
        n_linha +=1
        for char in linha: 
            if char == "-":
                if acumulador:
                    if acumulador[0] in letra:
                        if acumulador in reservadas:
                            token = dict(linha=n_linha, PRE=acumulador)
                            tokens.append(token)
                        else:
                            token = dict(linha=n_linha, IDE=acumulador)
                            tokens.append(token)
                        acumulador = ''
                        acumulador += char
                else: 
                    acumulador += char
            elif char == ">":
                print(f"acumulador -> {acumulador}")
                if acumulador == "-":
                    acumulador += char 
                    token = dict(linha=n_linha, DEL=acumulador)
                    tokens.append(token)
                    acumulador = ''
            elif char in letra:
                acumulador += char 
            elif char in espaco:
                if acumulador:
                    if acumulador in reservadas:
                        token = dict(linha=n_linha, PRE=acumulador)
                        tokens.append(token)
                    else:
                        token = dict(linha=n_linha, IDE=acumulador)
                        tokens.append(token)
                    acumulador = ''
            elif char in delimitadores:
                if acumulador:
                    token = dict(linha=n_linha, IDE=acumulador)
                    tokens.append(token)
                    acumulador = char
                    token = dict(linha=n_linha, DEL=acumulador)
                    tokens.append(token)
                else:
                    acumulador += char
                    token = dict(linha=n_linha, DEL=acumulador)
                    tokens.append(token)
                acumulador = ''


            else:
                acumulador += char
    for i in tokens:
        print(i)

file = open('teste.txt')

leitura(file)