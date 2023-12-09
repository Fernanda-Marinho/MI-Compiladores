import re

class AnaliseSintatica():
    def __init__(self, token_collection):
        self.tokens = token_collection
        self.index = 0
        self.errors = []
        self.errors_string = ''

    def start(self):
        self.consts_block()
        self.variables_block()
        self.class_block()
        print(self.errors_string)

    ###############         Funções auxiliares para análise          ###############

    def next_token(self):
        #print(self.current_token())
        self.index +=1

    #   refere-se ao token anterior com relação ao ponteiro
    def last_token(self):
        return self.tokens[self.index-1] if self.index > 0 else self.current_token()

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
                self.next_token()
                if self.current_token_text() == '=':
                    self.next_token()
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
        try:
            if (self.current_token_class() == "IDE"):
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
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                self.dec_var()
                self.multiple_objects()
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def multiple_objects(self):
        try:
            if self.current_token_text() == ';':
                self.next_token()
            elif self.current_token_text() == ',':
                self.next_token()
                self.dec_var()
                self.multiple_objects()
            else:
                self.error('Expected ";" or ","')
        except SyntaxError as e:
            self.write_error(e)

# main

    def main_methods(self):
        try:
            if self.current_token_text() == 'methods':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.main_methods_body()
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        self.error('Expected "}"')
                else:
                    self.error('Expected "{"')
            else:
                self.error('Expected "methods"')
        except SyntaxError as e:
            self.write_error(e)
    
    def main_methods_body(self):
        try:
            self.main_type()
            if self.current_token_text() == 'main':
                self.next_token()
                if self.current_token_text() == '(':
                    self.next_token()
                    if self.current_token_text() == ')':
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
        self.variables_block()
        self.objects_block()
        self.commands_method_body()
        
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

    def value(self): #TODO parei de verificar blocos nessa função
        try:
            if self.current_token_text() == '[':
                self.vector_assign_block()
            elif self.current_token_text() == '!':
                self.logical_expression_begin()
                self.logical_expression_end()
            elif self.current_token_text() == '(':
                self.arithmethic_or_logical_expression_with_parentheses()
            elif self.current_token_class() == 'NRO':
                self.next_token()
                self.simple_or_double_arithmetic_expression_optional()
            elif self.match_Bool():
                self.next_token()
            elif self.current_token_class() == 'CAC':
                self.next_token()
            elif self.current_token_class() == 'IDE':
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
                # TODO verificar qual erro é escrito no final - ou se tds sao escritos
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
        try:
            if self.current_token_class() == 'NRO':
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
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                self.dimensions()
                self.end_object_attribute_access()
            else:
                self.error('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    def method(self):
        try:
            if self.current_token_text() == 'void' or self.match_TYPE_VARIABLES():
                self.next_token()
                if self.current_token_class() == 'IDE':
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
        try:
            # <END_DEC_PARAMETERS>
            if self.current_token_text() == ')':
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
                    self.next_token()
                    self.mult_dec_parameters()
                else:
                    self.error('Expected <IDE>')
            # <OBJECT_PARAM>
            elif self.current_token_class() == 'IDE':
                self.next_token()
                if self.current_token_class() == 'IDE':
                    self.next_token()
                    self.mult_dec_parameters()
                else: self.error('Expected <IDE>')
            else:
                self.error('Expected " ) { " or <TYPE> or <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    # <MULT_DEC_PARAMETERS>
    def mult_dec_parameters(self):
        try:
            #   <END_DEC_PARAMETERS>
            if self.current_token_text() == ')':
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
        try:
            if self.current_token_text() == 'methods':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.methods()
                    if self.current_token_text() == '}':
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
        try:
            if self.current_token_text() == 'print':
                self.print_begin()
            elif self.current_token_text() == 'read':
                self.read_begin()
            elif self.current_token_class() == 'IDE':
                # self.log_rel_optional()
                self.object_access_or_assignment()
                if self.current_token_text() == ';':
                    self.next_token()
                else:
                    self.error('Expected ";"')
            elif self.current_token_text() == 'if':
                self.IF()
            elif self.current_token_text() == 'for':
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
        if self.match_value_firsts():
            self.value()
            self.mult_parameters()
        else: pass

    def object_access_or_assignment(self):
        self.dec_object_attribute_access()
        self.object_access_or_assignment_end()
    
    def object_access_or_assignment_end(self):
        try:
            if self.current_token_text() == '=':
                self.next_token()
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
        try:
            if self.current_token_text() == 'class':
                self.next_token()
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
                self.next_token()
                if self.current_token_class() == 'IDE':
                    self.next_token()
                    self.start_class_block()
                else:
                    self.error('Expected IDE')
            else:
                self.start_class_block()
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
                self.end_class()
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
        try:
            if self.current_token_text() == 'if':
                self.next_token()
                if self.current_token_text() ==  '(':
                    self.next_token()
                    self.logical_expression() # <condition> ::= <LOGICAL_EXPRESSION>
                    if self.current_token_text() == ')':
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
                        print((self.last_token()))
                        print(self.current_token())
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
        try:
            if self.current_token_text() == '.':
                self.next_token()
                self.multiple_object_atribute_access()
            else:
                pass
        except SyntaxError as e:
            self.write_error(e)
    
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
        try:
            if self.current_token_text() == '->':
                self.next_token()
                self.ide_or_constructor()
                if self.current_token_text() == '(':
                    self.next_token()
                    self.parameters()
                    if self.current_token_text() == ')':
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
        try:
            self.relational_expression_value()
            if self.current_token_class() == 'REL':
                self.next_token()
                self.relational_expression_value()
            else:
                self.error('Expected "<REL>"')
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
        if self.current_token_text() == 'REL':
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
        try:
            if self.current_token_text() == ')':
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
    
    



