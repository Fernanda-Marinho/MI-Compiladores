import re
PRE = ["variables","const", "class", "methods", "objects", "main", "return", "if", "else", "then", "for","read", "print", "void", "int", "real", "boolean", "string", "true", "false"]
DIG = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
LET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y","z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L","M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
ART = ["+", "-", "/", "*", "++", "--"]
REL = ["!=", "==", "<", "<=", ">", ">=", "="]
LOG = ["!", "&&", "||"]
DEL = [";", ",", ".", "(", ")", "[", "]", "{", "}", "->"]
ESP = [" ", "\t","\n"]
SEP = ART+REL+LOG+DEL
POSSIBLE_LOG = ["&", "|"]

def isLetter(char):
    return bool(re.match(r'[a-zA-Z]', char))

def isDigit(char):
    return bool(re.match(r'[0-9]',char))

def isSep(char):
    return ((char in SEP) or (char in ESP))

def isEsp(char):
    return (char in ESP)

def isSepNotEsp(char):
    return (char in SEP)

def isPossibleLog(char):
    return (char in POSSIBLE_LOG)

def isDel(char):
    return (char in SEP)

def isPre(char):
    return (char in PRE)

def isErrTMF(char):     #TODO trocar o uso disso por in range
    return bool(re.match(r'[!-~]',char))

def isErrCMF(char):
    return bool(re.match(r'[#$&%´@^`~]', char))

def isInRange(char):
    ascii_v = ord(char)
    return (ascii_v in range (32,35) or ascii_v in range (35,127))

def isNextSymbolDouble(current, next):
    if f'{current}{next}' in ART:
        return 'ART'
    elif f'{current}{next}' in REL:
        return 'REL'
    elif f'{current}{next}' in LOG:
        return 'LOG'
    else:
        return None

def currentSymbolClass(current):
    if current in ART:
        return 'ART'
    elif current in REL:
        return 'REL'
    elif current in LOG:
        return 'LOG'
    elif current in DEL:
        return 'DEL'
    else:
        return None

def isEOF(char):
    #TODO
    pass