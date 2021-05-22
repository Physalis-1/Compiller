import ply.lex as lex

reserved = {
    # 'program':'PROGRAM',
    'var':'VAR',
    'begin':'BEGIN',
    'end':'END',
    'integer':'INTEGER',
    'real':'REAL',
    'write':'WRITE',
    'if':'IF',
    'then':'THEN',
    'else':'ELSE',
    'while':'WHILE',
    'do':'DO',
    'function':'FUNCTION',
    'procedure':'PROCEDURE',
    'and':'AND',
    'or':'OR',
    'not':'NOT',
    'continue':'CONTINUE',
    'break':'BREAK',
    'div':'DIV',
    'mod':'MOD'


}
tokens = [
    # числа целые
    'integer',
    # числа вещественные
    'real',
    # литерал
    'literal',
    # сравнения
    'more',
    'less',
    'equally',
    'lessmore',
    'lessequally',
     'moreequally',
     'equallyequally',
    # идентификатор
    'ID',
    # оператор присвоения
    'ASSIGN_OPERATOR',
    # двоеточие
    'colon',
    # запятая
    'COMMA',
    # открывается кавычка
    'op_bracket',
    # закрывается кавычка
    'cl_bracket',
    # точка
    'point',
    # точка с запятой
    'colonss',
    # арифметические операторы +|-
    'ARITHMETIC_OPERATOR1',
    # арифметические операторы *|/
    'ARITHMETIC_OPERATOR2'

]+ list(reserved.values())


t_op_bracket = r'\('
t_cl_bracket = r'\)'
t_COMMA=r','
t_ASSIGN_OPERATOR=r'(:=)'
t_colon=r':'
t_colonss=r';'
t_point=r'\.'
t_ARITHMETIC_OPERATOR1=r'\+|\-'
t_ARITHMETIC_OPERATOR2=r'\/|\*'
t_lessmore=r'\<\>'
t_lessequally=r'\<\='
t_moreequally=r'\>\='
t_equallyequally=r'\=\='
t_more=r'\>'
t_less=r'\<'
t_equally=r'\='
def t_ID(t):
    r'[a-zA-Z][0-9a-zA-Z]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_comment(t):
    r'\{(.|\n)*\}'
    pass

def t_comments(t):
    r'\/\/(.)*\n'
    pass

def t_real(t):
    r'(\d)+(\.\d+)'
    t.value = float(t.value)
    return t

def t_integer(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_literal(t):
    r'\'{1,1}.{1,}\'{1,1}'
    t.value = str(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)



t_ignore = ' \t'

def t_error(t):
    print("ОШИБКА СИМВОЛ НЕ ОПОЗНАН '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

if __name__ == '__main__':
    import sys
    data= open(sys.argv[1]).read()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


