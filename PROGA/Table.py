import Parser

def branch(part):
    mass=[]
    if type(part)!=str:
        for i in range(0,len(part.parts)):
           mass.append(part.parts[i])
    return mass

def table_scope(tree):
    main_dict={}
    dict1={}
    # table=[]
    # main_table=[]
    datchik1 = []
    # datchik2 = []
    if tree[0].parts[0] != None:
        element=branch(tree[0].parts[0])
        for i in range (0,len(element)):
            for j in range (0, len(element[i].parts)):
                elem=element[i].parts[j]
                if elem!='integer' and  elem!='real':
                    datchik1.append(elem)
                else:
                    for ip in range (0, len(datchik1)):
                        # helps=[]
                        # helps.append(datchik1[ip])
                        # helps.append(elem)
                        # helps.append('global')
                        # helps.append([])
                        # table.append(helps)
                        dict1.update({str(datchik1[ip]):str(elem)})
                    datchik1=[]
        # datchik1=[]
        # datchik1.append('global')
        # datchik1.append(table)
        main_dict.update({'global':dict1})
        dict1 = {}
        # main_table.append(datchik1)
        # table=[]
    if tree[1].parts[0] != None:
        # datchik1=[]
        for i in range (0,len(tree[1].parts)):
            element = branch(tree[1].parts[i])
            if element[0].type=='function_head':
                # helps=[]
                # helps.append(element[0].parts[0])
                # helps.append(element[0].parts[2].parts[0])
                # helps.append(element[0].parts[0])
                # helps.append([])
                # table.append(helps)
                dict1.update({str(element[0].parts[0]): str(element[0].parts[2].parts[0])})
                # print(table)
            if element[0].parts[1].parts[0]!= None:
                datchik1=[]
                for z in range (0, len(element[0].parts[1].parts)):
                    elem=element[0].parts[1].parts[z]
                    for k in range (0, len(elem.parts)):
                        if elem.parts[k] != 'integer' and elem.parts[k]  != 'real':
                            datchik1.append(elem.parts[k])
                        else:
                            for p in range (0, len(datchik1)):
                                # helps=[]
                                # helps.append(datchik1[p])
                                # helps.append(elem.parts[k])
                                # helps.append(element[0].parts[0])
                                # helps.append([])
                                # table.append(helps)
                                dict1.update({str(datchik1[p]): str(elem.parts[k])})
                            datchik1=[]

            if element[1].parts[0] != None:
                datchik1=[]
                for ii in range(0, len(element[1].parts[0].parts)):
                    for jj in range(0, len(element[1].parts[0].parts[ii].parts)):
                        elem=element[1].parts[0].parts[ii].parts[jj]
                        if elem != 'integer' and elem != 'real':
                            datchik1.append(elem)
                        else:
                            for p1 in range (0, len(datchik1)):
                                # helps=[]
                                # helps.append(datchik1[p1])
                                # helps.append(elem)
                                # helps.append(element[0].parts[0])
                                # helps.append([])
                                # table.append(helps)
                                dict1.update({str(datchik1[p1]): str(elem)})
                            # datchik1=[]
            # datchik1 = []
            # if element[0].type == 'function_head':
                # main_dict.update({'func_'+str(element[0].parts[0]):dict1})
                # dict1={}
            # else:
                # main_dict.update({'proc_' + str(element[0].parts[0]):dict1})
                # dict1={}
            main_dict.update({str(element[0].parts[0]): dict1})
            dict1={}
            # main_table.append(datchik1)
            # table=[]
            # datchik1=[]
    return main_dict
    # for i in range (0, len(main_table)):
    #     for j in range (0,len(main_table[i])):
    #         if j==0:
    #             print(main_table[i][j])
    #         else:
    #             for c in range(0, len(main_table[i][j])):
    #                 print(main_table[i][j][c])


