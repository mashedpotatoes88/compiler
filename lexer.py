import re

class Token:
    def __init__(self, type, value, lineno, lexpos):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.lineno}, pos={self.lexpos})"

token_specification = [  
    ('PREPROCESSOR', r'\#.*'),
    ('NUMBER',   r'\d+(\.\d*)?'),
    ('PLUS',     r'\+'), ('MINUS',    r'-'), ('TIMES',    r'\*'), ('DIVIDE',   r'/'), ('MODULUS', r'\%'), ('EXPONENT', r'\^'),    
    ('LPAREN',   r'\('), ('RPAREN',   r'\)'),
    ("ADDRESSOF", r'&'),
    ('SPACE', r'[ \t]+'),         
    ('NEWLINE', r'\n'),

    ('MULTILINE_COMMENT', r'/\*(.*\n*)*?\*/'),
    ('INLINE_COMMENT', r'//[a-zA-Z_][a-zA-Z0-9_]*'),
    ('HASH', r'\#'),
    ('LANGLEDBR', r'<'),
    ('RANGLEDBR', r'>'),

    ('DOUBLE', r'double'),
    ('CONST', r'const'),
    ('CHAR', r'char'),
    ('STR', r'str'),
    ('STRTOD', r'strtod'),

    ('WHILE', r'while'), ('BREAK', r'break'), ('IF', r'if'), ('ELSE', r'else'), ('ELSE_IF', r'else if'),
    ('EQUAL', r'=='), ('INCREMENT', r'\+\+'), ('DECREMENT', r'\-\-'), ('NOT_EQUAL', r'!='),
    ('ASSIGN', r'='), 
    ('LESS_THAN', r'<'), ('LESS_THAN_EQUAL', r'<='), ('GREATER_THAN', r'>'), ('GREATER_THAN_EQUAL', r'>='),
    ('AND', r'&&'), ('OR', r'\|\|'), ('NOT', r'!'),
    ('TERMINATOR', r';'),
    ('COMMA', r','),
    ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('POWER', r'pow'), ('FMOD', r'fmod'), 
    ('DIVISION_ASSIGNMENT', r'/='), ('MULTIPLICATION_ASSIGNMENT', r'\*='), ('ADDITION_ASSIGNMENT', r'\+='), ('SUBTRACTION_ASSIGNMENT', r'\-='),
    ('LBRACKET', r'\['), ('RBRACKET', r'\]'),
    ('FUNCTION', r'function'), ('RETURN', r'return'),
    ('PRINT', r'printf'),
    ('FGET', r'fgets'),
    ('STRING_COMPARE','strncmp'),
    ('EXIT', r'exit'),
    ('TEN_SIG_DIGITS', r'%\.10g'),

    ('IDENTIFIER', r'[a-zA-Z]+[_]*[a-zA-Z0-9]*[_]*'),
    ('MISMATCH', r'.')
]

non_num_tokens = [t[0] for t in token_specification if t[0] != 'NUMBER']
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

def tokenize(code):
    tokens = []
    lineno = 1
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()

        if kind == 'NEWLINE':
            lineno += 1
            continue
        elif kind in ('SPACE', 'MULTILINE_COMMENT', 'INLINE_COMMENT', 'PREPROCESSOR'):
            continue
        elif kind == 'NUMBER':
            value = float(value)

        if kind in non_num_tokens or kind == 'NUMBER':
            token = Token(kind, value, lineno, mo.start())
            tokens.append(token)
        else:
            raise SyntaxError(f'Unexpected character {value!r} at line {lineno}')

    return tokens

class CustomLexer:
    def __init__(self, code):
        self.tokens = tokenize(code)
        self.index = 0

    def token(self):
        if self.index < len(self.tokens):
            tok = self.tokens[self.index]
            self.index += 1
            return tok
        return None
