import re
PRE = ["variables","const", "class", "methods", "objects", "main", "return", "if", "else", "then", "for","read", "print", "void", "int", "real", "boolean", "string", "true", "false"]
DIG = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
LET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y","z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L","M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
ART = ["+", "-", "/", "*", "++", "--"]
REL = ["!=", "==", "<", "<=", ">", ">=", "="]
LOG = ["!", "&&", "||"]
DEL = [";", ",", ".", "(", ")", "[", "]", "{", "}", "->"]
ESP = [" ", "\t","\n"]
SEP = ART+REL+LOG+DEL+ESP

def isLetter(char):
    return bool(re.match(r'[a-zA-Z]', char))

def isDigit(char):
    return bool(re.match(r'[0-9]',char))

def isSep(char):
    # return bool(re.match(r'[\+\-\/\*\+\+\-\-!=<>=!&\|;,.\(\)\[\]\{\}\-> \t\n]', char))
    return (char in SEP)

def isEsp(char):
    return (char in ESP)

def isPre(char):
    return (char in PRE)

def isErrTMF(char):
    return bool(re.match(r'[!-~]',char))

def classifySep(char):
    if (char in DEL): return 'DEL'
    else: return char

def isEOF(char):
    #TODO
    pass