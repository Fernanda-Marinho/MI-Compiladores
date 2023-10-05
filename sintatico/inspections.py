
def PROGRAM (symbol, next):
    if CONSTS_BLOCK( symbol, next) and VARIABLES_BLOCK( symbol, next) and CLASS_BLOCK( symbol, next):
        return True
    return False

def CONSTS_BLOCK (symbol):
    if symbol['token_text'] == "const":
        # if next['token_text'] == '{':
            return symbol
    return False

def VARIABLES_BLOCK (symbol, next):
    if symbol['token_text'] == "variables":
        return symbol
    return False

def CLASS_BLOCK (symbol, next):
    return False
