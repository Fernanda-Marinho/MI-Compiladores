from inspections import *

def start (n_line, line):
    line_len = len(line)
    token = {
        'ac': '',
        'state': 0
    }
    double = False
    for i_curr in range(line_len):
        if double == True:
            double = False
            continue
        else:
            if token['state'] == 0: #estado inicial, pode receber qualquer coisa 
                if isLetter(line[i_curr]):
                    token["ac"]+=line[i_curr]
                    token["state"]=1
                elif isDigit(line[i_curr]):
                    token["ac"]+=line[i_curr]
                    token["state"]=3
                elif line[i_curr] == "+":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "+":
                            double = True
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'ART')
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'ART')
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'ART')
                        clear_token(token)    
                elif line[i_curr] == "-":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "-":
                            double = True
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'ART')
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'ART')
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'ART')
                        clear_token(token)
                elif line[i_curr] == "&":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "&":
                            double = True 
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'LOG')
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'TMF')
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'TMF')
                        clear_token(token)
                elif line[i_curr] == '"':
                    token["ac"] += line[i_curr]
                    token["state"] = 7 
                elif isErrTMF(line[i_curr]):
                    token["ac"] = line[i_curr]
                    write_token(n_line,token["ac"],'TMF')
                    clear_token(token)

            elif token["state"]==1: #recebeu uma letra 
                if isSep(line[i_curr]):
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
                    token['ac'] += line[i_curr]
                    token['state'] = 6 
            elif token['state'] == 3: #recebeu um numero 
                if isDigit(line[i_curr]):
                    token['ac'] += line[i_curr]
                elif line[i_curr] != "." and (isLetter(line[i_curr]) or not isInRange(line[i_curr])):
                    token['ac'] += line[i_curr]
                    token['state'] = 5
                elif line[i_curr] == ".":
                    token['ac'] += line[i_curr]
                    token['state'] = 4
                elif isEsp(line[i_curr]):   # Separador espaço
                    write_token(n_line,token["ac"],'NRO')
                    clear_token(token)
                elif isSepNotEsp(line[i_curr]):   # Separador != espaço
                    if (i_curr < line_len - 1):
                        token_class = isNextSymbolDouble(line[i_curr],line[i_curr+1])
                        if token_class:
                            write_token(n_line,token["ac"],'NRO')
                            token["ac"] = f'{line[i_curr]}{line[i_curr+1]}'
                            write_token(n_line,token["ac"],token_class)
                            clear_token(token)
                            double = True
                        else:
                            write_token(n_line,token["ac"],'NRO')
                            token["ac"] = line[i_curr]
                            write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]))        # atenção para se isso resulta None alguma vez
                            clear_token(token)
                    else: 
                        write_token(n_line,token["ac"],'NRO')
                        token["ac"] = line[i_curr]
                        write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]))
                        clear_token(token)

            elif token['state'] == 4:       # NRO com 1 ponto
                if isDigit(line[i_curr]):
                    token['ac'] += line[i_curr]
                elif line[i_curr] == "." or isLetter(line[i_curr]) or (not isSep(line[i_curr])): # segundo ponto ou letra (NMF)
                    token['ac'] += line[i_curr]
                    token['state'] = 5
                elif isSep(line[i_curr]):
                    # TODO quando o separador é diferente de espaço ({[.,:; etc é preciso GUARDAR antes de limpar o token
                    write_token(n_line,token["ac"],'NRO')
                    # classifySep() deve escrever o token do delimitador encontrado para que não se perca ??
                    #       ou uma solução com mais estados.
                    #    IDEIA: usar lookahead para o caso especial dos não-espaços (logo no inicio do bloco)
                    ##   e nesse elif fazer apenas o isEsp
                    clear_token(token)
            elif token['state'] == 5:       # Estado de "acumulação" do NMF!
                if (line[i_curr] == ".") or (not isSep(line[i_curr])):
                    token['ac'] += line[i_curr]
                else:
                    write_token(n_line, token["ac"], 'NMF')
                    clear_token(token)
            elif token['state'] == 6:
                if not isSep(line[i_curr]):
                    token["ac"] += line[i_curr]
                else:
                    write_token(n_line, token['ac'], "IMF")
                    clear_token(token)
            elif token["state"] == 7: #pode ser cadeia de caracteres ou cadeia mal formada  
                if isInRange(line[i_curr]) and (line[i_curr] != '"') and (i_curr<line_len-1):
                    token["ac"] += line[i_curr]
                elif line[i_curr] == '"':
                    token["ac"] += line[i_curr]
                    write_token(n_line, token['ac'], "CAC")
                    clear_token(token)
                elif not isInRange(line[i_curr]):
                    token['ac'] += line[i_curr]
                    token['state'] = 8
                else: # \n
                    write_token(n_line, token['ac'], "CMF")
                    clear_token(token)
            elif token['state'] == 8: # acumular erro de CAC
                if line[i_curr] != '"' and i_curr < line_len-1:
                    token['ac'] += line[i_curr]
                else:
                    if line[i_curr] == '"': token['ac'] += line[i_curr]
                    write_token(n_line, token['ac'], "CMF")
                    clear_token(token)

def clear_token(t):
    t['state'] = 0
    t['ac'] = ''

def write_token(line_number, buffer, class_token):
    # TODO separar erros e escreve-los apenas no final  
    # TODO escrever mensagem de sucesso caso nao haja erros
    t = {
        'linha': line_number,
        class_token : buffer
    }
    print(t)

with open('teste.txt', 'r') as file:
    for index, line in enumerate(file.readlines(), start=1):
        # print(f'{index} {line}')
        start(index, (line+" "))
