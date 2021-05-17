import Parser
import Table
import TAC
import Compiller
import block_print
import llvmgen
def start ():
    f = open('testts1.txt')
    AST = Parser.start_parser(f.read())

    # print(AST)
    return AST

def print_table(table):
    for key, value in table.items():
        print(key, value)
        print()

tree=start()
table=Table.table_scope(tree)
# print_table(table)
tac=TAC.start(tree,table)
# block_print.start(tac,0)
code_gen=llvmgen.compile_llvm(tac)
Compiller.run(code_gen)


