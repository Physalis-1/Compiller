def start(tac,id):
    print()
    for i in range (0, len(tac)):
        if type(tac[i])==list:
            start(tac[i],id+4)
        else:
            print(' '*id,tac[i])
