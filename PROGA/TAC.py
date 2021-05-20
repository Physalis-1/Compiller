import Table
import Parser
import copy
float_val=0.0
int_val=0
versions={'int':0,'float':0, 'bool':0,'str':0}

def new_temp(typeobj):
    global versions
    name = "__%s_%d" % (typeobj, versions[typeobj])
    versions[typeobj] += 1
    return name

def elem_in_expr(elem, e, table, func):
    t=[]
    if elem.parts[e].type == 'unar_operator':
        if type(elem.parts[e].parts[1].parts[0].parts[0]) == int:
            temp = new_temp('int')
            t.append(('literal_int', elem.parts[e].parts[1].parts[0].parts[0], temp))
            t.append(('usub_int', temp, new_temp('int')))
        elif type(elem.parts[e].parts[1].parts[0].parts[0]) == float:
            temp = new_temp('float')
            t.append(('literal_float', elem.parts[e].parts[1].parts[0].parts[0], temp))
            t.append(('usub_float', temp, new_temp('float')))
        elif type(elem.parts[e].parts[1].parts[0].parts[0]) == str:
            try:
                type_el = table['global'][elem.parts[e].parts[1].parts[0].parts[0]]
            except KeyError:
                type_el = table[str(func)][elem.parts[e].parts[1].parts[0].parts[0]]
            if type_el == 'integer':
                temp = new_temp('int')
                t.append(('load_int', elem.parts[e].parts[1].parts[0].parts[0], temp))
                t.append(('usub_int', temp, new_temp(str('int'))))
            else:
                temp = new_temp('float')
                t.append(
                    ('load_float', elem.parts[e].parts[1].parts[0].parts[0], temp))
                t.append(('usub_float', temp, new_temp('float')))
    elif elem.parts[e].type == 'elem':

        if type(elem.parts[e].parts[0].parts[0]) == int:
            temp = new_temp('int')
            t.append(('literal_int', elem.parts[e].parts[0].parts[0], temp))

        elif type(elem.parts[e].parts[0].parts[0]) == float:
            temp = new_temp('float')
            t.append(('literal_float', elem.parts[e].parts[0].parts[0], temp))

        elif type(elem.parts[e].parts[0].parts[0]) == str:
            try:
                type_el = table['global'][elem.parts[e].parts[0].parts[0]]
            except KeyError:
                type_el = table[str(func)][elem.parts[e].parts[0].parts[0]]
            if type_el == 'integer':
                temp = new_temp('int')
                t.append(('load_int', elem.parts[e].parts[0].parts[0], temp))

            else:
                temp = new_temp('float')
                t.append(
                    ('load_float', elem.parts[e].parts[0].parts[0], temp))
    return t

def elem_without_expr(elem, table, func):
    t=[]
    if elem.type == 'unar_operator':
        if type(elem.parts[1].parts[0].parts[0]) == int:
            temp = new_temp('int')
            t.append(('literal_int', elem.parts[1].parts[0].parts[0], temp))
            t.append(('usub_int', temp, new_temp('int')))
        elif type(elem.parts[1].parts[0].parts[0]) == float:
            temp = new_temp('float')
            t.append(('literal_float', elem.parts[1].parts[0].parts[0], temp))
            t.append(('usub_float', temp, new_temp('float')))
        elif type(elem.parts[1].parts[0].parts[0]) == str:
            try:
                type_el = table['global'][elem.parts[1].parts[0].parts[0]]
            except KeyError:
                type_el = table[str(func)][elem.parts[1].parts[0].parts[0]]
            if type_el == 'integer':
                temp = new_temp('int')
                t.append(('load_int', elem.parts[1].parts[0].parts[0], temp))
                t.append(('usub_int', temp, new_temp(str('int'))))
            else:
                temp = new_temp('float')
                t.append(
                    ('load_float', elem.parts[1].parts[0].parts[0], temp))
                t.append(('usub_float', temp, new_temp('float')))
    elif elem.type == 'elem':

        if type(elem.parts[0].parts[0]) == int:
            temp = new_temp('int')
            t.append(('literal_int', elem.parts[0].parts[0], temp))
        elif type(elem.parts[0].parts[0]) == float:
            temp = new_temp('float')
            t.append(('literal_float', elem.parts[0].parts[0], temp))
        elif type(elem.parts[0].parts[0]) == str:
            try:
                type_el = table['global'][elem.parts[0].parts[0]]
            except KeyError:
                type_el = table[str(func)][elem.parts[0].parts[0]]
            if type_el == 'integer':
                temp = new_temp('int')
                t.append(('load_int', elem.parts[0].parts[0], temp))
            else:
                temp = new_temp('float')
                t.append(
                    ('load_float', elem.parts[0].parts[0], temp))
    return t

def abstrack_exrp(t1,t2,operator):
    t=[]
    if t1[2]== 'f' and t2[2]=='i':
        u = 'float'
        elem=new_temp(u)
        t.append(('int_to_float',t2,elem))
        t2=elem
    elif t1[2]== 'i' and t2[2]=='f':
        u = 'float'
        elem=new_temp(u)
        t.append(('int_to_float',t1,elem))
        t1=elem
    elif t1[2]== 'i' and t2[2]=='i' and operator=='/':
        u = 'float'
        elem=new_temp(u)
        elem2=new_temp(u)
        t.append(('int_to_float',t1,elem))
        t.append(('int_to_float', t2, elem2))
        t1=elem
        t2=elem2
    else:
        if t1[2] == 'f' :
            u = 'float'
        else:
            u = 'int'
    if operator == '*':
        t.append(('mul_' + u, t1, t2, new_temp(u)))
    elif operator == '/':
        t.append(('div_' + u, t1, t2, new_temp(u)))
    elif operator == '+':
        t.append(('add_' + u, t1, t2, new_temp(u)))
    elif operator == '-':
        t.append(('sub_' + u, t1, t2, new_temp(u)))
    return t

def expression(elem,table,func):
    t=[]
    datchik=0
    if (elem.type == 'expression' and elem.parts[0].type=='expression') or (elem.type == 'expression' and elem.parts[0].type=='bracket')or (elem.type == 'bracket' and elem.parts[0].type=='expression'):
        datchik=1
        t=expression(elem.parts[0],table,func)
        if (len(elem.parts)==3) and ((elem.type == 'expression' and elem.parts[2].type == 'expression') or (
                elem.type == 'expression' and elem.parts[2].type == 'bracket') or (
                elem.type == 'bracket' and elem.parts[2].type == 'expression')):
            t_1 = expression(elem.parts[2], table, func)
            datchik=3
    elif (len(elem.parts)==3) and ((elem.type == 'expression' and elem.parts[2].type == 'expression') or (elem.type == 'expression' and elem.parts[2].type == 'bracket') or (elem.type == 'bracket' and elem.parts[2].type == 'expression')):
        t=expression(elem.parts[2],table,func)
        datchik=2
    else:
        if len(elem.parts) == 1:
            t = copy.deepcopy(elem_in_expr(elem, 0, table, func))
        elif len(elem.parts) == 3:
            t1 = copy.deepcopy(elem_in_expr(elem, 0, table, func))
            t2 = copy.deepcopy(elem_in_expr(elem, 2, table, func))
            for n in range(0, len(t1)):
                t.append(t1[n])
            for n in range(0, len(t2)):
                t.append(t2[n])
            t3 = abstrack_exrp(t1[len(t1) - 1][len(t1[len(t1) - 1]) - 1], t2[len(t2) - 1][len(t2[len(t2) - 1]) - 1],
                               elem.parts[1])
            for iy in range(0, len(t3)):
                t.append(t3[iy])
        return t
    if len(elem.parts)==1:
        return t
    if datchik==1:
        element=t[len(t) - 1][len(t[len(t) - 1]) - 1]
        t2 = copy.deepcopy(elem_in_expr(elem, 2, table, func))
        for n in range(0, len(t2)):
            t.append(t2[n])
        t3 = abstrack_exrp(element, t2[len(t2) - 1][len(t2[len(t2) - 1]) - 1],
                           elem.parts[1])
        for iy in range(0, len(t3)):
            t.append(t3[iy])

    elif datchik == 2:
        t1 = copy.deepcopy(elem_in_expr(elem, 0, table, func))
        element = t[len(t) - 1][len(t[len(t) - 1]) - 1]
        for n in range(0, len(t1)):
            t.append(t1[n])
        t3 = abstrack_exrp(t1[len(t1) - 1][len(t1[len(t1) - 1]) - 1], element,
                           elem.parts[1])
        for iy in range (0,len(t3)):
            t.append(t3[iy])
    elif datchik == 3:
        element = t[len(t) - 1][len(t[len(t) - 1]) - 1]
        element_1 = t_1[len(t_1) - 1][len(t_1[len(t_1) - 1]) - 1]
        for n in range(0, len(t_1)):
            t.append(t_1[n])
        t3 = abstrack_exrp(element, element_1,
                           elem.parts[1])
        for iy in range(0, len(t3)):
            t.append(t3[iy])
    return t

def call_func_proc_param(elem, table, func,types):
    k=[]
    t=[]
    el=[]
    if elem.parts[1].parts[0]!=None:
        for i in range (0, len(elem.parts[1].parts)):
            if elem.parts[1].parts[i].type=='expression':
                k.append(expression(elem.parts[1].parts[i],table,func))
            else:
                k.append(elem_without_expr(elem.parts[1].parts[i],table,func))
    el.append('call_'+types)
    el.append(elem.parts[0])
    for i in range(0, len(k)):
        el.append(k[i][len(k[i])-1][len(k[i][len(k[i])-1])-1])
        for j in range (0,len(k[i])):
            t.append(k[i][j])
    if types=='func':
        if table[elem.parts[0]][elem.parts[0]]=='integer':
            new_el=new_temp('int')
        else:
            new_el=new_temp('float')
        el.append(new_el)
    t.append(tuple(el))
    return t

def assign_bock(elem,table,func):
    store=elem.parts[0].parts[0]
    if elem.parts[1].type=='expression' :
        t = expression(elem.parts[1], table, func)
    elif elem.parts[1].type=='function_statement' :
        t= call_func_proc_param(elem.parts[1], table, func,'func')

    else:
        t=elem_without_expr(elem.parts[1], table, func)
    try:
        type_el = table['global'][store]
    except KeyError:
        type_el = table[str(func)][store]
    if type_el == 'integer':
        t.append(('store_int',t[len(t)-1][len(t[len(t)-1])-1],store))
    else:
        t.append(('store_float',t[len(t)-1][len(t[len(t)-1])-1],store))
    return t

def logic_expr(elem,table,func):
    t=[]
    datchik=0
    datchik2=0
    while (datchik) <= len(elem.parts[0].parts):
        temp=[]
        t1=[]
        t2=[]
        t3=[]
        if elem.parts[0].parts[2+datchik].type=='expression':
            t1=copy.deepcopy(expression(elem.parts[0].parts[2+datchik], table, func))
        else:
            t1=copy.deepcopy(elem_without_expr(elem.parts[0].parts[2+datchik], table, func))
        if (elem.parts[0].parts[4+datchik].type) == 'expression':
            t2 = copy.deepcopy(expression(elem.parts[0].parts[4 + datchik], table, func))
        else:
            t2=copy.deepcopy(elem_without_expr( elem.parts[0].parts[4+datchik], table, func))
        if t1[len(t1)-1][len(t1[len(t1)-1])-1][2] == 'f' and t2[len(t2)-1][len(t2[len(t2)-1])-1][2] == 'i':
            c = 'float'
            el = new_temp(c)
            t3.append(('int_to_float', t2[len(t2)-1][len(t2[len(t2)-1])-1], el))
            t11= t1[len(t1)-1][len(t1[len(t1)-1])-1]
            t22 = el
        elif t1[len(t1)-1][len(t1[len(t1)-1])-1][2] == 'i' and t2[len(t2)-1][len(t2[len(t2)-1])-1][2] == 'f':
            c = 'float'
            el = new_temp(c)
            t3.append(('int_to_float', t1[len(t1)-1][len(t1[len(t1)-1])-1], el))
            t22=t2[len(t2)-1][len(t2[len(t2)-1])-1]
            t11 = el
        elif t1[len(t1)-1][len(t1[len(t1)-1])-1][2] == 'i' and t2[len(t2)-1][len(t2[len(t2)-1])-1][2] == 'i':
            c = 'float'
            el = new_temp(c)
            el2 = new_temp(c)
            t3.append(('int_to_float', t1[len(t1)-1][len(t1[len(t1)-1])-1], el))
            t3.append(('int_to_float', t2[len(t2)-1][len(t2[len(t2)-1])-1], el2))
            t11 = el
            t22 = el2
        else:
            if t1[len(t1)-1][len(t1[len(t1)-1])-1][2]=='f':
                c = 'float'
                t11=t1[len(t1)-1][len(t1[len(t1)-1])-1]
                t22=t2[len(t2)-1][len(t2[len(t2)-1])-1]
            else:
                c = 'int'
                t11 = t1[len(t1) - 1][len(t1[len(t1) - 1]) - 1]
                t22 = t2[len(t2) - 1][len(t2[len(t2) - 1]) - 1]
        if elem.parts[0].parts[3+datchik].type=='comparision':
            if elem.parts[0].parts[3+datchik].parts[0]=='=':
                t3.append(('eq_'+c,t11,t22,new_temp('bool')))
            elif elem.parts[0].parts[3+datchik].parts[0]=='>':
                t3.append(('gt_'+c,t11,t22,new_temp('bool')))
            elif elem.parts[0].parts[3 + datchik].parts[0] == '<':
                t3.append(('lt_'+c,t11,t22,new_temp('bool')))
        elif  elem.parts[0].parts[3+datchik].type=='comparision_x_2':
            if elem.parts[0].parts[3 + datchik].parts[0] == '>' and elem.parts[0].parts[3 + datchik].parts[1] == '=':
                t3.append(('gt_' + c, t11,t22, new_temp('bool')))
            elif elem.parts[0].parts[3 + datchik].parts[0] == '<' and elem.parts[0].parts[3 + datchik].parts[1] == '=':
                    t3.append(('le_' + c, t11,t22, new_temp('bool')))
            elif elem.parts[0].parts[3 + datchik].parts[0] == '<' and elem.parts[0].parts[3 + datchik].parts[1] == '>':
                t3.append(('ne_' + c, t11,t22, new_temp('bool')))
        if elem.parts[0].parts[0 + datchik].parts[0]=='not':
            t3.append(('not_bool',t3[len(t3) - 1][len(t3[len(t3) - 1]) - 1],new_temp('bool')))
        if datchik2>0 :
            t.append(elem.parts[0].parts[datchik-1].parts[0])
        for i in range (0, len(t1)):
            temp.append(copy.deepcopy(t1[i]))
        for i in range (0, len(t2)):
            temp.append(copy.deepcopy(t2[i]))
        for i in range (0, len(t3)):
            temp.append(copy.deepcopy(t3[i]))
        datchik = datchik + 7
        if len(elem.parts[0].parts)>=datchik-7:
            t.append(copy.deepcopy(temp))
        datchik2=datchik2+1

    datchik=1
    if len(t)>1:
        while datchik<len(t):
            if t[datchik]=='and':
                elem1=t[datchik-1][len(t[datchik-1])-1]
                elem1=elem1[len(elem1)-1]
                elem2=t[datchik+1][len(t[datchik+1])-1]
                elem2 = elem2[len(elem2) - 1]
                for i in range (0, len(t[datchik+1])):
                    t[datchik - 1].append(t[datchik+1][i])
                t[datchik-1].append(('and_bool',elem1,elem2,new_temp('bool')))
                t.pop(datchik+1)
                t.pop(datchik)
            else:
                datchik=datchik+2
        datchik=1
        while datchik<len(t):
            if t[datchik]=='or':
                elem1=t[datchik-1][len(t[datchik-1])-1]
                elem1=elem1[len(elem1)-1]
                elem2=t[datchik+1][len(t[datchik+1])-1]
                elem2 = elem2[len(elem2) - 1]
                for i in range (0, len(t[datchik+1])):
                    t[datchik - 1].append(t[datchik+1][i])
                t[datchik-1].append(('or_bool',elem1,elem2,new_temp('bool')))
                t.pop(datchik+1)
                t.pop(datchik)
            else:
                datchik=datchik+2
    return t[0]

def abstract_body(elem,table,func):
    t=[]
    for i in range (0, len(elem.parts)):
        if elem.parts[i].type=='ASSIGN_OPERATOR':
            k=[]
            k=assign_bock(elem.parts[i],table,func)
            for j in range (0, len(k)):
                t.append(k[j])
        elif elem.parts[i].type == 'BREAK_CONTINUE':
            if elem.parts[i].parts[0]=='break':
                t.append(('break', ))
            else:
                t.append(('continue',))
        elif elem.parts[i].type == 'procedure_statement':
            k=[]
            k = call_func_proc_param(elem.parts[i].parts[0], table, func, 'proc')
            for j in range (0, len(k)):
                t.append(k[j])
        elif elem.parts[i].type=='WRITE':
            if elem.parts[i].parts[0].type=='text':
                v=new_temp('str')
                t.append(('literal_str', elem.parts[i].parts[0].parts[0],v))
                t.append(('print_str',v))
            else:
                if elem.parts[i].parts[0].type=='expression':
                    k=[]
                    k=expression(elem.parts[i].parts[0], table, func)
                    for j in range(0, len(k)):
                        t.append(k[j])
                else:
                    k=[]
                    k=elem_without_expr(elem.parts[i].parts[0], table, func)
                    for j in range(0, len(k)):
                        t.append(k[j])
                if k[len(k)-1][len(k[len(k)-1])-1][2]=='i':
                    c='int'
                elif k[len(k)-1][len(k[len(k)-1])-1][2]=='f':
                    c='float'
                t.append(('print_'+c,k[len(k)-1][len(k[len(k)-1])-1]))
        else:
            if elem.parts[i].type=='IF':
                t.append(('if_block',))
            elif elem.parts[i].type=='WHILE':
                t.append(('while_block',))
            k=[]
            k1=[]
            for z in range (0,len(elem.parts[i].parts[1].parts[0].parts)):
                k.append(abstract_body(elem.parts[i].parts[1].parts[0].parts[z],table,func))
            for z in range (0, len(k)):
                for z1 in range (0, len(k[z])):
                    k1.append(k[z][z1])
            t.append([logic_expr(elem.parts[i],table,func), k1])
    return t

def start(tree,table):
    global int_val
    global float_val
    block=[[],[],[]]
    block[0].append(('func','__init', 'void'))
    # VAR
    if tree[0].parts[0]!=None:
        for i in range(0,len(tree[0].parts[0].parts),2):
            for j in range (0, len(tree[0].parts[0].parts[i].parts)):
                if tree[0].parts[0].parts[i+1].parts[0]=='integer':
                    c='int'
                    x = int_val
                else:
                    c='float'
                    x = float_val
                str_lit=new_temp(c)
                block[0].append(('global_'+c,tree[0].parts[0].parts[i].parts[j]))
                block[0].append(('literal_'+c, x, str_lit))
                block[0].append(('store_'+c,str_lit, tree[0].parts[0].parts[i].parts[j]))
        block[0].append(('return_void',))
                # table['global'][tree[0].parts[0].parts[i].parts[j]][1]=copy.deepcopy(str_lit)
    # function
    if tree[1].parts[0] != None:
        for i in range (0, len(tree[1].parts)):
            temporary=[]
            types=[]
            params=[]
            id=0
            if tree[1].parts[i].parts[0].parts[1].parts[0]!=None:
                for j in range (0,len(tree[1].parts[i].parts[0].parts[1].parts),2):
                    for k  in range (0,len(tree[1].parts[i].parts[0].parts[1].parts[j].parts)):

                        if tree[1].parts[i].parts[0].parts[1].parts[j+1].parts[0]=='integer':
                            types.append('int')
                            params.append(('parm_int',tree[1].parts[i].parts[0].parts[1].parts[j].parts[k],id))
                            id = id + 1
                        elif tree[1].parts[i].parts[0].parts[1].parts[j+1].parts[0]=='real':
                            types.append('float')
                            params.append(('parm_float',tree[1].parts[i].parts[0].parts[1].parts[j].parts[k],id))
                            id = id + 1

            if tree[1].parts[i].parts[0].type == 'function_head':
                if tree[1].parts[i].parts[0].parts[2].parts[0]=='integer':
                    types.append('int')
                else:
                    types.append('float')
            if tree[1].parts[i].parts[0].type == 'function_head':
                types.insert(0,tree[1].parts[i].parts[0].parts[0])
                types.insert(0,'func')
            else:
                types.insert(0,tree[1].parts[i].parts[0].parts[0])
                types.insert(0,'proc')
            if len(params)==0:
                # types.append(('None'))
                params.append(('None',))


            temporary.append(params)
            temporary_var=[]
            # var functions
            if tree[1].parts[i].parts[0].type == 'function_head':
                if tree[1].parts[i].parts[0].parts[2].parts[0] == 'integer':
                    c = 'int'
                    x = int_val
                else:
                    c = 'float'
                    x = float_val
                str_lit = new_temp(c)
                temporary_var.append(('alloc_' + c, tree[1].parts[i].parts[0].parts[0]))
                temporary_var.append(('literal_' + c, x, str_lit))
                temporary_var.append(
                    ('store_' + c, str_lit, tree[1].parts[i].parts[0].parts[0]))
            if tree[1].parts[i].parts[1].parts[0] != None:
                # if tree[1].parts[i].parts[0].type == 'function_head':
                #     if tree[1].parts[i].parts[0].parts[2].parts[0]== 'integer':
                #         c = 'int'
                #         x = int_val
                #     else:
                #         c = 'float'
                #         x = float_val
                #     str_lit = new_temp(c)
                #     temporary_var.append(('alloc_' + c, tree[1].parts[i].parts[0].parts[0]))
                #     temporary_var.append(('literal_' + c, x, str_lit))
                #     temporary_var.append(
                #         ('store_' + c, str_lit, tree[1].parts[i].parts[0].parts[0]))

                # print(tree[1].parts[i].parts[0].parts[0])
                # print(tree[1].parts[i].parts[0].parts[2].parts[0])
                for i1 in range(0, len(tree[1].parts[i].parts[1].parts[0].parts), 2):
                    for j1 in range(0, len(tree[1].parts[i].parts[1].parts[0].parts[i1].parts)):
                        if tree[1].parts[i].parts[1].parts[0].parts[i1 + 1].parts[0] == 'integer':
                            c = 'int'
                            x = int_val
                        else:
                            c = 'float'
                            x = float_val
                        str_lit = new_temp(c)
                        temporary_var.append(('alloc_' + c, tree[1].parts[i].parts[1].parts[0].parts[i1].parts[j1]))
                        temporary_var.append(('literal_' + c, x, str_lit))
                        temporary_var.append(
                            ('store_' + c, str_lit, tree[1].parts[i].parts[1].parts[0].parts[i1].parts[j1]))
                        # table[tree[1].parts[i].parts[0].parts[0]][
                        #     tree[1].parts[i].parts[1].parts[0].parts[i1].parts[j1]][1] = copy.deepcopy(str_lit)
            if len(temporary_var)==0:
                temporary_var.append('None')

        # тело

            tt=abstract_body(tree[1].parts[i].parts[2].parts[0],table,tree[1].parts[i].parts[0].parts[0])
            if tree[1].parts[i].parts[0].type == 'function_head':
                type_el = table[tree[1].parts[i].parts[0].parts[0]][tree[1].parts[i].parts[0].parts[0]]
                if type_el == 'integer':
                    temp = new_temp('int')
                    ez='int'
                else:
                    temp = new_temp('float')
                    ez='float'
                tt.append(('load_'+ez,tree[1].parts[i].parts[0].parts[0],temp))
                tt.append(('return_'+ez,temp))
            else:
                tt.append(('return_void', ))
            block[1].append([tuple(types),params,temporary_var,tt])
    tt = abstract_body(tree[2].parts[0], table, 'global')
    tt.append(('return_void',))
    block[2].append(tt)
    block[2].insert(0,('func', '__init_main', 'void'))
    return block
    # for i in range (0, len(block)):
    #     print(block[i])
    #     print()
    #     print()

