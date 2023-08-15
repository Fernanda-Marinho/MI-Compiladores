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
    for linha in arquivo.read(): 
        n_linha +=1
        for char in linha:  #quando EOF ele não entra no loop
            if char.isspace() or char in espaco:    
                if acumulador in reservadas:
                    token = dict(linha=n_linha, PRE=acumulador)
                    tokens.append(token)
                elif acumulador in relacionais:
                    token = dict(linha=n_linha, REL=acumulador)
                    tokens.append(token)
                elif acumulador in logicos:
                    token = dict(linha=n_linha, LOG=acumulador)
                    tokens.append(token)
                elif acumulador in aritmeticos:
                    token = dict(linha=n_linha, ART=acumulador)
                    tokens.append(token)
                #TODO classificar identificador, string, numero, delimitador e erros
                else: 
                    token = dict(linha=n_linha, OUTRO=acumulador)
                    tokens.append(token)
                acumulador = ''
            else:
                acumulador += char
    print(tokens)

