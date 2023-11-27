import re 

class AnaliseSintatica():
    def __init__(self, token_collection):
        self.tokens = token_collection
        self.index = 0
        self.errors = []

    def next_token():
        self.index+=1

    def current_token():
        return tokens[index] if index < len(tokens) else None

    def current_line():
        return current_token()['n_line']

    def current_class():
        return current_token()['token_class']

    def current_text():
        return current_token()['token_text']

    
