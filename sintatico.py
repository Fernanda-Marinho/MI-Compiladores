from os import error
import re

class AnaliseSintatica():
    def __init__(self, token_collection):
        self.tokens = token_collection
        self.index = 0
        self.errors = []
        self.errors_string = ''

    def start(self):
        # self.consts_block()
        # self.variables_block()
        self.class_block()
        print(self.errors_string)

    ###############         Funções auxiliares para análise          ###############

    def next_token(self):
        print(self.current_token())
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
        message = f'{e.msg}, {self.current_token_text()} in line {self.tokens[self.index-1]["n_line"]}'
        self.errors.append(message)
        self.errors_string = f'{self.errors_string} \n {message}'
        # sincronizar/tratamento de erros

    def error(self, text):
        raise SyntaxError (text)

    ###############         Produções da gramática          ###############

    # Terminais <TYPE>
    def match_TYPE(self):
        v = self.current_token_text()
        type_pattern = re.compile(r'^(int|string|real|boolean)')
        return bool(type_pattern.match(v))
    
    # Terminais <ATTRIBUTION>
    def match_ATTRIBUTION(self):
        v = self.current_token_text()
        return isinstance(v, (int, float, complex, str, bool))

    # Bloco <CONSTS_BLOCK>
    def consts_block(self):
        try: 
            if self.current_token_text() == 'const':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.consts()
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        self.error('Expected "}"')
                else:
                    self.error('Expected "{"')
        except SyntaxError as e:
            self.write_error(e)

    #   CONSTS (recursao para gerar varias)
    def consts(self):
        try:
            if self.current_token_text() == "}":
                pass
            else:
                self.const()
                self.consts()
        except SyntaxError as e:
            pass    # o erro já foi escrito na função invocada antes

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
                    self.variable()
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        raise SyntaxError ('Expected "}"')
                else:
                    raise SyntaxError ('Expected "{"')
        except SyntaxError as e:
            self.write_error(e)

    #   Bloco <VARIABLE>
    def variable(self):
        try:
            if self.match_TYPE():
                self.next_token()
                self.dec_variable() #
                self.multi_variables_line()  #
            elif self.current_token_text() == '}':
                pass
            else:
                raise SyntaxError('Expected <TYPE>')
        except SyntaxError as e:
            self.write_error(e=e)
    
    # Bloco <DEC_VAR>   declaracao de variavel
    def dec_variable(self):
        try:
            if (self.current_token_class() == "IDE"):
                self.next_token()
                self.dimensions()
            else:
                raise SyntaxError('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)

    #   Bloco <DIMENSIONS>
    def dimensions(self):
        try:
            if self.current_token() == '[':
                self.next_token()
                self.size_dimension()
                if self.current_token() == "]":
                    self.next_token()
                    self.dimensions()   # r a direita
                else:
                    raise SyntaxError('Expected "]"')
        except SyntaxError as e:
            self.write_error(e)

    #   <SIZE_DIMENSION>
    def size_dimension(self):
        try:
            if self.current_token_class() == 'IDE' or self.current_token_class() == 'NRO':
                self.next_token()
            else:
                raise SyntaxError("Expected <NRO> or <IDE>")
        except SyntaxError as e:
            self.write_error(e=e)

    #   <MULTI_VARIABLES_LINE>
    def multi_variables_line(self):
        try:
            if self.current_token_text() == ';':
                self.next_token()
            elif self.current_token_text() == ',':
                self.next_token()
                self.dec_variable()
                self.multi_variables_line()
            else:
                raise SyntaxError('Expected ";" or ","')
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
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        raise SyntaxError('Expected "}"')
                else:
                    raise SyntaxError('Expected "{"')
        except SyntaxError as e:
            self.write_error(e)    
    

    def objects(self): #duvida nesse 
        try:
            if self.current_token_class() == 'IDE':
                self.object()
                self.multiple_objects()
            elif self.current_token_text() == '}':
                return 
            else:
                raise SyntaxError('Expected <IDE> or "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def object(self):
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                self.dec_variable()
                self.multiple_objects()
            else:
                raise SyntaxError('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def multiple_objects(self):
        try:
            if self.current_token_text() == ';':
                self.next_token()
            elif self.current_token_text() == ',':
                self.next_token()
                self.dec_variable()
                self.multiple_objects()
            else:
                raise SyntaxError('Expected ";" or ","')
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
                        raise SyntaxError('Expected "}"')
                else:
                    raise SyntaxError('Expected "{"')
            else:
                raise SyntaxError('Expected "methods"')
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
                            if self.current_token_text() == '}':
                                self.next_token()
                            else:
                                raise SyntaxError('Expected "}"')
                        else:
                            raise SyntaxError('Expected "{"')
                    else:
                        raise SyntaxError('Expected ")"')
                else:
                    raise SyntaxError('Expected "("')
            else:
                raise SyntaxError('Expected "main"')
        except SyntaxError as e:
            self.write_error(e)
    
    def method_body(self):
        self.variables_block()
        self.objects_block()
        self.commands_method_body() # TODO

    def commands_method_body(self):     # TODO
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
    
    def return_block(self):
        pass        # TODO

    def value(self):
        pass        #   TODO

    def method(self):
        try:
            if self.current_token_text() == 'void' or self.current_token_class() == 'IDE' or self.match_TYPE():
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
            if self.current_token_text() == ')':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.method_body()
                else:
                    self.error('Expected "{"')
            elif self.match_TYPE():
                self.next_token()
                if self.current_token_class() == 'IDE': # fim de var param
                    self.next_token()
                    self.mult_dec_parameters()
                else:
                    self.error('Expected <IDE>')
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

    def mult_dec_parameters(self):
        try:
            if self.current_token_text() == ')':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.method_body()
                else:
                    self.error('Expected "{"')
            elif self.current_token_text() == ',':
                self.next_token()
                if self.match_TYPE() or self.current_token_class() == 'IDE':
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

    def methods (self):
        try:
            if self.match_TYPE():
                self.method()
                self.methods()
            else:
                pass
        except SyntaxError as e:
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
        except SyntaxError as e:
            self.write_error(e)

    def dec_parameters_constructor(self):
        pass    #   TODO
    def commands(self):
        pass    #TODO
    def dec_object_atribute_access(self):
        pass    #TODO
    def object_method_or_object_access_or_part(self):
        pass #      TODO
    def parameters(self):
        pass        # TODO 
    def object_access_or_assignment(self):
        pass # TODO


    def main_type(self):
        try:
            if self.current_token_text() == 'void':
                self.next_token()
            else:
                self.type()
        except SyntaxError as e:
            self.write_error(e)
    
    #bloco classe

    def class_block(self):
        try:
            if self.current_token_text() == 'class':
                self.next_token()
                self.ide_class()
            else:
                raise SyntaxError('Expected "class"')
        except SyntaxError as e:
            self.write_error(e)
    
    def ide_class(self):
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                self.extends()
            elif self.current_token_text() == 'main':
                self.main()
            else:
                raise SyntaxError('Expected <IDE> or "main"')
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
                    raise SyntaxError('Expected IDE')
            elif self.current_token_text() == '{':
                self.start_class_block()
            else:
                self.error('Expected "extends" or "{"')
        except SyntaxError as e:
            self.write_error(e)

    def start_class_block(self):
        try:
            if self.current_token_text() == '{':
                self.next_token()
                self.init_class()
            else:
                raise SyntaxError('Expected "{"')
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
                                raise SyntaxError('Expected "}"')
                        else:
                            raise SyntaxError('Expected "{"')
                    else:
                        raise SyntaxError('Expected ")"')
                else:
                    raise SyntaxError('Expected "("')
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
                raise SyntaxError('Expected "}"')
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
                    raise SyntaxError('Expected "{"')
            else:
                raise SyntaxError('Expected "main"')
        except SyntaxError as e:
            self.write_error(e)
    

    def init_main(self):
        try:
            self.body_blocks()
            self.main_methods()
            if self.current_token_text() == '}':
                self.next_token()
            else:
                raise SyntaxError('Expected "}"')
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
                    self.condition()
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
                                    raise SyntaxError('Expected "}"')
                            else:
                                raise SyntaxError('Expected "{"')
                        else:
                            raise SyntaxError('Expected "then"')
                    else:
                        raise SyntaxError('Expected ")"')
                else:
                    raise SyntaxError('Expected "("')
            else:
                raise SyntaxError('Expected "if"')
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
                        raise SyntaxError('Expected "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def condition(self):
        try:
            self.logical_expression()
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
                    raise SyntaxError('Expected "("')
            else:
                raise SyntaxError('Expected "print"')
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
                    raise SyntaxError('Expected ";"')
            else:
                raise SyntaxError('Expected ")"')
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
                    raise SyntaxError('Expected "("')
            else:
                raise SyntaxError('Expected "read"')
        except SyntaxError as e:
            self.write_error(e)
    
    def read_end(self):
        try:
            self.dec_object_atribute_access()
            if self.current_token_text() == ')':
                self.next_token()
                if self.current_token_text() == ';':
                    self.next_token()
                else:
                    raise SyntaxError('Expected ";"')
            else:
                raise SyntaxError('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)
    

    def print_parameter(self):
        try:
            if self.current_token_class() == 'IDE':
                self.dec_object_atribute_access()
            elif self.current_token_class() == 'CAC' or self.current_token_class() == 'NRO':
                self.next_token()
            else:
                raise SyntaxError('Expected <DEC_OBJECT_ATTRIBUTE_ACCESS>, <CAC>, or <NRO>')
        except SyntaxError as e:
            self.write_error(e)
    
    #atributos e metodos de objetos 
    def multiple_object_atribute_access(self):
        try:
            self.dec_variable()
            self.end_object_attribute_access()
        except SyntaxError as e:
            self.write_error(e)
    
    def end_object_attribute_access(self):
        try:
            if self.current_token_text() == '.':
                self.next_token()
                self.multiple_object_atribute_access()
        except SyntaxError as e:
            self.write_error(e)
    
    def object_method_or_object_access(self):
        try:
            self.object_method_or_object_access_or_part()
        except SyntaxError as e:
            self.write_error(e)
    
    def optional_object_method_access(self):
        try:
            self.object_method_access_end()
        except SyntaxError as e:
            self.write_error(e)
    
    def ide_or_constructor(self):
        try:
            if self.current_token_text() == 'constructor' or self.current_token_class() == 'IDE':
                self.next_token()
            else:
                raise SyntaxError('Expected "constructor" or <IDE>')
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
                            raise SyntaxError('Expected ")"')
                    else:
                        raise SyntaxError('Expected "("')
                else:
                    raise SyntaxError('Expected "->"')
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
                raise SyntaxError('Expected "<REL>"')
        except SyntaxError as e:
            self.write_error(e)
    
    def relational_expression_value(self):
        try:
            if self.current_token_class() == 'NRO' or self.current_token_class() == 'CAC':
                self.next_token()
            else:
                self.object_method_or_object_access()
        except SyntaxError as e:
            self.write_error(e)
    
    #operadores logicos
    def logical_expression(self):
        try:
            self.logical_expression_begin()
            self.logical_expression_end()
        except SyntaxError as e:
            self.write_error(e)
    
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
                    raise SyntaxError('Expected ")"')
            else:
                self.logical_expression_value()
        except SyntaxError as e:
            self.write_error(e)
    
    def logical_expression_end(self):
        try:
            if self.current_token_class() == 'LOG':
                self.next_token()
                self.logical_expression_begin()
                self.logical_expression_end()
        except SyntaxError as e:
            self.write_error(e)
    
    def log_rel_optional(self):
        try:
            if self.current_token_text() == 'REL':
                self.next_token()
                self.relational_expression_value()
        except SyntaxError as e:
            self.write_error(e)
    
    def logical_expression_value(self):
        try:
            if self.current_token_text() in ['true','false']:
                self.next_token()
            else:
                self.object_method_or_object_access()
                self.log_rel_optional()
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
                raise SyntaxError('Expected "=" or "ART_DOUBLE"')
        except SyntaxError as e:
            self.write_error(e)

    def for_increment(self):
        try:
            self.dec_object_atribute_access()
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
                            raise SyntaxError('Expected ";"')
                    else:
                        raise SyntaxError('Expected ";"')
                else:
                    raise SyntaxError('Expected "("')
            else:
                raise SyntaxError('Expected "for"')
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
                        raise SyntaxError('Expected "}"')
                else:
                    raise SyntaxError('Expected "{"')
            else:
                raise SyntaxError('Expected ")"')
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
                    raise SyntaxError('Expected ")"')
            else:
                self.relational_expression()
        except SyntaxError as e:
            self.write_error(e)
    
    



