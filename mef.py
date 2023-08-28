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
                            write_token(n_line,token["ac"],'ART',errors_tokens)
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'ART',errors_tokens)
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'ART',errors_tokens)
                        clear_token(token)    
                elif line[i_curr] == "-":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "-":
                            double = True
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'ART',errors_tokens)
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'ART',errors_tokens)
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'ART',errors_tokens)
                        clear_token(token)
                elif line[i_curr] == "=":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "=":
                            double = True
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'REL',errors_tokens)
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'REL',errors_tokens)
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'REL',errors_tokens)
                        clear_token(token)
                elif line[i_curr] == "&":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "&":
                            double = True 
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'LOG',errors_tokens)
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'TMF',errors_tokens)
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'TMF',errors_tokens)
                        clear_token(token)
                elif line[i_curr] == "|":
                    if i_curr < line_len - 1:
                        if line[i_curr+1] == "|":
                            double = True 
                            token["ac"] = line[i_curr]+line[i_curr+1]
                            write_token(n_line,token["ac"],'LOG',errors_tokens)
                            clear_token(token)
                        else:
                            token["ac"] += line[i_curr]
                            write_token(n_line,token["ac"],'TMF',errors_tokens)
                            clear_token(token)
                    else:
                        token["ac"] += line[i_curr]
                        write_token(n_line,token["ac"],'TMF',errors_tokens)
                        clear_token(token)
                elif line[i_curr] == '"':
                    token["ac"] += line[i_curr]
                    token["state"] = 7 
                elif not isInRange(line[i_curr]):
                    token["ac"] = line[i_curr]
                    write_token(n_line,token["ac"],'TMF',errors_tokens)
                    clear_token(token)

            elif token["state"]==1: #recebeu uma letra 
                if isSep(line[i_curr]):
                    if isPre(token["ac"]):
                        write_token(n_line,token["ac"],'PRE',errors_tokens)
                        token["ac"] = line[i_curr]
                        clear_token(token)
                    else:
                        write_token(n_line,token["ac"],'IDE',errors_tokens)
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
                elif isEsp(line[i_curr]):   # Separador espaço
                    write_token(n_line,token["ac"],'NRO',errors_tokens)
                    clear_token(token)
                elif line[i_curr] != "." and (isLetter(line[i_curr]) or not isInRange(line[i_curr])):
                    token['ac'] += line[i_curr]
                    token['state'] = 5
                elif line[i_curr] == ".":
                    token['ac'] += line[i_curr]
                    token['state'] = 4
                elif isSepNotEsp(line[i_curr]) or isPossibleLog(line[i_curr]):   # Separador != espaço
                    if (i_curr < line_len - 1):
                        token_class = isNextSymbolDouble(line[i_curr],line[i_curr+1])
                        if token_class:
                            write_token(n_line,token["ac"],'NRO',errors_tokens)
                            token["ac"] = f'{line[i_curr]}{line[i_curr+1]}'
                            write_token(n_line,token["ac"],token_class,errors_tokens)
                            clear_token(token)
                            double = True
                        else:
                            write_token(n_line,token["ac"],'NRO',errors_tokens)
                            token["ac"] = line[i_curr]
                            write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]),errors_tokens)        # atenção para se isso resulta None alguma vez
                            clear_token(token)
                    else: 
                        write_token(n_line,token["ac"],'NRO',errors_tokens)
                        token["ac"] = line[i_curr]
                        write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]),errors_tokens)
                        clear_token(token)

            elif token['state'] == 4:       # NRO com 1 ponto
                if isDigit(line[i_curr]):
                    token['ac'] += line[i_curr]
                elif line[i_curr] == "." or isLetter(line[i_curr]): # segundo ponto ou letra (NMF)
                    token['ac'] += line[i_curr]
                    token['state'] = 5
                elif isEsp(line[i_curr]):   # Separador espaço
                    if isDigit(line[i_curr-1]):
                        write_token(n_line,token["ac"],'NRO',errors_tokens)
                        clear_token(token)
                    else:
                        write_token(n_line,token["ac"],'NMF',errors_tokens)
                        clear_token(token)
                elif isSepNotEsp(line[i_curr]) or isPossibleLog(line[i_curr]):   # Separador != espaço
                    if isDigit(line[i_curr-1]):
                        if (i_curr < line_len - 1):
                            token_class = isNextSymbolDouble(line[i_curr],line[i_curr+1])
                            if token_class:
                                write_token(n_line,token["ac"],'NRO',errors_tokens)
                                token["ac"] = f'{line[i_curr]}{line[i_curr+1]}'
                                write_token(n_line,token["ac"],token_class,errors_tokens)
                                clear_token(token)
                                double = True
                            else:
                                write_token(n_line,token["ac"],'NRO',errors_tokens)
                                token["ac"] = line[i_curr]
                                write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]),errors_tokens)        # atenção para se isso resulta None alguma vez
                                clear_token(token)
                        else: 
                            write_token(n_line,token["ac"],'NRO',errors_tokens)
                            token["ac"] = line[i_curr]
                            write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]),errors_tokens)
                            clear_token(token)
                    else:
                        token['ac'] += line[i_curr]
                        token['state'] = 5
                        
            elif token['state'] == 5:       # Estado de "acumulação" do NMF!
                if (line[i_curr] == ".") or (not isSep(line[i_curr])):
                    token['ac'] += line[i_curr]
                elif isSepNotEsp(line[i_curr]):
                    if (i_curr < line_len - 1):
                        token_class = isNextSymbolDouble(line[i_curr],line[i_curr+1])
                        if token_class:
                            write_token(n_line,token["ac"],'NMF',errors_tokens)
                            token["ac"] = f'{line[i_curr]}{line[i_curr+1]}'
                            write_token(n_line,token["ac"],token_class,errors_tokens)
                            clear_token(token)
                            double = True
                        else:
                            write_token(n_line,token["ac"],'NMF',errors_tokens)
                            token["ac"] = line[i_curr]
                            write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]),errors_tokens)        # atenção para se isso resulta None alguma vez
                            clear_token(token)
                    else: 
                        write_token(n_line,token["ac"],'NMF',errors_tokens)
                        token["ac"] = line[i_curr]
                        write_token(n_line,token["ac"],currentSymbolClass(line[i_curr]),errors_tokens)
                        clear_token(token)
                elif isEsp(line[i_curr]):
                    write_token(n_line, token["ac"], 'NMF',errors_tokens)
                    clear_token(token)
            elif token['state'] == 6:
                if not isSep(line[i_curr]):
                    token["ac"] += line[i_curr]
                else:
                    write_token(n_line, token['ac'], "IMF",errors_tokens)
                    clear_token(token)
            elif token["state"] == 7: #pode ser cadeia de caracteres ou cadeia mal formada  
                if isInRange(line[i_curr]) and (line[i_curr] != '"') and (i_curr<line_len-1):
                    token["ac"] += line[i_curr]
                elif line[i_curr] == '"':
                    token["ac"] += line[i_curr]
                    write_token(n_line, token['ac'], "CAC",errors_tokens)
                    clear_token(token)
                elif not isInRange(line[i_curr]):
                    token['ac'] += line[i_curr]
                    token['state'] = 8
                else: # \n
                    write_token(n_line, token['ac'], "CMF",errors_tokens)
                    clear_token(token)
            elif token['state'] == 8: # acumular erro de CAC
                if line[i_curr] != '"' and i_curr < line_len-1:
                    token['ac'] += line[i_curr]
                else:
                    if line[i_curr] == '"': token['ac'] += line[i_curr]
                    write_token(n_line, token['ac'], "CMF",errors_tokens)
                    clear_token(token)

def clear_token(t):
    t['state'] = 0
    t['ac'] = ''

def write_token(line_number, buffer, class_token, errors_t):
    errors = ['CMF', 'CoMF', 'NMF', 'IMF', 'TMF']
    # TODO escrever mensagem de sucesso caso nao haja erros
    
    if ('\n' in buffer): buffer = buffer.replace('\n','')
    if class_token in errors:
        e_t = {
            'linha' : line_number, 
            class_token : buffer
        }
        errors_t.append(e_t)
    else: 
        t = {
        'linha': line_number,
        class_token : buffer
        }
        print(t)
    # t = {
    # 'linha': line_number,
    # class_token : buffer
    # }
    # print(t)


errors_tokens = []
with open('teste.txt', 'r') as file:
    for index, line in enumerate(file.readlines(), start=1):
        # print(f'{index} {line}')
        start(index, (line+" "))

print("erros")
print(errors_tokens)