from inspections import *

def start(n_line, line):
    line_len = len(line)
    token = {
        'ac': '',
        'state': 0
    }
    for i_curr in range(line_len):
        if token['state'] == 0:
            if isLetter(line[i_curr]):
                token["ac"]+=line[i_curr]
                token["state"]=1
            elif isDigit(line[i_curr]):
                token["ac"]+=line[i_curr]
                token["state"]=3
            elif isErr(line[i_curr]):
                token["ac"] = line[i_curr]
                write_token(n_line,token["ac"],'TMF')
                clear_token(token)
            elif line[i_curr] == "+":
                token["ac"] = line[i_curr]
                token["state"] = 5
            elif line[i_curr] == '-':
                token["ac"] += line[i_curr]
                token["state"] = 6
        elif token["state"]==1:
            if isSep(line[i_curr]):
                # token["state"] = 2
                if isPre(token["ac"]):
                    write_token(n_line,token["ac"],'PRE')
                    token["ac"] = line[i_curr]
                    clear_token(token)
                else:
                    write_token(n_line,token["ac"],'IDE')
                    token["ac"] = line[i_curr]
                    clear_token(token)
            elif isLetter(line[i_curr]) or isDigit(line[i_curr]) or line[i_curr] == "_":
                token["ac"]+=line[i_curr]
            else:
                #TODO identificador mal formado
                # clear_token(token)
                pass
        elif token['state'] == 3:
            if isDigit(line[i_curr]):
                token['ac'] += line[i_curr]
            elif isLetter(line[i_curr]):
                token['ac'] += line[i_curr]
                write_token(n_line, token["ac"], 'NMF')
                clear_token(token)
            elif line[i_curr] == ".":
                token['state'] = 4
                token['ac'] += line[i_curr]
            elif isSep(line[i_curr]):
                write_token(n_line,token["ac"],'NRO')
                clear_token(token)
        elif token['state'] == 4:
            if isDigit(line[i_curr]):
                token['ac'] += line[i_curr]
            elif isLetter(line[i_curr]) or line[i_curr] == "." or isErr(line[i_curr]): 
                token['ac'] += line[i_curr]
                write_token(n_line, token["ac"], 'NMF')
                clear_token(token)
            elif isSep(line[i_curr]):
                write_token(n_line,token["ac"],'NRO')
                clear_token(token)
        elif token['state'] == 5:
            if line[i_curr] == "+":
                token["ac"] += line[i_curr]
                write_token(n_line, token["ac"], 'ART') #token ++
                clear_token(token)
                token["ac"] = line[i_curr]
                token["state"] = 0
            else:
                write_token(n_line, token["ac"], 'ART' ) #token +
                clear_token(token)
                token["ac"] = line[i_curr]
                token["state"] = 0
        elif token["state"] == 6:
            if line[i_curr] == "-":
                token["ac"] += line[i_curr]
                


def clear_token(t):
    t['state'] = 0
    t['ac'] = ''

def write_token(line_number, buffer, class_token):
    # TODO separar erros e escreve-los apenas no final  
    # TODO escrever mensagem de sucesso caso não haja erros
    t = {
        'linha': line_number,
        class_token : buffer
    }
    print(t)

with open('exemplos/01.txt', 'r') as file:
    for index, line in enumerate(file.readlines(), start=1):
        # print(f'{index} {line}')
        start(index, line)
        # n_line += 1
