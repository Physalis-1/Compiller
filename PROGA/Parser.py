from lexer import tokens
import ply.yacc as yacc
import AST

precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('nonassoc', 'less','more','equally','lessmore','lessequally','moreequally', 'equallyequally'),
        ('left', 'ARITHMETIC_OPERATOR1'),
        ('left', 'ARITHMETIC_OPERATOR2','DIV','MOD'),
        ('right', 'UMINUS'),
    )

def p_programm(p):
    '''programm : vars subprogram_declarations compound_statement point '''
    p[0] = AST.Node('PROGRAMM', [p[1], p[2], p[3]])

def p_vars(p):
    '''vars : VAR declarations
         | empty '''
    if len(p) == 3:
        p[0] = AST.Node('Var', [p[2]])
    elif len(p)==2:
        p[0] =AST.Node('Var', [p[1]])


def p_declarations(p):
    '''declarations : declarations id_name colon type colonss
                |  id_name colon type colonss '''

    if len(p)==5:
        p[0] = AST.Node('declarations', [p[1], p[3]])
    else:
        p[0] = p[1].add_parts([p[2], p[4]])


def p_id_name(p):
    '''id_name : ID
                | id_name COMMA ID '''
    if len(p) == 2:
        p[0] = AST.Node('ID', [p[1]])

    else:
        p[0] = p[1].add_parts([p[3]])



def p_type(p):
    '''type : INTEGER
                | REAL '''
    p[0] = AST.Node('Type', [p[1]])


def p_subprogram_declarations(p):
    '''subprogram_declarations : subprogram_declarations subprogram_declarat colonss
                | subprogram_declarat colonss
                | empty '''
    if len(p)==3:
        p[0] = AST.Node('subprogram_declarations', [p[1]])
    elif len(p)==2:
        p[0] = AST.Node('subprogram_declarations', [p[1]])
    else :
        p[0] = p[1].add_parts([p[2]])



def p_subprogram_declarat(p):
    '''subprogram_declarat : subprogram_head vars compound_statement  '''
    p[0] = AST.Node('sub_declarate', [p[1], p[2], p[3]])


def p_subprogram_head (p):
    '''subprogram_head : PROCEDURE ID op_bracket parameters cl_bracket  colonss
                    |  FUNCTION ID op_bracket parameters cl_bracket  colon type colonss '''
    if len(p) == 9:
        p[0] = AST.Node('function_head', [p[2], p[4], p[7]])
    elif len(p) == 7:
        p[0] = AST.Node('procedure_head', [p[2], p[4]])


def p_parameters (p):
    '''parameters : id_name colon type
                    | parameters colonss id_name colon type
                    | empty'''
    if len(p) == 4:
        p[0] = AST.Node('parameters', [p[1], p[3]])
    elif len(p)==6:
        p[0] = p[1].add_parts([p[3],p[5]])
    else:
        p[0] = AST.Node('parameters', [p[1]])

def p_compound_statement(p):
    '''compound_statement  : BEGIN statement_list END    '''
    p[0] = AST.Node('compound_statement', [p[2]])


def p_compound_statement1(p):
    '''compound_statement1  : BEGIN statement_list1 END    '''
    p[0] = AST.Node('compound_statement1', [p[2]])


def p_statement_list1 (p):
    '''statement_list1 : statement1 colonss
                    | statement_list1 statement1 colonss'''
    if len(p) == 3:
        p[0] = AST.Node('statement_list1', [p[1]])
    else:
        p[0] = p[1].add_parts([p[2]])


def p_statement_list (p):
    '''statement_list : statement colonss
                    | statement_list statement colonss'''
    if len(p) == 3:
        p[0] = AST.Node('statement_list', [p[1]])
    else:
        p[0] = p[1].add_parts([p[2]])


def p_statement (p):
    '''statement : WRITE op_bracket text cl_bracket
                | WRITE op_bracket elem1 cl_bracket
                | id_name ASSIGN_OPERATOR elem1
                | id_name ASSIGN_OPERATOR function_statement
                | procedure_statement
                | IF expression_list THEN compound_statement1 ELSE compound_statement1
                | WHILE expression_list DO compound_statement1
                | IF expression_list THEN compound_statement1
                '''

    if len(p) == 7:
        p[0] = AST.Node('IF_ELSE', [p[2], p[4], p[6]])
    elif len(p) == 4:
        p[0] = AST.Node('ASSIGN_OPERATOR', [p[1], p[3]])
    elif len(p) == 2:
        p[0] = AST.Node('procedure_statement', [p[1]])
    elif len(p) == 5:
        if p[1]=='while':
            p[0] = AST.Node('WHILE', [p[2], p[4]])
        elif p[1]=='if':
            p[0] = AST.Node('IF', [p[2], p[4]])
        elif p[1] == 'write':
            p[0] = AST.Node('WRITE', [p[3]])


def p_statement1(p):
    '''statement1  : st
                    | statement    '''
    p[0] = AST.Node('statement1', [p[1]])

def p_st(p):
    '''st  : BREAK
             | CONTINUE     '''
    p[0] = AST.Node('BREAK_CONTINUE', [p[1]])


def p_text(p):
    '''text : literal
            | text COMMA literal '''
    if len(p) == 2:
        p[0] = AST.Node('text', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_procedure_statement(p):
    '''procedure_statement : ID op_bracket id_name1 cl_bracket      '''
    p[0] = AST.Node('procedure', [p[1],p[3]])


def p_function_statement (p):
    '''function_statement  : ID op_bracket id_name1 cl_bracket    '''
    p[0] = AST.Node('function_statement', [p[1],p[3]])


def p_id_name1(p):
    '''id_name1 : empty
                | elem1
                | id_name1 COMMA elem1 '''
    if len(p) == 2:
        p[0] = AST.Node('ID', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_expression_list (p):
    '''expression_list  :  expression_list less  expression_list
                        | expression_list more  expression_list
                        | expression_list equally expression_list
                        | expression_list lessmore expression_list
                        | expression_list lessequally expression_list
                        | expression_list moreequally expression_list
                        | expression_list equallyequally expression_list
                        | expression_list expression_list expression_list
                        |  expression_list AND expression_list
                        |  expression_list OR expression_list
                        |  NOT op_bracket  expression_list cl_bracket
                        |  op_bracket  expression_list cl_bracket
                        |  elem1'''
    if len(p) == 2:
        p[0] = AST.Node('expression_list_elem', [p[1]])
    elif len(p)==5:
        p[0] = AST.Node('expression_list_bracket_NOT', [p[1], p[3]])
    else:
        if p[2]=='and' or  p[2]=='or':
            p[0] = AST.Node('AND_OR', [p[1],p[2], p[3]])
        elif p[1]=='(' :
            p[0]=AST.Node('expression_list_bracket', [p[2]])
        else:
            p[0] = AST.Node('comparision', [p[1],p[2], p[3]])


def p_elem(p):
    '''elem : ID
    | integer
    | real '''
    p[0] = AST.Node('element', [p[1]])


def p_elem1(p):

    '''elem1 : elem1 ARITHMETIC_OPERATOR1 elem1
           | elem1 ARITHMETIC_OPERATOR2 elem1
           | elem1 MOD elem1
           | elem1 DIV elem1
           | ARITHMETIC_OPERATOR1 elem1 %prec UMINUS
           | op_bracket elem1  cl_bracket
           | elem'''
    if len(p) == 2:
         p[0] = AST.Node('elem', [p[1]])
    elif len(p) == 4:
        if p[1]=='(':
            p[0] = AST.Node('bracket', [p[2]])
        else:
            p[0] = AST.Node('expression', [p[1], p[2], p[3]])
    else :
        p[0] = AST.Node('unar_operator', [p[1], p[2]])


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print('Unexpected token:', p)

def start_parser(data):
    parser = yacc.yacc()
    elm=parser.parse(data)

    return AST.Node.tree(elm)

if __name__ == '__main__':
    import sys
    parser = yacc.yacc()
    elem = parser.parse(open(sys.argv[1]).read())
    elem=AST.Node.tree(elem)
    for i in range (0, len(elem)):
        print(elem[i])
