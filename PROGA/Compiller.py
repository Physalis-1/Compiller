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

    engine = llvm.create_mcjit_compiler(mod, target_machine)


    init_ptr = engine.get_function_address('__init')
    # print(init_ptr)
    init_func = ctypes.CFUNCTYPE(None)(init_ptr)
    init_func()
    main_ptr = engine.get_function_address('__init_main')
    # print(main_ptr)
    main_func = ctypes.CFUNCTYPE(None)(main_ptr)
    main_func()