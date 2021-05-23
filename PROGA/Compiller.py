import os.path
import ctypes
import llvmlite.binding as llvm
def run(llvm_ir):
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()

    pmb = llvm.create_pass_manager_builder()
    pmb.opt_level = 1
    pm = llvm.create_module_pass_manager()
    pmb.populate(pm)
    pm.run(mod)
    engine = llvm.create_mcjit_compiler(mod, target_machine)

    init_ptr = engine.get_function_address('__init')
    init_func = ctypes.CFUNCTYPE(None)(init_ptr)
    init_func()
    main_ptr = engine.get_function_address('main')
    main_func = ctypes.CFUNCTYPE(None)(main_ptr)
    main_func()

def print_table(table):
    for key, value in table.items():
        print(key, value)
        print()

if __name__ == '__main__':
    import sys
    import Parser
    import Table
    import TAC
    import Compiller
    import block_print
    import llvmgen
    text = open(sys.argv[1]).read()
    AST = Parser.start_parser(text)
    # вывод дерева
    # for i in range(0, len(AST)):
    #     print(AST[i])
    table = Table.table_scope(AST)
    # вывод символьной таблицы
    # print_table(table)
    tac = TAC.start(AST, table)
    # вывод промежуточного
    # block_print.start(tac, 0)
    code_gen = llvmgen.generate_llvm(tac)
    # вывод сгенеренного LLVMlite
    # print(code_gen)
    Compiller.run(code_gen)

