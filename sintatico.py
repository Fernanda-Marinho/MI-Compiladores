from ast import Try
import re

class AnaliseSintatica():
    def __init__(self, token_collection):
        self.tokens = token_collection
        self.index = 0
        self.errors = []

    def start(self):
        self.variables_block()

    def next_token(self):
        try:
            if self.index < len(self.tokens): self.index+=1
            else:
                raise Exception()
        except Exception as eof:
            message = f'{eof.args}, {self.current_token_text()} in line {self.current_token_line()}'
            self.errors.append(message)
        

    def current_token(self):
        return self.tokens[self.index] #if self.index < len(self.tokens) else {}

    def current_token_line(self):
        return self.current_token()['n_line']

    def current_token_class(self):
        return self.current_token()['token_class']

    def current_token_text(self):
        return self.current_token()['token_text']
    
    def write_error(self, e: SyntaxError):
        message = f'{e.args}, {self.current_token_text()} in line {self.current_token_line()}'
        self.errors.append(message)
        self.next_token()
        # sincronizar/tratamento de erros (pular token)

    # Bloco <TYPE>
    def match_TYPE(self):
        v = self.current_token_text()
        type_pattern = re.compile(r'^(int|string|real|boolean)')
        return bool(type_pattern.match(v))
    
    # Bloco <VARIABLES_BLOCK>
    def variables_block (self):
        try:
            if self.current_token_text() == 'variables':
                self.next_token()
                if self.current_token_text() == '{':
                    self.next_token()
                    self.variable() #TODO variables
                    if self.current_token_text() == '}':
                        self.next_token()
                    else:
                        raise SyntaxError ('Expected "}"')
                else:
                    raise SyntaxError ('Expected "{"')
        except SyntaxError as e:
            self.write_error(e)
    
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
            else:   # se a declaração não for com dimensões (variavel)
                return True
        except SyntaxError as e:
            self.write_error(e)

    def size_dimension(self):
        try:
            if self.current_token_class() == 'IDE' or self.current_token_class() == 'NRO':
                self.next_token()
            else:
                raise SyntaxError("Expected <NRO> or <IDE>")
        except SyntaxError as e:
            self.write_error(e=e)

    def multi_variables_line(self):
        try:
            if self.current_token() == ';':
                return True
            elif self.current_token() == ',':
                self.next_token()
                self.dec_variable()
                self.multi_variables_line()
            else:
                raise SyntaxError('Expected ";" or ","')
        except SyntaxError as e:
            self.write_error(e=e)


    # <VARIABLE>
    def variable(self):
        try:
            if self.match_TYPE():
                self.next_token()
                if self.dec_variable():
                    self.next_token()
                    self.multi_variables_line()
            else:
                raise SyntaxError('Expected <TYPE>')
        except SyntaxError as e:
            self.write_error(e=e)
    

    #bloco de objetos 
    def objects_block(self):
        try:
            if self.current_token_text() == 'objects':
                self.next_token()
                if self.current_token_text == '{':
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
            elif self.current_token_text == '}':
                return 
            else:
                raise SyntaxError('Expected <IDE> or "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def object(self):
        try:
            if self.current_token_class == 'IDE':
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
            if self.current_token_text == 'class':
                self.next_token()
                self.ide_class 
            else:
                raise SyntaxError('Expected "class"')
        except SyntaxError as e:
            self.write_error(e)
    
    def ide_class(self):
        try:
            if self.current_token_class() == 'IDE':
                self.next_token()
                self.extends()
            else:
                raise SyntaxError('Expected <IDE>')
        except SyntaxError as e:
            self.write_error(e)
    
    def extends(self):
        try:
            if self.current_token_text == 'extends':
                self.next_token()
                if self.current_token_class == 'IDE':
                    self.next_token()
                    self.start_class_block()
                else:
                    raise SyntaxError('Expected IDE')
            else:
                self.start_class_block()
        except SyntaxError as e:
            self.write_error(e)
    

    def start_class_block(self):
        try:
            if self.current_token_text == '{':
                self.next_token()
                self.init_class()
            else:
                raise SyntaxError('Expected "{')
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
            if self.current_token_text == 'constructor':
                self.next_token()
                if self.current_token_text == '(':
                    self.next_token()
                    self.dec_parameters_constructor()
                    if self.current_token_text == ')':
                        self.next_token()
                        if self.current_token_text == '{':
                            self.next_token()
                            self.variables_block()
                            self.objects_block()
                            self.commands()
                            if self.current_token_text == '}':
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
            if self.current_token_text == '}':
                self.next_token()
                self.class_block()
            else:
                raise SyntaxError('Expected "}"')
        except SyntaxError as e:
            self.write_error(e)
    
    def main(self):
        try:
            if self.current_token_text == 'main':
                self.next_token()
                if self.current_token_text == '{':
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
            if self.current_token_text == '}':
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
            if self.current_token_text == 'if':
                self.next_token()
                if self.current_token_text ==  '(':
                    self.next_token()
                    self.condition()
                    if self.current_token_text == ')':
                        self.next_token()
                        if self.current_token_text == 'then':
                            self.next_token()
                            if self.current_token_text == '{':
                                self.next_token()
                                self.commands()
                                if self.current_token_text == '}':
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
            if self.current_token_text == 'else':
                self.next_token()
                if self.current_token_text == '{':
                    self.next_token()
                    self.commands()
                    if self.current_token_text == '}':
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
            if self.current_token_text == 'print':
                self.next_token()
                if self.current_token_text == '(':
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
            if self.current_token_text == ')':
                self.next_token()
                if self.current_token_text == ';':
                    self.next_token()
                else:
                    raise SyntaxError('Expected ";"')
            else:
                raise SyntaxError('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)
    
    def read_begin(self):
        try:
            if self.current_token_text == 'read':
                self.next_token()
                if self.current_token_text == '(':
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
            if self.current_token_text == ')':
                self.next_token()
                if self.current_token_text == ';':
                    self.next_token()
                else:
                    raise SyntaxError('Expected ";"')
            else:
                raise SyntaxError('Expected ")"')
        except SyntaxError as e:
            self.write_error(e)
    

    def print_parameter(self):
        try:
            if self.current_token_class == 'IDE':
                self.dec_object_atribute_access()
            elif self.current_token_class == 'CAC' or self.current_token_class == 'NRO':
                self.next_token()
            else:
                raise SyntaxError('Expected <DEC_OBJECT_ATTRIBUTE_ACCESS>, <CAC>, or <NRO>')
        except SyntaxError as e:
            self.write_error(e)

