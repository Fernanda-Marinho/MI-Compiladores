global g #escopo global (sem classe)
global c #classe
global cond_m #existe metodo? 
cond_m = False
global m  
global cond_o #existe objeto?
cond_o = False
global var 
global expressao #expressao depois da atribuicao 
expressao = []
global tem_if #tem if?
tem_if = False
global if_var #variaveis dentro da condicao do if
if_var = []
global tem_for #tem for?
tem_for = False
global metodo_this 
metodo_this = False  
global param 
param = []
global erros_semanticos
erros_semanticos = [] 
# -------------------- ANALISE SEMANTICA --------------------------------
class TabelaSimbolos():
    def __init__(self):
        self.scopes = {}
        self.classes = []

    def add_classe(self, classe, linha):
        global erros_semanticos
        if (classe in self.classes):
            #print(f"<{linha}> <{classe}> duplicada!")
            erros_semanticos.append(f"<{linha}> <{classe}> duplicada!")
        self.classes.append(classe)
        self.scopes[classe] = {}
        self.scopes[classe]['atributos'] = None
        self.scopes[classe]['extends'] = None
        self.scopes[classe]['objetos'] = None
        self.scopes[classe]['metodos'] = None
        if classe == '@':
            self.scopes[classe]['constantes'] = None 
        

    def add_atribute(self, classe, nome, tipo, linha):
        global erros_semanticos
        cond = True 
        if (self.scopes[classe]['atributos'] == None): #primeiro atributo 
            self.scopes[classe]['atributos'] = [{
                'nome': nome,
                'tipo': tipo
            }]
        else:
            for i in self.scopes[classe]['atributos']:
                if i['nome'] == nome:
                    #print(f"<{linha}> <{nome}> duplicado!")
                    erros_semanticos.append(f"<{linha}> <{nome}> duplicado!")
                    cond = False 
                    break 
            if (cond):
                self.scopes[classe]['atributos'].append({ 
                    'nome': nome,
                    'tipo': tipo
                })
    
    def add_variable(self, classe, metodo, nome, tipo, linha):
        global erros_semanticos
        cond = True
        d = self.scopes[classe]['metodos'][metodo]
        dicionario = d[-1]
        if (dicionario['variaveis'] == None): #primeira variavel
            dicionario['variaveis'] = [{
                'nome': nome,
                'tipo': tipo
            }]
        else:
            for i in dicionario['variaveis']:
                if i['nome'] == nome:
                    erros_semanticos.append(f"<{linha}> <{nome}> duplicado!")
                    #print(f"<{linha}> <{nome}> duplicado!")
                    cond = False 
                    break 
            if (cond):
                dicionario['variaveis'].append({ 
                    'nome': nome,
                    'tipo': tipo
                })

    def add_param(self, classe, metodo, tipo, parametro, linha):
        global erros_semanticos
        cond = True 
        d = self.scopes[classe]['metodos'][metodo]
        dicionario = d[-1]
        if (dicionario['parametros'] == None): #primeiro parametro
            dicionario['parametros'] = [{
                'nome': parametro,
                'tipo': tipo
            }]
        else:
            for i in dicionario['parametros']:
                if i['nome'] == parametro:
                    #print(f"<{linha}> <{parametro}> duplicado!")
                    erros_semanticos.append(f"<{linha}> <{parametro}> duplicado!")
                    cond = False 
                    break 
            if (cond):
                dicionario['parametros'].append({ 
                    'nome': parametro,
                    'tipo': tipo
                })

    def quantidade_parametros(self, classe, metodo):
        cont = 0 
        d = self.scopes[classe]['metodos'][metodo]
        dicionario = d[-1]
        if (dicionario['parametros'] == None):
            dicionario['qtd parametros'] = cont
        else:
            for i in dicionario['parametros']:
                cont += 1
            dicionario['qtd parametros'] = cont

    
    def add_object_metodo(self, classe, metodo, nome, tipo, linha):
        global erros_semanticos
        cond = True
        d = self.scopes[classe]['metodos'][metodo]
        dicionario = d[-1]
        if (dicionario['objetos'] == None): #primeira variavel
            dicionario['objetos'] = [{
                'nome': nome,
                'tipo': tipo
            }]
        else:
            for i in dicionario['objetos']:
                if i['nome'] == nome:
                    erros_semanticos.append(f"<{linha}> <{nome}> duplicado!")
                    #print(f"<{linha}> <{nome}> duplicado!")
                    cond = False 
                    break 
            if (cond):
                dicionario['objetos'].append({ 
                    'nome': nome,
                    'tipo': tipo
                })



    
    def add_const(self, classe, nome, tipo, linha):
        global erros_semanticos
        cond = True
        if (self.scopes[classe]['constantes'] == None): #primeira constante  
            self.scopes[classe]['constantes'] = [{
                'nome': nome,
                'tipo': tipo,
                'valor': None
            }]
        else:
            for i in self.scopes[classe]['constantes']:
                if i['nome'] == nome:
                    #print(f"<{linha}> <{nome}> duplicado!")
                    erros_semanticos.append(f"<{linha}> <{nome}> duplicado!")
                    cond = False 
                    break 
            if (cond):
                self.scopes[classe]['constantes'].append({ 
                    'nome': nome,
                    'tipo': tipo,
                    'valor': None
                })
    
    def add_value_const(self, classe, valor):
        ultimo = self.scopes[classe]['constantes'][-1]
        ultimo['valor'] = valor

    
    def pegar_tipo(self, classe, categoria):
        tipo = self.scopes[classe][categoria][-1]
        if (tipo):
            return tipo['tipo']
    
    def pegar_tipo_metodo(self, classe, metodo):
        d = self.scopes[classe]['metodos'][metodo]
        d = d[-1]
        t = d['variaveis']
        t = t[-1]
        if (t):
            return t['tipo']
    
    def verificar_varivel_existe(self, classe, metodo, variavel, linha):
        #verifica se a variavel existe, se existir retorna o tipo dela
        #vai ser util na parte de comandos dos metodos
        global erros_semanticos
        if (variavel == 'this'):
            return False, False
        dicionario = self.scopes[classe]['metodos'][metodo]
        d = dicionario[-1]
        v = d['variaveis']
        if v == None:
            #print(f"<{linha}> <{variavel}> não declarada")
            erros_semanticos.append(f"<{linha}> <{variavel}> não declarada")
            return False, False
        if (variavel == 'true') or (variavel == 'false'):
            #print(f"<{linha}> tipo incompatível!")
            erros_semanticos.append(f"<{linha}> tipo incompatível!")
            return False, False
        for i in v:
            if i['nome'] == variavel:
                return True, i['tipo']
        #print(f"<{linha}> <{variavel}> não declarada")
        erros_semanticos.append(f"<{linha}> <{variavel}> não declarada")
        return False, False

    def verificar_atr_int(self, exp, var, linha, classe, metodo):
        global erros_semanticos
        global tem_for
        cond = False
        exibir = True
        v = False
        if (tem_for):
            existe, tipo = self.verificar_varivel_existe(classe, metodo, var, linha)
            if (existe):
                if (tipo == 'int'):
                    v = True 
                else:
                    cond = True
            else:
                cond = True
                exibir = False
            if (v):
                if not(exp.isdigit()):
                    cond = True
        else:
            for i in exp:
                if (i[0] != '"'): 
                    if(i.isalpha()):
                        existe, tipo = self.verificar_varivel_existe(classe, metodo, i, linha)
                        if (existe):
                            if (tipo == 'int'):
                                pass
                            else:
                                cond = True
                                break
                        else: #var nao existe, logo nao  precisa exibir msg de erro de tipo
                            exibir = False #nao precisa exibir dois erros ao msm tempo
                            cond = True 
                            break
                    else: #verifica de fato se é int
                        if not(i.isdigit()):
                            cond = True
                            break
                else:
                    cond = True 
                    break 

        if (cond and exibir): 
            #print(f"<{linha}> tipo incompatível <{var}> <int>")
            erros_semanticos.append(f"<{linha}> tipo incompatível <{var}> <int>")
    
    def verificar_atr_real(self, exp, var, linha, classe, metodo):
        global erros_semanticos
        cond = False
        exibir = True
        for i in exp:
            if (i[0] != '"'): 
                if(i.isalpha()):
                    existe, tipo = self.verificar_varivel_existe(classe, metodo, i, linha)
                    if (existe):
                        if (tipo == 'real'):
                            pass
                        else:
                            cond = True
                            break
                    else: #var nao existe, logo nao  precisa exibir msg de erro de tipo
                        exibir = False #nao precisa exibir dois erros ao msm tempo
                        cond = True 
                        break
                else: #verifica de fato se é real 
                    if (i.isdigit()):
                        exibir = False
                        cond = True 
                        break
                    else:
                        try:
                            float(i)
                            pass
                        except:
                            cond = True
                            break
            else:
                cond = True 
                break 

        if (cond and exibir):
            #print(f"<{linha}> tipo incompatível <{var}> <real>")
            erros_semanticos.append(f"<{linha}> tipo incompatível <{var}> <real>")
    
    def verificar_atr_string(self, exp, var, linha, classe, metodo):
        global erros_semanticos
        cond = False
        exibir = True
        for i in exp:
            if (i[0] != '"'): 
                if(i.isalpha()):
                    existe, tipo = self.verificar_varivel_existe(classe, metodo, i, linha)
                    if (existe):
                        if (tipo == 'string'):
                            pass
                        else:
                            cond = True
                            break
                    else: #var nao existe, logo nao  precisa exibir msg de erro de tipo
                        exibir = False #nao precisa exibir dois erros ao msm tempo
                        cond = True 
                        break
                else: #verifica de fato se é string 
                    if (i[0] != "'"):
                        cond = True 
                        break
                    
            else: #significa que é string
                pass

        if (cond and exibir):
            erros_semanticos.append(f"<{linha}> tipo incompatível <{var}> <string>")
            #print(f"<{linha}> tipo incompatível <{var}> <string>")
    
    def verificar_atr_boolean(self, exp, var, linha, classe, metodo):
        global erros_semanticos
        cond = False
        exibir = True
        for i in exp:
            if (i == 'true') or (i == 'false'):
                pass
            else:
                if (i[0] != '"'): 
                    if(i.isalpha() or '_' in i):
                        existe, tipo = self.verificar_varivel_existe(classe, metodo, i, linha)
                        if (existe):
                            if (tipo == 'boolean'):
                                pass
                            else:
                                cond = True
                                break
                        else: #var nao existe, logo nao  precisa exibir msg de erro de tipo
                            exibir = False #nao precisa exibir dois erros ao msm tempo
                            cond = True 
                            break
                    else: #verifica de fato se é boolean 
                        if (i != 'true') and (i != 'false'):
                            cond = True
                            break
                else:
                    cond = True 
                    break 

        if (cond and exibir):
            erros_semanticos.append(f"<{linha}> tipo incompatível <{var}> <boolean>")
            #print(f"<{linha}> tipo incompatível <{var}> <boolean>")
    
    
    def atribuicao(self, classe, categoria, identificador, valor, linha):
        global erros_semanticos
        escopo = self.scopes[classe][categoria]
        tipo = None
        existe = False
        for i in escopo:
            if (i['nome'] == identificador):
                tipo = i['tipo']
                existe = True
                break 
        if(existe):
            if (tipo == 'int'):
                if (valor.isdigit()):
                    i['valor'] = valor
                else:
                    erros_semanticos.append(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                    #print(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                    i['valor'] = None
            elif (tipo == 'boolean'):
                if (valor == 'true' or valor == 'false'):
                    i['valor'] = valor
                else:
                    erros_semanticos.append(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                    #print(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                    i['valor'] = None
            elif tipo == 'string':
                if valor[0] == '"':
                    i['valor'] = valor
                else:
                    erros_semanticos.append(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                    #print(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>") 
                    i['valor'] = None
            else: #real 
                if valor.isdigit():
                    if tipo == None:
                        pass
                    else:
                        erros_semanticos.append(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                        #print(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                        i['valor'] = None
                else:
                    try:
                        float(valor)
                        i['valor'] = valor
                    except:
                        if tipo == None:
                            pass
                        else:
                            erros_semanticos.append(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                            #print(f"<{linha}> tipo incompatível <{identificador}> <{tipo}>")
                            i['valor'] = None
        else:
            erros_semanticos.append(f"<{linha}> <{identificador}> não existe!")
            #print(f"<{linha}> <{identificador}> não existe!")        
    
    def add_exist_superclass(self, classe, superclass, linha):
        global erros_semanticos
        cond = False
        for i in self.scopes:
            if (i == superclass):
                cond = True
                break
        if (cond):
            self.scopes[classe]['extends'] = superclass
        else:
            erros_semanticos.append(f"<{linha}> <{superclass}> não existe!")
            #print(f"<{linha}> <{superclass}> não existe!")
    
    def exist_classe(self, classe, candidata, linha):
        global erros_semanticos
        cond = True
        for i in self.scopes:
            if (i == candidata):
                cond = False
                return True
        if (cond):
            erros_semanticos.append(f"<{linha}> tipo incompatível <{candidata}>")
            #print(f"<{linha}> tipo incompatível <{candidata}>")
            return False

    
    def add_object(self, classe, tipo, nome, linha):
        global erros_semanticos
        cond = True 
        if (self.scopes[classe]['objetos'] == None): #primeiro objeto 
            self.scopes[classe]['objetos'] = [{
                'nome': nome,
                'tipo': tipo
            }]
        else:
            for i in self.scopes[classe]['objetos']:
                if i['nome'] == nome:
                    erros_semanticos.append(f"<{linha}> <{nome}> duplicado!")
                    #print(f"<{linha}> <{nome}> duplicado!")
                    cond = False 
                    break 
            if (cond):
                self.scopes[classe]['objetos'].append({ 
                    'nome': nome,
                    'tipo': tipo
                })
    
    def add_method(self, classe, tipo, nome, linha):
        global erros_semanticos
        if self.scopes[classe]['metodos'] is None:  # primeiro método
            self.scopes[classe]['metodos'] = {}
        
        if nome in self.scopes[classe]['metodos']:
            erros_semanticos.append(f"<{linha}> <{nome}> duplicado!")
            #print(f"<{linha}> <{nome}> duplicado!")
        else:
            if nome not in self.scopes[classe]['metodos']:
                self.scopes[classe]['metodos'][nome] = []
            
            self.scopes[classe]['metodos'][nome].append({
                'tipo': tipo,
                'variaveis': None,
                'objetos': None,
                'parametros': None,
                'qtd parametros': None
            })
    
    def verificar_metodo_existe(self, classe, metodo, linha):
        global erros_semanticos
        global metodo_this
        cond = True
        dicionario = self.scopes[classe]['metodos']
        for i in dicionario:
            if i == metodo:
                metodo_this = metodo
                cond = False
                break 
        if (cond):
            erros_semanticos.append(f"<{linha}> <{metodo}> não declarado!")
            #print(f"<{linha}> <{metodo}> não declarado!")

    def verificar_parametros(self, classe, metodo, parametros, linha):
        global erros_semanticos
        cond = True
        index = 0 
        dicionario = self.scopes[classe]['metodos']
        d = dicionario[metodo]
        p = d[0]['parametros']
        qtd = d[0]['qtd parametros']
        if (qtd != len(parametros)):
            erros_semanticos.append(f"<{linha}> erro na quantidade de parametros!")
            #print(f"<{linha}> erro na quantidade de parametros!")
            cond = False
        else:
            #primeiro verificar se a variavel existe 
            for i, j in zip(parametros, p):
                if i[0] != ('"'):
                    if(i.isalpha()):
                        existe, tipo = self.verificar_varivel_existe(classe, metodo, i, linha)
                        if (existe):
                            if tipo == j['tipo']:
                                pass
                            else:
                                erros_semanticos.append(f"<{linha}> tipo incompatível <{i}> <{j['tipo']}>")
                                #print(f"<{linha}> tipo incompatível <{i}> <{j['tipo']}>")
                    else:
                        if j['tipo'] == 'int':
                            if not (i.isdigit()):
                                erros_semanticos.append(f"<{linha}> tipo incompatível <{i}> <{j['tipo']}>")
                                #print(f"<{linha}> tipo incompatível <{i}> <{j['tipo']}>")
                        elif j['tipo'] == 'real':
                            pass
                        elif j['tipo'] == 'boolean':
                            pass
                else:
                    if j['tipo'] != 'string':
                        erros_semanticos.append(f"<{linha}> tipo incompatível <{i}> <{j['tipo']}>")
                        #print(f"<{linha}> tipo incompatível <{i}> <{j['tipo']}>")
    

    def show_expression(self):
        global expressao
        print(expressao)

    def show_table(self):
        for i in self.scopes:
            print(f"Classe {i}:")
            for j in self.scopes[i]:
                print(f"{j} -> {self.scopes[i][j]}")
            print()
    




# --------------------- ANALISE SINTATICA ---------------------------------- 
class AnaliseSintatica():
    def __init__(self, token_collection):
        self.tokens = token_collection
        self.index = 0
        self.errors = []
        self.errors_string = ''
        self.symbol_table = TabelaSimbolos()

    def start(self):
        global erros_semanticos
        global g
        erros_semanticos = []
        g = 1
        self.symbol_table.add_classe('@', self.current_token_line())
        self.consts_block()
        self.variables_block()
        g = 0
        self.class_block()
        while (self.current_token_text() == 'class'):
            self.class_block()
        # print(self.errors_string)
        #self.symbol_table.show_table()
        return self.errors_string, erros_semanticos

    ###############         Funções auxiliares para análise          ###############

    def next_token(self):
        self.index +=1

    #   refere-se ao token anterior com relação ao ponteiro
    def last_token(self):
        return self.tokens[self.index-1] if self.index > 0 else self.current_token()

    def last_token_line(self):
        return self.last_token()['n_line']

    def last_token_class(self):
        return self.last_token()['token_class']

    def last_token_text(self):
        return self.last_token()['token_text']

    def current_token(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else dict(n_line = '',token_class = '',token_text = '')
                                                                                  
    def current_token_line(self):
        return self.current_token()['n_line']

    def current_token_class(self):
        return self.current_token()['token_class']

    def current_token_text(self):
        return self.current_token()['token_text']
    
    def write_error(self, e: SyntaxError):
        message = f'{e.msg}, received: {self.current_token_text()} in line {self.tokens[self.index]["n_line"]}'
        self.errors.append(message)
        self.errors_string = f'{self.errors_string} \n {message}'
        # sincronizar/tratamento de erros

    def error(self, text):
        raise SyntaxError (text)

    ###############         Produções da gramática          ###############

    # Terminais <TYPE>
    def match_TYPE(self):
        type = ['int','real','boolean','string']
        return bool(self.current_token_text() in type)
    
    # Terminais <ATTRIBUTION>
    def match_ATTRIBUTION(self):
        v = self.current_token_text()
        return isinstance(v, (int, float, complex, str, bool))
    
    #  Terminais ART_DOUBLE (classificacao)
    def match_ART_DOUBLE(self):
        return bool(self.current_token_text() == '++' or self.current_token_text() == '--')

    def match_Bool(self):
        return bool(self.current_token_text() == 'true' or self.current_token_text() == 'false')

    # Bloco <CONSTS_BLOCK>
    def consts_block(self):
        try: 
            if self.current_token_text() == 'const':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.consts()
                else:
                    self.error('Expected "{"')
            else:
                self.error('Expected "const"')
        except SyntaxError as e:
            self.write_error(e)

    #   CONSTS (recursao para gerar varias)
    def consts(self):
        try:
            if self.current_token_text() == "}":
                self.next_token()
            elif self.match_TYPE():
                self.const()
                self.consts()
            else:
                self.error('Expected "}" or "const"')
        except SyntaxError as e:
            self.write_error(e)

    #   <CONST>
    def const(self):
        try: 
            if self.match_TYPE():
                self.next_token()
                self.const_attribution()
                self.multiple_consts()
                # não precisa de next aqui, o multiple_consts já consumiu
            else:
                self.error('Expected <TYPE>')
        except SyntaxError as e:
            self.write_error(e=e)

    #   <CONST_ATTRIBUTION>
    def const_attribution(self):
        try:
            if self.current_token_class() == 'IDE':
                if self.last_token_text() == ',':
                    tipo_escopo = self.symbol_table.pegar_tipo('@', 'constantes')
                    self.symbol_table.add_const('@', self.current_token_text(), tipo_escopo, self.current_token_line())
                else:
                    self.symbol_table.add_const('@', self.current_token_text(), self.last_token_text(), self.current_token_line())
                self.next_token()
                if self.current_token_text() == '=':
                    constante = self.last_token_text()
                    self.next_token()
                    self.symbol_table.add_value_const('@', self.current_token_text())
                    self.symbol_table.atribuicao('@', 'constantes', constante, self.current_token_text(), self.current_token_line())
                    if self.match_ATTRIBUTION():
                        self.next_token()
                    else:
                        self.error('Expected "<NRO> or Bool or <CAC>"')
                else:
                    self.error('Expected "="')
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e=e)

    #   Bloco <MULTIPLE_CONSTS>
    def multiple_consts(self):
        try:
            if self.current_token_text() == ',':
                self.next_token()
                self.const_attribution()
                self.multiple_consts()
            elif self.current_token_text() == ';':
                self.next_token()
            else:
                self.error('Expected "," or ";" ')
        except SyntaxError as e:
            self.write_error(e)

    # Bloco <VARIABLES_BLOCK>
    def variables_block (self):
        try:
            if self.current_token_text() == 'variables':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.variables()
                else:
                    raise SyntaxError ('Expected "{"')
            else: self.error('Expected "variables"')
        except SyntaxError as e:
            self.write_error(e)
    
    #   <VARIABLES>
    def variables(self):
        try:
            if self.current_token_text() == '}':
                self.next_token()
            elif self.match_TYPE():
                self.variable()
                self.variables()
            else:
                self.error('Expected "}" or <TYPE>')
        except SyntaxError as e:
            self.write_error(e)

    #   Bloco <VARIABLE>
    def variable(self):
        try:
            if self.match_TYPE():
                self.next_token()
                self.dec_var() #
                self.multiple_variables_line()  #
            else:
                self.error('Expected <TYPE>')
        except SyntaxError as e:
            self.write_error(e=e)
    
    # Bloco <DEC_VAR>   declaracao de variavel
    def dec_var(self):
        global g
        global c
        global m
        global cond_m
        global cond_o
        try:
            if (self.current_token_class() == "IDE"):
                if self.last_token_text() == ',':
                    if g == 1:
                        tipo_escopo = self.symbol_table.pegar_tipo('@', 'atributos')
                        self.symbol_table.add_atribute('@', self.current_token_text(), tipo_escopo, self.current_token_line())
                    else:
                        tipo_escopo = self.symbol_table.pegar_tipo('@', 'atributos')
                        if (cond_o):
                            tipo = self.symbol_table.pegar_tipo_metodo(c, m)
                            instancia = self.symbol_table.exist_classe(c, tipo, self.current_token_line())
                            if (instancia):
                                self.symbol_table.add_object_metodo(c, m, self.current_token_text(), tipo, self.current_token_line())
                        elif (cond_m):
                            #pass
                            tipo = self.symbol_table.pegar_tipo_metodo(c, m)
                            self.symbol_table.add_variable(c, m, self.current_token_text(), tipo, self.current_token_line())
                        else:
                            self.symbol_table.add_atribute(c, self.current_token_text(), tipo_escopo, self.current_token_line())
                else:
                    if g == 1:
                        self.symbol_table.add_atribute('@', self.current_token_text(), self.last_token_text(), self.current_token_line())
                    else:
                        if (cond_o):
                            instancia = self.symbol_table.exist_classe(c, self.last_token_text(), self.current_token_line())
                            if (instancia):
                                self.symbol_table.add_object_metodo(c, m, self.current_token_text(), self.last_token_text(), self.current_token_line())
                        elif (cond_m):
                            #pass
                            self.symbol_table.add_variable(c, m, self.current_token_text(), self.last_token_text(), self.current_token_line())
                        else:
                            self.symbol_table.add_atribute(c, self.current_token_text(), self.last_token_text(), self.current_token_line())
                self.next_token()
                self.dimensions()
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    #   Bloco <DIMENSIONS>
    #<DIMENSIONS> ::= '[' <SIZE_DIMENSION> ']' <DIMENSIONS>
                # |
    def dimensions(self):
        try:
            if self.current_token_text() == '[':
                self.next_token()
                self.size_dimension()
                if self.current_token_text() == "]":
                    self.next_token()
                    self.dimensions()   # r a direita
                else:
                    self.error('Expected "]"')
            else:
                pass
        except SyntaxError as e:
            self.write_error(e)

    #   <SIZE_DIMENSION>
    def size_dimension(self):
        try:
            if self.current_token_class() == 'IDE' or self.current_token_class() == 'NRO':
                self.next_token()
            else:
                self.error("Expected <NRO> or <IDE>")
        except SyntaxError as e:
            self.write_error(e=e)

    #   <MULTIPLE_VARIABLES_LINE>
    def multiple_variables_line(self):
        try:
            if self.current_token_text() == ';':
                self.next_token()
            elif self.current_token_text() == ',':
                self.next_token()
                self.dec_var()
                self.multiple_variables_line()
            else:
                self.error('Expected ";" or ","')
        except SyntaxError as e:
            self.write_error(e=e)

    #   Bloco <CLASS_BLOCK>

    ###############         Produções da gramática          ###############

    #bloco de objetos 
    def objects_block(self):
        try:
            if self.current_token_text() == 'objects':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.objects()
                else:
                    self.error('Expected "{"')
        except SyntaxError as e:
            self.write_error(e)    
    

    def objects(self): #duvida nesse 
        try:
            if self.current_token_class() == 'IDE':
                self.object()
                self.objects()
            elif self.current_token_text() == '}':
                self.next_token() 
            else:
                self.error('Expected <IDE> or "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def object(self):
        global c
        global cond_m
        global cond_o
        if (cond_m):
            cond_o = True 
        try:
            if self.current_token_class() == 'IDE':
                instancia = self.symbol_table.exist_classe(c, self.current_token_text(), self.current_token_line())
                self.next_token()
                if (instancia):
                    if (not cond_o): #garante que o objeto passado nao esta dentro de um metodo 
                        self.symbol_table.add_object(c, self.last_token_text(), self.current_token_text(), self.current_token_line())
                self.dec_var()
                self.multiple_objects()
                cond_o = False
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def multiple_objects(self):
        global c
        global cond_m
        global cond_o
        if (cond_m):
            cond_o = True
        try:
            if self.current_token_text() == ';':
                self.next_token()
            elif self.current_token_text() == ',':
                self.next_token()
                tipo_obj = self.symbol_table.pegar_tipo(c, 'objetos')
                instancia = self.symbol_table.exist_classe(c, tipo_obj, self.current_token_line())
                if (instancia):
                    if (not cond_o): #garante que o objeto passado nao esta dentro de um metodo 
                        self.symbol_table.add_object(c, tipo_obj, self.current_token_text(), self.current_token_line())
                self.dec_var()
                self.multiple_objects()
            else:
                self.error('Expected ";" or ","')
        except SyntaxError as e:
            self.write_error(e)

# main

    def main_methods(self):
        global cond_m 
        try:
            if self.current_token_text() == 'methods':
                cond_m = True
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.main_methods_body()
                    if self.current_token_text() == '}':
                        self.next_token()
                        cond_m = False 
                    else:
                        self.error('Expected "}"')
                else:
                    self.error('Expected "{"')
            else:
                self.error('Expected "methods"')
        except SyntaxError as e:
            self.write_error(e)
    
    def main_methods_body(self):
        global c
        global m 
        try:
            self.main_type()
            if self.current_token_text() == 'main':
                m = self.current_token_text()
                self.symbol_table.add_method(c, self.last_token_text(), self.current_token_text(), self.current_token_line())
                self.next_token()
                if self.current_token_text() == '(':
                    self.next_token()
                    if self.current_token_text() == ')':
                        self.symbol_table.quantidade_parametros(c, m)
                        self.next_token()
                        if self.current_token_text() == '{':
                            self.next_token()
                            self.method_body()
                            self.methods()  
                        else:
                            self.error('Expected "{"')
                    else:
                        self.error('Expected ")"')
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "main"')
        except SyntaxError as e:
            self.write_error(e)
    
    #   <METHOD_BODY>
    def method_body(self):
        global expressao
        self.variables_block()
        self.objects_block()
        self.commands_method_body()
        #self.symbol_table.show_expression()
        
        
    def commands_method_body(self):
        try:
            self.commands()
            if self.current_token_text() == 'return':
                self.next_token()
                self.return_block()     # return_block equivalente a <RETURN>
                if self.current_token_text() == ';':
                    self.next_token()
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        self.error('Expected "}')
                else:
                    self.error('Expected ";"')
            else:
                self.error('Expected "return"')
        except SyntaxError as e:
            self.write_error(e=e)
    
    def match_value_firsts(self):
        return bool((self.current_token_text() in ["[" , "!" , "("]) or (self.current_token_class() in [ 'NRO' , 'CAC' , 'IDE']) or self.match_Bool())

    def return_block(self):
        try:
            if self.match_value_firsts():
                self.value()
            else:
                pass
        except:
            pass

    def init_expression(self):
        self.dec_object_attribute_access()
        self.arithmetic_or_logical_expression()
    
    def arithmetic_or_logical_expression(self):
        if self.current_token_class() == 'ART':
            self.simple_or_double_arithmethic_expression()
        # elif self.current_token_text() == '->' or self.current_token_class() == 'LOG' or self.current_token_class() == 'REL':
        else:
            self.optional_object_method_access()
            self.log_rel_optional()
            self.logical_expression_end()


    def value(self): #TODO parei de verificar blocos nessa função
        global expressao 
        global param
        global metodo_this
        try:
            if self.current_token_text() == '[':
                self.vector_assign_block()
            elif self.current_token_class() == 'IDE':
                expressao.append(self.current_token_text())
                if (metodo_this):
                    param.append(self.current_token_text())
                self.init_expression()
            elif self.current_token_text() == '!':
                self.logical_expression_begin()
                self.logical_expression_end()
            elif self.current_token_text() == '(':
                self.arithmethic_or_logical_expression_with_parentheses()
            elif self.current_token_class() == 'NRO':
                if (metodo_this):
                    param.append(self.current_token_text())
                expressao.append(self.current_token_text())
                self.next_token()
                self.simple_or_double_arithmetic_expression_optional()
            elif self.match_Bool():
                if (metodo_this):
                    param.append(self.current_token_text())
                expressao.append(self.current_token_text())
                self.next_token()
            elif self.current_token_class() == 'CAC':
                if (metodo_this):
                    param.append(self.current_token_text())
                expressao.append(self.current_token_text())
                self.next_token()
            else:
                self.error('Expected any of the following: \n\t\t "[" , "!" , "(" , <BOOL> , <NRO> , <CAC> , <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def vector_assign_block(self):
        try:
            if self.current_token_text() == '[':
                self.next_token()
                self.elements_assign()
                if self.current_token_text() == ']':
                    self.next_token()
                else:
                    self.error('Expected "]"')
            else:
                self.error('Expected "["')  # provavelmente inatingivel (value gera vazio)
        except SyntaxError as e:
            self.write_error(e)

    def elements_assign(self):
        self.element_assign()
        self.multiple_elements_assign()

    def multiple_elements_assign(self):
        if self.current_token_text() == ',':
            self.next_token()
            self.element_assign()
            self.multiple_elements_assign()
        else:
            pass
    
    def element_assign(self):
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
            elif self.current_token_class() == 'CAC':   #StringLiteral
                self.next_token()
            elif self.current_token_class() == 'NRO':
                self.next_token()
            elif self.current_token_text() == '[':
                self.n_dimensions_assign()
            else:
                self.error('Expected <IDE> , <CAC> , <NRO> or "["')
        except SyntaxError as e:
            self.write_error(e)
    
    def n_dimensions_assign(self):
        try:
            if self.current_token_text() == '[':
                self.next_token()
                self.elements_assign()
                if self.current_token_text() == ']':
                    self.next_token()
                else:
                    self.error('Expected "]"')
            else:
                pass    #prod. vazia
        except SyntaxError as e:
            self.write_error(e)


    def arithmethic_or_logical_expression_with_parentheses(self):
        try:
            if self.current_token_text() == '(':
                self.next_token()
                self.expressions()
                if self.current_token_text() == ')':
                    self.next_token()
                    self.expressions_without_parentheses_end()
                else:
                    self.error('Expected ")"')
            else:
                self.error('Expected "("')
        except SyntaxError as e:
            self.write_error(e)
    
    def expressions(self):
        try:
            if self.current_token_text() == '(':
                self.parentheses_begin()
            elif self.current_token_class() == 'NRO':
                self.simple_expression_without_parentheses()
            elif self.match_Bool():
                self.logical_expression_without_parentheses()
            elif self.current_token_class() == 'IDE':
                self.simple_or_logical_ide_begin()
            else:
                self.error('Expected "(" or <NRO> or "true","false" or <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def simple_or_logical_ide_begin(self):
        try:
            if self.current_token_class() == 'IDE':
                self.dec_object_attribute_access()
                self.simple_or_logical_ide_end()
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def simple_or_logical_ide_end(self):
        try:
            if self.current_token_class() == 'ART':
                self.end_expression()
            elif self.current_token_text() == '->':
                self.optional_object_method_access()
                self.log_rel_optional()
                self.logical_expression_end()
            else:
                self.error('Expected <ART> or "->"')
        except SyntaxError as e:
            self.write_error(e)

    def logical_expression_without_parentheses(self):
        try:
            if self.match_Bool():
                self.next_token()
                self.logical_expression_end()
            elif self.current_token_text() == '!':
                self.next_token()
                self.logical_expression_begin()
                self.logical_expression_end()
            else:
                self.error('Expected "true", "false" or "!"')
        except SyntaxError as e:
            self.write_error(e=e)

    def simple_expression_without_parentheses(self):
        try:
            if self.current_token_class() == 'NRO':
                self.next_token()
                self.end_expression()
            else:
                self.error('Expected <NRO>')
        except SyntaxError as e:
            self.write_error(e)

    def parentheses_begin(self):
        try:
            if self.current_token_text() == '(':
                self.next_token()
                self.expressions()
                self.parentheses_end()
            else:
                self.error('Expected "("')
        except SyntaxError as e:
            self.write_error(e)
    
    def parentheses_end(self):
        try:
            if self.current_token_text() == ')':
                self.next_token()
                self.expressions_without_parentheses_end()
            else:
                self.error('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)

    def expressions_without_parentheses_end(self):
        try:
            if self.current_token_class() == 'ART':
                self.end_expression()
            elif self.current_token_class() == 'LOG':
                self.next_token()
                self.logical_expression_begin()
                self.logical_expression_end()
            else:
                pass
        except:
            pass

    # bloco <SIMPLE_OR_DOUBLE_ARITHIMETIC_EXPRESSION_OPTIONAL>
    def simple_or_double_arithmetic_expression_optional(self):
        if self.match_ART_DOUBLE() or self.current_token_class() == 'ART':
            self.simple_or_double_arithmethic_expression()
        else: pass

    # <SIMPLE_OR_DOUBLE_ARITHIMETIC_EXPRESSION>
    def simple_or_double_arithmethic_expression(self):
        try:
            if self.match_ART_DOUBLE():
                self.next_token()
            elif self.current_token_class() == 'ART':
                self.end_expression()
            else:
                self.error('Expected "++" , "--" or <ART>')
        except SyntaxError as e:
            self.write_error(e)
    
    def end_expression(self):
        try:
            if self.current_token_class() == 'ART':
                self.next_token()
                self.part_loop()
            else:
                self.error("Expected '+' , '-' , '*' or '/'")
        except SyntaxError as e:
            self.write_error(e)

    def end_expression_optional(self):
        try:
            if self.current_token_class() == 'ART':
                self.end_expression()
            else:
                pass
        except:
            pass
    
    def simple_expression(self):
        try:
            if self.current_token_class() == 'NRO':
                self.part()
                self.end_expression()
            elif self.current_token_text() == '(':
                self.parenthesis_expression()
            else:
                self.error('Expected "(" or <NRO>')
        except SyntaxError as e:
            self.write_error(e)

    def parenthesis_expression(self):
        try:
            if self.current_token_text() == '(':
                self.next_token()
                self.simple_expression()
                if self.current_token_text() == ')':
                    self.next_token()
                    self.end_expression_optional()
                else:
                    self.error('Expected ")"')
            else:
                self.error('Expected "("')
        except SyntaxError as e:
            self.write_error(e)

    def part_loop(self):
        global expressao
        try:
            if self.current_token_class() == 'NRO' or self.current_token_class() == 'IDE':
                expressao.append(self.current_token_text())
                self.part()
                self.end_expression_optional()
            elif self.current_token_text() == '(':
                self.parenthesis_expression()
            else:
                self.error('Expected <NRO> or "("')
        except SyntaxError as e:
            self.write_error(e)

    def part(self):
        try: 
            if self.current_token_class() == 'NRO':
                self.next_token()
            elif self.current_token_class() == 'IDE':
                self.object_method_or_object_access_or_part()
            else:
                self.error('Expected <NRO> or <IDE>')
        except:
            pass

    # <OBJECT_METHOD_OR_OBJECT_ACCESS> ::= <OBJECT_METHOD_OR_OBJECT_ACCESS_OR_PART> 
    # remoção de ambiguidade
    def object_method_or_object_access_or_part(self):
        self.dec_object_attribute_access()
        self.optional_object_method_access()

    def dec_object_attribute_access(self):
        global erros_semanticos
        global tem_for
        global c
        global m
        try:
            if self.current_token_class() == 'IDE':
                if (tem_for):
                    existe, tipo = self.symbol_table.verificar_varivel_existe(c, m, self.current_token_text(), self.current_token_line())
                    if (existe):
                        if (tipo != 'int'):
                            erros_semanticos.append(f"<{self.current_token_line()}> tipo incompatível <{self.current_token_text()}> <int>")
                            #print(f"<{self.current_token_line()}> tipo incompatível <{self.current_token_text()}> <int>")
                self.next_token()
                self.dimensions()
                self.end_object_attribute_access()
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def method(self):
        global c
        global m
        try:
            if self.current_token_text() == 'void' or self.match_TYPE_VARIABLES():
                self.next_token()
                if self.current_token_class() == 'IDE':
                    m = self.current_token_text()
                    self.symbol_table.add_method(c, self.last_token_text(), self.current_token_text(), self.current_token_line())
                    self.next_token()
                    if self.current_token_text() == '(':
                        self.next_token()
                        self.dec_parameters()
                    else: self.error('Expected "("')
                else: self.error('Expected <IDE>')
            else: self.error('Expected "void" or <IDE> or <TYPE>')
        except SyntaxError as e:
            self.write_error(e=e)
    
    def dec_parameters(self):
        global c
        global m
        try:
            # <END_DEC_PARAMETERS>
            if self.current_token_text() == ')':
                #ver quantidade de parametros 
                self.symbol_table.quantidade_parametros(c, m)
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.method_body()
                else:
                    self.error('Expected "{"')
            # <VARIABLE_PARAM>
            elif self.match_TYPE():
                self.next_token()
                if self.current_token_class() == 'IDE': # fim de var param
                    self.symbol_table.add_param(c, m, self.last_token_text(), self.current_token_text(), self.current_token_line())
                    self.next_token()
                    self.mult_dec_parameters()
                else:
                    self.error('Expected <IDE>')
            # <OBJECT_PARAM>
            elif self.current_token_class() == 'IDE':
                self.next_token()
                if self.current_token_class() == 'IDE':
                    self.symbol_table.add_param(c, m, self.last_token_text(), self.current_token_text(), self.current_token_line())
                    self.next_token()
                    self.mult_dec_parameters()
                else: self.error('Expected <IDE>')
            else:
                self.error('Expected " ) { " or <TYPE> or <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    # <MULT_DEC_PARAMETERS>
    def mult_dec_parameters(self):
        global c
        global m 
        try:
            #   <END_DEC_PARAMETERS>
            if self.current_token_text() == ')':
                self.symbol_table.quantidade_parametros(c, m)
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.method_body()
                else:
                    self.error('Expected "{"')
            elif self.current_token_text() == ',':
                self.next_token()
                if self.match_TYPE_VARIABLES():
                    self.next_token()
                    if self.current_token_class() == 'IDE':
                        self.symbol_table.add_param(c, m, self.last_token_text(), self.current_token_text(), self.current_token_line())
                        self.next_token()
                        self.mult_dec_parameters()
                    else:
                        self.error('Expected <IDE>')
                else:
                    self.error('Expected <TYPE> or <IDE>')
            else:
                self.error('Expected ")" or ","')
        except SyntaxError as e:
            self.write_error(e)

    # <TYPE_VARIABLES>
    def match_TYPE_VARIABLES(self):
        return self.current_token_class() == 'IDE' or self.match_TYPE()
    
    # <METHODS>
    def methods (self):
        #   <TYPES> (primeiro de method)
        if self.current_token_text() == 'void' or self.match_TYPE_VARIABLES():
            self.method()
            self.methods()
        else:
            pass

    def methods_block(self):
        global cond_m 
        try:
            if self.current_token_text() == 'methods':
                cond_m = True
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.methods()
                    if self.current_token_text() == '}':
                        cond_m = False
                        self.next_token()
                    else:
                        self.error('Expected "}"')
                else:
                    self.error('Expected "{"')
            else: 
                self.error('Expected "methods"')
        except SyntaxError as e:
            self.write_error(e)

    #   <COMMANDS> (recursao de <COMMAND>)
    def commands(self):
        primeiro_command = ['print', 'read', 'if', 'for']
        try:
            if (self.current_token_text() in primeiro_command) or (self.current_token_class() == 'IDE'):
                self.command()
                self.commands()
            else:
                pass
        except SyntaxError as e:
            pass

    # Bloco <COMMAND>
    def command(self):
        global expressao 
        global c
        global m
        global tem_for
        try:
            if self.current_token_text() == 'print':
                self.print_begin()
            elif self.current_token_text() == 'read':
                self.read_begin()
            elif self.current_token_class() == 'IDE':
                var = self.current_token_text()
                existe, tipo = self.symbol_table.verificar_varivel_existe(c, m, self.current_token_text(), self.current_token_line())
                self.object_access_or_assignment()
                if self.current_token_text() == ';':
                    if (existe):
                        if tipo == 'int':
                            self.symbol_table.verificar_atr_int(expressao, var, self.current_token_line(), c, m)
                        elif tipo == 'real':
                            self.symbol_table.verificar_atr_real(expressao, var, self.current_token_line(), c, m)
                        elif tipo == 'string': 
                            self.symbol_table.verificar_atr_string(expressao, var, self.current_token_line(), c, m) 
                        elif tipo == 'boolean':
                            self.symbol_table.verificar_atr_boolean(expressao, var, self.current_token_line(), c, m)
                    #self.symbol_table.show_expression()
                    expressao = []
                    self.next_token()
                else:
                    self.error('Expected ";"')
            elif self.current_token_text() == 'if':
                self.IF()
            elif self.current_token_text() == 'for':
                tem_for = True
                self.for_block()
            else:
                self.error('Expected "print" or "read" or "if" or "for" or <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def dec_parameters_constructor(self):
        if self.current_token_class() == 'IDE' or self.match_TYPE():
            self.mult_param_constructor()
            self.mult_dec_parameters_constructor()
        else: pass
    
    def mult_dec_parameters_constructor(self):
        if self.current_token_text() == ',':
            self.next_token()
            self.mult_param_constructor()
            self.mult_dec_parameters_constructor()
        else:
            pass    # prod. vazia

    def mult_param_constructor(self):
        try:
            if self.match_TYPE():
                self.variable_param()
            elif self.current_token_class() == 'IDE':
                self.object_param()
            else:
                self.error('Expected <IDE> or <TYPE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def variable_param(self):
        try:
            if self.match_TYPE():
                self.next_token()
                if self.current_token_class() == 'IDE':
                    self.next_token()
                else: 
                    self.error('Expected <IDE>')
            else:
                self.error('Expected <TYPE>')
        except SyntaxError as e:
            self.write_error(e)

    def object_param(self):
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                if self.current_token_class() == 'IDE':
                    self.next_token()
                else:
                    self.error('Expected <IDE>')
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def mult_parameters(self):
        if self.current_token_text() == ',':
            self.next_token()
            self.value()
            self.mult_parameters()
        else:
            pass    # prod. vazia

    def parameters(self):
        global param
        global c
        global m
        if self.match_value_firsts():
            self.value()
            self.mult_parameters()
            self.symbol_table.verificar_parametros(c, m, param, self.current_token_line())
        else: pass

    def object_access_or_assignment(self):
        self.dec_object_attribute_access()
        self.object_access_or_assignment_end()
    
    def object_access_or_assignment_end(self):
        global var
        global tem_for
        global c
        global m
        try:
            if self.current_token_text() == '=':
                var = self.last_token_text()
                self.next_token()
                if (tem_for):
                    self.symbol_table.verificar_atr_int(self.current_token_text(), var, self.current_token_line(), c, m)
                self.value()
            elif self.match_ART_DOUBLE():
                self.next_token()
            elif self.current_token_text() == '->':
                self.object_method_access_end()
            else:
                self.error('Expected "=" , "++" , "--" or "->"')
        except SyntaxError as e:
            self.write_error(e)

    def main_type(self):
        try:
            if self.match_TYPE():
                self.next_token()
            elif self.current_token_text() == 'void':
                self.next_token()
            else:
                self.error('Expected "void" or <TYPE>')
        except SyntaxError as e:
            self.write_error(e)
    
    #bloco classe

    def class_block(self):
        global c
        try:
            if self.current_token_text() == 'class':
                self.next_token()
                c = self.current_token_text()
                self.symbol_table.add_classe(c, self.current_token_line())
                self.ide_class()
            else:
                self.error('Expected "class"')
        except:
            pass
    
    def ide_class(self):
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                self.extends()
            elif self.current_token_text() == 'main':
                self.main()
            else:
                self.error('Expected <IDE> or "main"')
        except SyntaxError as e:
            self.write_error(e)
    
    def extends(self):
        try:
            if self.current_token_text() == 'extends':
                classe = self.last_token_text() 
                self.next_token()
                self.symbol_table.add_exist_superclass(classe, self.current_token_text(), self.current_token_line())
                if self.current_token_class() == 'IDE':
                    self.next_token()
                    self.start_class_block()
                else:
                    self.error('Expected IDE')
            elif self.current_token_text() == '{':
                self.start_class_block()
            else: self.error('Expected "extends" or "{"')
        except SyntaxError as e:
            self.write_error(e)

    def start_class_block(self):
        try:
            if self.current_token_text() == '{':
                self.next_token()
                self.init_class()
            else:
                self.error('Expected "{"')
        except SyntaxError as e:
            self.write_error(e)
    
    def init_class(self):
        try:
            self.body_blocks()
            self.methods_block()
            self.constructor()
        except SyntaxError as e:
            self.write_error(e)

    def constructor(self):
        try:
            if self.current_token_text() == 'constructor':
                self.next_token()
                if self.current_token_text() == '(':
                    self.next_token()
                    self.dec_parameters_constructor()
                    if self.current_token_text() == ')':
                        self.next_token()
                        if self.current_token_text() == '{':
                            self.next_token()
                            self.variables_block()
                            self.objects_block()
                            self.commands()
                            if self.current_token_text() == '}':
                                self.next_token()
                                self.end_class()
                            else:
                                self.error('Expected "}"')
                        else:
                            self.error('Expected "{"')
                    else:
                        self.error('Expected ")"')
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "constructor"')
        except SyntaxError as e:
            self.write_error(e)
    
    def end_class(self):
        try:
            if self.current_token_text() == '}':
                self.next_token()
                self.class_block()
            else:
                self.error('Expected "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def main(self):
        try:
            if self.current_token_text() == 'main':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.init_main()
                else:
                    self.error('Expected "{"')
            else:
                self.error('Expected "main"')
        except SyntaxError as e:
            self.write_error(e)
    

    def init_main(self):
        try:
            self.body_blocks()
            self.main_methods()
            if self.current_token_text() == '}':
                self.next_token()
            else:
                self.error('Expected "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def body_blocks(self):
        try:
            self.variables_block()
            self.objects_block()
        except SyntaxError as e:
            self.write_error(e)


    # bloco if-else
    def IF(self):
        global tem_if
        global if_var
        global c
        global m
        try:
            if self.current_token_text() == 'if':
                tem_if = True 
                self.next_token()
                if self.current_token_text() ==  '(':
                    self.next_token()
                    self.logical_expression() # <condition> ::= <LOGICAL_EXPRESSION>
                    if self.current_token_text() == ')':
                        tem_if = False
                        self.symbol_table.verificar_atr_boolean(if_var, 'if', self.current_token_line(), c, m)
                        if_var = []
                        self.next_token()
                        if self.current_token_text() == 'then':
                            self.next_token()
                            if self.current_token_text() == '{':
                                self.next_token()
                                self.commands()
                                if self.current_token_text() == '}':
                                    self.next_token()
                                    self.if_else()
                                else:
                                    self.error('Expected "}"')
                            else:
                                self.error('Expected "{"')
                        else:
                            self.error('Expected "then"')
                    else:
                        self.error('Expected ")"')
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "if"')
        except SyntaxError as e:
            self.write_error(e)
    
    def if_else(self):
        try:
            if self.current_token_text() == 'else':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.commands()
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        self.error('Expected "}"')
            else:
                pass #prod vazia
        except SyntaxError as e:
            self.write_error(e)
    
    #print + read

    def print_begin(self):
        try:
            if self.current_token_text() == 'print':
                self.next_token()
                if self.current_token_text() == '(':
                    self.next_token()
                    self.print_end()
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "print"')
        except SyntaxError as e:
            self.write_error(e)
    
    def print_end(self):
        try:
            self.print_parameter()
            if self.current_token_text() == ')':
                self.next_token()
                if self.current_token_text() == ';':
                    self.next_token()
                else:
                    self.error('Expected ";"')
            else:
                self.error('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)
    
    def read_begin(self):
        try:
            if self.current_token_text() == 'read':
                self.next_token()
                if self.current_token_text() == '(':
                    self.next_token()
                    self.read_end()
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "read"')
        except SyntaxError as e:
            self.write_error(e)
    
    def read_end(self):
        try:
            self.dec_object_attribute_access()
            if self.current_token_text() == ')':
                self.next_token()
                if self.current_token_text() == ';':
                    self.next_token()
                else:
                    self.error('Expected ";"')
            else:
                self.error('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)
    

    def print_parameter(self):
        try:
            if self.current_token_class() == 'IDE':
                self.dec_object_attribute_access()
            elif self.current_token_class() == 'CAC' or self.current_token_class() == 'NRO':
                self.next_token()
            else:
                self.error('Expected <DEC_OBJECT_ATTRIBUTE_ACCESS>, <CAC>, or <NRO>')
        except SyntaxError as e:
            self.write_error(e)
    
    #atributos e metodos de objetos 
    def multiple_object_atribute_access(self):
        try:
            self.dec_var()
            self.end_object_attribute_access()
        except SyntaxError as e:
            self.write_error(e)
    
    def end_object_attribute_access(self):
        if self.current_token_text() == '.':
            self.next_token()
            self.multiple_object_atribute_access()
        else:
            pass
            
    def optional_object_method_access(self):
        if self.current_token_text() == '->':
            self.object_method_access_end()
        else:
            pass
    
    def ide_or_constructor(self):
        try:
            if self.current_token_text() == 'constructor' or self.current_token_class() == 'IDE':
                self.next_token()
            else:
                self.error('Expected "constructor" or <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def object_method_access_end(self):
        global c
        global metodo_this
        try:
            if self.current_token_text() == '->':
                metodo_this = True
                #verificar o metodo:
                self.next_token()
                self.symbol_table.verificar_metodo_existe(c, self.current_token_text(), self.current_token_line())
                self.ide_or_constructor()
                if self.current_token_text() == '(':
                    self.next_token()
                    self.parameters()
                    if self.current_token_text() == ')':
                        metodo_this = False
                        self.next_token()
                    else:
                        self.error('Expected ")"')
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "->"')
        except SyntaxError as e:
            self.write_error(e)
    
    #operadores relacionais 
    def relational_expression(self):
        global tem_for
        global c 
        global m
        global erros_semanticos
        try:
            r1 = self.current_token_text()
            self.relational_expression_value()
            if self.current_token_class() == 'REL':
                self.next_token()
                r2 = self.current_token_text()
                self.relational_expression_value()
            else:
                self.error('Expected "<REL>"')
            if (tem_for):
                existe1, tipo1 = self.symbol_table.verificar_varivel_existe(c, m, r1, self.current_token_line())
                existe2, tipo2 = self.symbol_table.verificar_varivel_existe(c, m, r2, self.current_token_line())
                if (existe1):
                    if (tipo1) == 'int':
                        if (existe2):
                            if (tipo2) == 'int':
                                pass
                            else:
                                erros_semanticos.append(f"<{self.current_token_line()}> tipo incompatível <{r2}> <int>")
                                #print(f"<{self.current_token_line()}> tipo incompatível <{r2}> <int>")
                    else:
                        erros_semanticos.append(f"<{self.current_token_line()}> tipo incompatível <{r1}> <int>")
                        #print(f"<{self.current_token_line()}> tipo incompatível <{r1}> <int>")
                

        except SyntaxError as e:
            self.write_error(e)
    
    def relational_expression_value(self):
        try:
            if self.current_token_class() == 'NRO' or self.current_token_class() == 'CAC':
                self.next_token()
            elif self.current_token_class() == 'IDE':
                self.object_method_or_object_access_or_part()
            else:
                self.error('Expected <NRO> , <CAC> or <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    #operadores logicos
    def logical_expression(self):
        self.logical_expression_begin()
        self.logical_expression_end()
    
    def logical_expression_begin(self):
        global expressao
        global tem_if
        global if_var
        try:
            if self.current_token_text() == '!':
                self.next_token()
                self.logical_expression_begin()
            elif self.current_token_text() == '(':
                self.next_token()
                self.logical_expression()
                if self.current_token_text() == ')':
                    self.next_token()
                else:
                    self.error('Expected ")"')
            elif self.match_Bool() or self.current_token_class() == 'IDE':
                if (tem_if):
                    if_var.append(self.current_token_text())
                else:
                    expressao.append(self.current_token_text())
                self.logical_expression_value()
            else:
                self.error('Expected "!" , "(" , <BOOL> or <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def logical_expression_end(self):
        if self.current_token_class() == 'LOG':
            self.next_token()
            self.logical_expression_begin()
            self.logical_expression_end()
        else: pass
    
    def log_rel_optional(self):
        if self.current_token_class() == 'REL':
            self.next_token()
            self.relational_expression_value()
        else: pass

    def logical_expression_value(self):
        try:
            if self.match_Bool():
                self.next_token()
            elif self.current_token_class() == 'IDE':
                self.object_method_or_object_access_or_part()
                self.log_rel_optional()
            else:
                self.error('Expected <BOOL> or <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    #bloco for
    def for_block(self):
        global tem_for
        try:
            self.begin_for()
            self.for_increment()
            self.end_for()
        except SyntaxError as e:
            self.write_error(e)
    
    def assignment(self):
        try:
            if self.current_token_text() == '=':
                self.next_token()
                self.value()
            elif self.current_token_text() in ['--','++']:
                self.next_token()
            else:
                self.error('Expected "=" or "ART_DOUBLE"')
        except SyntaxError as e:
            self.write_error(e)

    def for_increment(self):
        try:
            self.dec_object_attribute_access()
            self.assignment()
        except SyntaxError as e:
            self.write_error(e)
    
    def begin_for(self):
        try:
            if self.current_token_text() == 'for':
                self.next_token()
                if self.current_token_text() == '(':
                    self.next_token()
                    self.object_access_or_assignment()
                    if self.current_token_text() == ';':
                        self.next_token()
                        self.conditional_expression()
                        if self.current_token_text() == ';':
                            self.next_token()
                        else:
                            self.error('Expected ";"')
                    else:
                        self.error('Expected ";"')
                else:
                    self.error('Expected "("')
            else:
                self.error('Expected "for"')
        except SyntaxError as e:
            self.write_error(e)
    
    def end_for(self):
        global tem_for
        try:
            if self.current_token_text() == ')':
                tem_for = False
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.commands()
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        self.error('Expected "}"')
                else:
                    self.error('Expected "{"')
            else:
                self.error('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)
    
    def conditional_expression(self):
        try:
            if self.current_token_text() == '(':
                self.next_token()
                self.relational_expression()
                if self.current_token_text() == ')':
                    self.next_token()
                else:
                    self.error('Expected ")"')
            else:
                self.relational_expression()
        except SyntaxError as e:
            self.write_error(e)
    
    




