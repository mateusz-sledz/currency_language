import ply.lex as lex
import ply.yacc as yacc
import logging


tokens = (
    'NAME',
    'NUMBER',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'IFEQUALS',
    'EQUALS',
    'LBRACKET',
    'RBRACKET',
    'GREATEREQUAL',
    'LESSEQUAL',
    'NOTEQUAL',
    'GREATER',
    'LESS',
    'COMMA',
    'LCURLY',
    'RCURLY',
    'AND',
    'OR',
    'STRING'
 )

t_IFEQUALS = r'\=='
t_GREATEREQUAL = r'\>='
t_LESSEQUAL = r'\<='
t_NOTEQUAL = r'\!='
t_GREATER = r'\>'
t_LESS = r'\<'
t_EQUALS  = r'\='
t_PLUS    = r'\+'
t_MINUS   = r'\-'
t_MULTIPLY   = r'\*'
t_DIVIDE  = r'\/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r'\,'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_AND = r'\&'
t_OR = r'\|'
t_STRING = r'\".*?\"'


t_ignore = r' '


reserved = {
    'if': 'IF',
    'while': 'WHILE',
    'print': 'PRINT',
    'def': 'DEF',
    'var': 'ASSIGN',
    'return': 'RETURN'
 }

tokens = tuple(tokens) + tuple(reserved.values())


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Parser: Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

#parsing rules

variables = {}
functions = {}
paramlists = {}
tree = []

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'UMINUS'),
    )


def p_program(p):
    '''
    program : statement
            | functionDef
            | program program
    '''

    if p[1] is not None:
        tree.append(p[1])


def p_functionDef(p):
    '''
    functionDef : DEF NAME LPAREN paramlist RPAREN LCURLY statements RCURLY
    '''

    functions[p[2]] = p[7]
    paramlists[p[2]] = p[4]


def p_funstatementsone(p):
    '''
    statements : statement
    '''

    p[0] = p[1]


def p_funstatementsmulti(p):
    '''
    statements : statements statements
    '''

    lista = list(p[2])

    if type(lista[0]) is not tuple:
        lista = tuple(lista)
        x = (tuple(p[1]), tuple(lista))
        p[0] = x
    else:
        lista = [p[1]] + lista
        p[0] = tuple(lista)




def p_paramlist(p):
    '''
    paramlist : empty
              | NAME
              | NAME multipleparams

    '''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if isinstance(p[2], str):
            x = tuple([p[2]])
        elif isinstance(p[2], tuple):
            x = p[2]

        p[0] = tuple([p[1]]) + x


def p_multipleparams(p):
    '''
    multipleparams : COMMA NAME
    '''

    p[0] = p[2]


def p_mulitpleparams2(p):
    '''
    multipleparams : multipleparams multipleparams
    '''

    if type(p[1]) is str and type(p[2]) is str:
        p[0] = (p[1], p[2])
        return
    elif type(p[1]) is str:
        p[1] = (p[1],)
    elif type(p[2]) is str:
        p[2] = (p[2],)
    p[0] = p[1] + p[2]


def p_functioncall(p):
    '''
    functioncall : NAME LPAREN valuelist RPAREN
    '''

    p[0] = ('functioncall', p[1], p[3])


def p_valuelist(p):
    '''
    valuelist : empty
              | expressions
              | expressions multiplevalueslist
    '''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if isinstance(p[2], int):
            x = tuple([p[2]])
        elif isinstance(p[2], tuple):
            if isinstance(p[2][0], str):
                x = tuple([p[2]])
            else:
                x = tuple(p[2])

        p[0] = tuple([p[1]]) + x


def p_multiplevalueslist(p):
    '''
    multiplevalueslist : COMMA expressions
    '''

    p[0] = p[2]


def p_multiplevalueslist2(p):
    '''
    multiplevalueslist : multiplevalueslist multiplevalueslist
    '''

    if type(p[2]) is tuple:
        if isinstance(p[2][0], str):
            lista = list([p[2]])
        else:
            lista = list(p[2])
        lista = [p[1]] + lista
        p[0] = tuple(lista)
    else:
        lista = [p[1]] + [p[2]]

        p[0] = tuple(lista)


def p_if(p):
    '''
    if : IF LPAREN logicexpression RPAREN LCURLY statements RCURLY
    '''

    p[0] = (p[1], p[3], p[6])


def p_while(p):
    '''
    while : WHILE LPAREN logicexpression RPAREN LCURLY statements RCURLY
    '''

    p[0] = (p[1], p[3], p[6])


def p_expressions(p):
    '''
    expressions : expression
                | curExpression
    '''

    p[0] = p[1]


def p_statement(p):
    '''
    statement : assignment
            | declaration
            | printcall
            | functioncall
            | if
            | while
            | return
    '''
    p[0] = p[1]


def p_return(p):
    '''
    return : RETURN expressions
    '''

    p[0] = ('return', p[2])

def p_printcall(p):
    '''
    printcall : PRINT LPAREN NAME RPAREN
              | printstring
    '''

    if len(p) == 5:
        p[0] = ('printvar', p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_printstring(p):
    '''
    printstring : PRINT LPAREN STRING RPAREN
    '''

    x = p[3]
    p[0] = ('printstring', x[1:-1])


def p_declaration_minus(p):
    '''
    declaration : ASSIGN NAME EQUALS MINUS NUMBER
                | ASSIGN NAME EQUALS MINUS NUMBER currency
    '''

    if len(p) == 6:
        p[0] = ('ASSIGN', p[2], -p[5])
    else:
        p[0] = ('ASSIGN', p[2], (p[6], -p[5]))


def p_declaration(p):
    '''
    declaration : ASSIGN NAME EQUALS NUMBER
                | ASSIGN NAME EQUALS NUMBER currency
    '''

    if len(p) == 5:
        p[0] = ('ASSIGN', p[2], p[4])
    else:
        p[0] = ('ASSIGN', p[2], (p[5], p[4]))


def p_assignment(p):
    '''
    assignment : NAME EQUALS curExpression
               | NAME EQUALS expression
    '''

    p[0] = (p[2], p[1], p[3])


def p_assignment_fun(p):
    '''
    assignment : NAME EQUALS functioncall
    '''

    p[0] = ('functionassign', p[1], p[3])


def p_curExpression(p):
    '''
    curExpression : curExpression MULTIPLY expression
                    | expression MULTIPLY curExpression
                    | curExpression DIVIDE expression
                    | curExpression PLUS curExpression
                    | curExpression MINUS curExpression
    '''

    p[0] = (p[2], p[1], p[3])


def p_andexpression(p):
    '''
    andexpression : expression IFEQUALS expression
                  | expression GREATEREQUAL expression
                  | expression LESSEQUAL expression
                  | expression NOTEQUAL expression
                  | expression GREATER expression
                  | expression LESS expression
                  | curExpression IFEQUALS curExpression
                  | curExpression GREATEREQUAL curExpression
                  | curExpression LESSEQUAL curExpression
                  | curExpression NOTEQUAL curExpression
                  | curExpression GREATER curExpression
                  | curExpression LESS curExpression
    '''

    p[0] = (p[2], p[1], p[3])



def p_orexpression(p):
    '''
    orexpression : andexpression
                 | andexpression andmultiple
    '''

    if len(p) == 2:
        p[0] = tuple(p[1])

    if len(p) == 3:
        p[0] = tuple('&') + tuple([p[1]]) + p[2]


def p_andmultiple(p):
    '''
    andmultiple : AND andexpression
    '''

    p[0] = tuple([p[2]])


def p_andmultiple2(p):
    '''
    andmultiple : andmultiple andmultiple
    '''

    p[0] = (p[1] + p[2])


def p_logicexpression(p):
    '''
    logicexpression : orexpression
                    | orexpression ormultiple
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = tuple('|') + tuple([p[1]]) + p[2]


def p_ormultiple(p):
    '''
    ormultiple : OR orexpression
    '''

    p[0] = tuple([p[2]])


def p_ormultiple2(p):
    '''
    ormultiple : ormultiple ormultiple
    '''

    p[0] = (p[1] + p[2])


def p_curExpression_number(p):
    '''
    curExpression : NAME
                  | NUMBER currency
    '''
    if len(p) == 2:
        p[0] = ('var', p[1])
    else:
        p[0] = (p[2], p[1])


def p_currency(p):
    '''
    currency : LBRACKET NAME RBRACKET
    '''
    p[0] = p[2]


def p_empty(p):
    '''
    empty :
    '''

    p[0] = None


def p_error(p):
    print("Syntax error found!")



def p_expression(p):
    '''
    expression : expression MULTIPLY expression
                | expression DIVIDE expression
                | expression PLUS expression
                | expression MINUS expression
    '''

    p[0] = (p[2], p[1], p[3])


def p_expr_uminus(p):
     'expression : MINUS expression %prec UMINUS'
     p[0] = -p[2]


def p_expression_number(p):
    '''
    expression : NUMBER
    '''

    p[0] = p[1]


def p_expression_var(p):
    '''
    expression : NAME
    '''

    p[0] = ('var', p[1])


def restart():
    global tree
    tree = []
    global functions
    functions = {}
    global paramlists
    paramlists = {}


def get_products(program):
    parser = yacc.yacc()

    log = logging.getLogger()
    parser.parse(program, debug=log)

    return tree, functions, paramlists
