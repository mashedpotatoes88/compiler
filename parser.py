import ply.yacc as yacc
from lexer import CustomLexer

tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULUS', 'EXPONENT',
    'LPAREN', 'RPAREN',
    'ASSIGN', 'TERMINATOR', 'IDENTIFIER',
    'LBRACE', 'RBRACE',
    'DOUBLE', 'INT', 'CONST', 'STR', 'RETURN',
    'IF', 'ELSE', 'WHILE', 'COMMA', 'PRINT'
)


# Grammar

def p_program(p):
    '''program : program_item_list'''
    p[0] = ('program', p[1])

def p_program_item_list(p):
    '''program_item_list : program_item_list program_item
                         | program_item'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_program_item(p):
    '''program_item : declaration
                    | function'''
    p[0] = p[1]

def p_function(p):
    '''function : type IDENTIFIER LPAREN RPAREN compound_stmt'''
    p[0] = ('function', p[1], p[2], p[5])

def p_type(p):
    '''type : INT
            | DOUBLE
            | STR'''
    p[0] = p[1]

def p_const_type(p):
    '''type : CONST type'''
    p[0] = ('const', p[2])

def p_compound_stmt(p):
    '''compound_stmt : LBRACE stmt_list RBRACE'''
    p[0] = ('block', p[2])

def p_stmt_list(p):
    '''stmt_list : stmt_list statement
                 | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | expression_stmt
                 | return_stmt
                 | compound_stmt
                 | if_stmt
                 | while_stmt
                 | func_call_stmt'''
    p[0] = p[1]


def p_declaration(p):
    '''declaration : type IDENTIFIER TERMINATOR
                   | type IDENTIFIER ASSIGN expression TERMINATOR'''
    if len(p) == 4:
        p[0] = ('declare', p[1], p[2])
    else:
        p[0] = ('declare_assign', p[1], p[2], p[4])

def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN expression TERMINATOR'''
    p[0] = ('assign', p[1], p[3])

def p_expression_stmt(p):
    '''expression_stmt : expression TERMINATOR'''
    p[0] = p[1]

def p_return_stmt(p):
    '''return_stmt : RETURN expression TERMINATOR'''
    p[0] = ('return', p[2])

def p_func_call_stmt(p):
    '''func_call_stmt : factor TERMINATOR'''
    if p[1][0] == 'call':
        p[0] = ('func_call', p[1])
    else:
        raise SyntaxError("Expected a function call")

# Expression rules (same as before)
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES power
            | term DIVIDE power
            | term MODULUS power'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_term_power(p):
    'term : power'
    p[0] = p[1]

def p_power_exp(p):
    'power : factor EXPONENT power'
    p[0] = ('binop', p[2], p[1], p[3])

def p_power_factor(p):
    'power : factor'
    p[0] = p[1]

def p_factor_num_or_id(p):
    '''factor : NUMBER
              | IDENTIFIER'''
    if p.slice[1].type == 'NUMBER':
        p[0] = ('num', p[1])
    else:
        p[0] = ('id', p[1])

def p_factor_func_call(p):
    'factor : IDENTIFIER LPAREN arg_list RPAREN'
    p[0] = ('call', p[1], p[3])

def p_factor_group(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN compound_stmt
               | IF LPAREN expression RPAREN compound_stmt ELSE compound_stmt'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

def p_while_stmt(p):
    'while_stmt : WHILE LPAREN expression RPAREN compound_stmt'
    p[0] = ('while', p[3], p[5])

def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
                | expression
                | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}', type={p.type}")
    else:
        print("Syntax error at EOF")

def parse_input(source_code):
    lexer = CustomLexer(source_code)
    parser = yacc.yacc()
    result = parser.parse(lexer=lexer)
    return result

if __name__ == "__main__":
    with open("calc.c") as file:
        source_code = file.read()
        ast = parse_input(source_code)
        print("AST:", ast)
