import ctypes
import tempfile
from llvmlite.ir import (
    Module, IRBuilder, Function, IntType, DoubleType, VoidType, Constant,
    GlobalVariable, FunctionType,
    ArrayType)

from llvmlite import binding

int_type = IntType(32)
float_type = DoubleType()
bool_type = IntType(1)
void_type = VoidType()
break_mass=[]
continue_mass=[]

typemap = {
    'int': int_type,
    'float': float_type,
    'bool': bool_type,
    'void': void_type
}
versions={'fstr':0}
def new_temp(typeobj):
    global versions
    name = "__%s_%d" % (typeobj, versions[typeobj])
    versions[typeobj] += 1
    return name



class GenerateLLVM(object):

    def __init__(self, name='module'):


        self.module = Module(name)
        self.module.triple = binding.get_default_triple()
        self.block = None
        self.builder = None
        self.globals = {}
        self.locals = {}
        self.temps = {}
        self.declare_print()
        self.last_branch = None


    def declare_print(self):

        self.printf= Function(self.module, FunctionType(IntType(32), [IntType(8).as_pointer()], var_arg=True), name="printf")

    def start_function(self, name, rettypename, parmtypenames):
        rettype = typemap[rettypename]
        parmtypes = [typemap[pname] for pname in parmtypenames]
        func_type = FunctionType(rettype, parmtypes)
        self.function = Function(self.module, func_type, name=name)

        self.block = self.function.append_basic_block("entry")
        self.builder = IRBuilder(self.block)

        self.exit_block = self.function.append_basic_block("exit")
        self.locals = {}
        self.temps = {}
        if rettype is not void_type:
            self.locals['return'] = self.builder.alloca(rettype, name="return")

        self.globals[name] = self.function

    def generate_code(self, ircode):
        for opcode, *args in ircode:
            if hasattr(self, 'emit_' + opcode):
                getattr(self, 'emit_' + opcode)(*args)

    def terminate(self):
        if self.last_branch != self.block:
            self.builder.branch(self.exit_block)
        self.builder.position_at_end(self.exit_block)

        if 'return' in self.locals:
            self.builder.ret(self.builder.load(self.locals['return']))
        else:
            self.builder.ret_void()

    def add_block(self, name):
        t=self.function.append_basic_block(name)
        return t

    def set_block(self, block):
        self.block = block
        self.builder.position_at_end(block)

    def cbranch(self, testvar, true_block,false_block):
        self.builder.cbranch(self.temps[testvar], true_block, false_block)

    def branch(self, next_block):
        if self.last_branch != self.block:
            t=self.builder.branch(next_block)
        self.last_branch = self.block

    def emit_literal_int(self, value, target):
        self.temps[target] = Constant(int_type, value)

    def emit_literal_float(self, value, target):
        self.temps[target] = Constant(float_type, value)

    def emit_literal_bool(self, value, target):
        self.temps[target] = Constant(bool_type, value)

    def emit_literal_str(self, value, target):
        value=value+'\0'
        str_val = Constant(ArrayType(IntType(8), len(value)),
                                bytearray(value.encode("utf8")))
        var = self.builder.alloca(str_val.type,name=target)
        self.builder.store(str_val, var)
        self.temps[target] =  var

    def emit_alloc_int(self, name):
        var = self.builder.alloca(int_type, name=name)
        var.initializer = Constant(int_type, 0)
        self.locals[name] = var

    def emit_alloc_float(self, name):
        var = self.builder.alloca(float_type, name=name)
        var.initializer = Constant(float_type, 0)
        self.locals[name] = var


    def emit_global_int(self, name):
        var = GlobalVariable(self.module, int_type, name=name)
        var.initializer = Constant(int_type, 0)
        self.globals[name] = var

    def emit_global_float(self, name):
        var = GlobalVariable(self.module, float_type, name=name)
        var.initializer = Constant(float_type, 0)
        self.globals[name] = var

    def lookup_var(self, name):
        if name in self.locals:
            return self.locals[name]
        else:
            return self.globals[name]

    def emit_load_int(self, name, target):
        self.temps[target] = self.builder.load(self.lookup_var(name), target)

    def emit_load_float(self, name, target):
        self.temps[target] = self.builder.load(self.lookup_var(name), target)


    def emit_store_int(self, source, target):
        self.builder.store(self.temps[source], self.lookup_var(target))

    def emit_store_float(self, source, target):
        self.builder.store(self.temps[source], self.lookup_var(target))


    def emit_add_int(self, left, right, target):
        self.temps[target] = self.builder.add(
            self.temps[left], self.temps[right], target)

    def emit_add_float(self, left, right, target):
        self.temps[target] = self.builder.fadd(
            self.temps[left], self.temps[right], target)

    def emit_sub_int(self, left, right, target):
        self.temps[target] = self.builder.sub(
            self.temps[left], self.temps[right], target)

    def emit_sub_float(self, left, right, target):
        self.temps[target] = self.builder.fsub(
            self.temps[left], self.temps[right], target)

    def emit_mul_int(self, left, right, target):
        self.temps[target] = self.builder.mul(
            self.temps[left], self.temps[right], target)

    def emit_mul_float(self, left, right, target):
        self.temps[target] = self.builder.fmul(
            self.temps[left], self.temps[right], target)

    def emit_divs_int(self, left, right, target):
        self.temps[target] = self.builder.sdiv(
            self.temps[left], self.temps[right], target)

    def emit_div_float(self, left, right, target):
        self.temps[target] = self.builder.fdiv(
            self.temps[left], self.temps[right], target)

    def emit_mod_int(self, left, right, target):
        self.temps[target] = self.builder.srem(
            self.temps[left], self.temps[right], target)


    def emit_uadd_int(self, source, target):
        self.temps[target] = self.builder.add(
            Constant(int_type, 0),
            self.temps[source],
            target)

    def emit_uadd_float(self, source, target):
        self.temps[target] = self.builder.fadd(
            Constant(float_type, 0.0),
            self.temps[source],
            target)

    def emit_usub_int(self, source, target):
        self.temps[target] = self.builder.sub(
            Constant(int_type, 0),
            self.temps[source],
            target)

    def emit_usub_float(self, source, target):
        self.temps[target] = self.builder.fsub(
            Constant(float_type, 0.0),
            self.temps[source],
            target)

    def emit_lt_int(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '<', self.temps[left], self.temps[right], target)

    def emit_lt_float(self, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(
            '<', self.temps[left], self.temps[right], target)

    def emit_le_int(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '<=', self.temps[left], self.temps[right], target)

    def emit_le_float(self, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(
            '<=', self.temps[left], self.temps[right], target)

    def emit_gt_int(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '>', self.temps[left], self.temps[right], target)

    def emit_gt_float(self, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(
            '>', self.temps[left], self.temps[right], target)

    def emit_ge_int(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '>=', self.temps[left], self.temps[right], target)

    def emit_ge_float(self, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(
            '>=', self.temps[left], self.temps[right], target)

    def emit_eq_int(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '==', self.temps[left], self.temps[right], target)

    def emit_eq_bool(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '==', self.temps[left], self.temps[right], target)

    def emit_eq_float(self, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(
            '==', self.temps[left], self.temps[right], target)

    def emit_ne_int(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '!=', self.temps[left], self.temps[right], target)

    def emit_ne_bool(self, left, right, target):
        self.temps[target] = self.builder.icmp_signed(
            '!=', self.temps[left], self.temps[right], target)

    def emit_ne_float(self, left, right, target):
        self.temps[target] = self.builder.fcmp_ordered(
            '!=', self.temps[left], self.temps[right], target)

    def emit_and_bool(self, left, right, target):
        self.temps[target] = self.builder.and_(
            self.temps[left], self.temps[right], target)

    def emit_or_bool(self, left, right, target):
        self.temps[target] = self.builder.or_(
            self.temps[left], self.temps[right], target)

    def emit_not_bool(self, source, target):
        self.temps[target] = self.builder.icmp_signed(
            '==', self.temps[source], Constant(bool_type, 0), target)

    def emit_print_int(self, source):
        value=self.temps[source]
        voidptr_ty = IntType(8).as_pointer()
        type = "%i \n\0"
        const_type = Constant(ArrayType(IntType(8), len(type)),
                        bytearray(type.encode("utf8")))
        global_fmt = GlobalVariable(self.module, const_type.type, name=new_temp('fstr'))
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = const_type
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])

    def emit_print_float(self, source):
        value=self.temps[source]
        voidptr_ty = IntType(8).as_pointer()
        type = "%f \n\0"
        const_type = Constant(ArrayType(IntType(8), len(type)),
                        bytearray(type.encode("utf8")))
        global_fmt = GlobalVariable(self.module, const_type.type, name=new_temp('fstr'))
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = const_type
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])


    def emit_print_str(self, source):
        value=self.temps[source]
        voidptr_ty = IntType(8).as_pointer()
        type = "%s \n\0"
        const_type = Constant(ArrayType(IntType(8), len(type)),
                        bytearray(type.encode("utf8")))
        global_fmt = GlobalVariable(self.module, const_type.type, name=new_temp('fstr'))
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = const_type
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)
        self.builder.call(self.printf, [fmt_arg, value])


    def emit_call_func(self, funcname, *args):
        target = args[-1]
        func = self.globals[funcname]
        argvals = [self.temps[name] for name in args[:-1]]
        self.temps[target] = self.builder.call(func, argvals)

    def emit_call_proc(self, funcname, *args):
        target = void_type
        func = self.globals[funcname]
        argvals = [self.temps[name] for name in args]
        self.temps[target] = self.builder.call(func, argvals)

    def emit_parm_int(self, name, num):
        var = self.builder.alloca(int_type, name=name)
        self.builder.store(self.function.args[num], var)
        self.locals[name] = var

    def emit_parm_float(self, name, num):
        var = self.builder.alloca(float_type, name=name)
        self.builder.store(self.function.args[num], var)
        self.locals[name] = var


    def emit_return_int(self, source):
        self.builder.store(self.temps[source], self.locals['return'])
        self.branch(self.exit_block)

    def emit_return_float(self, source):
        self.builder.store(self.temps[source], self.locals['return'])
        self.branch(self.exit_block)

    def emit_return_void(self):
        self.branch(self.exit_block)


    def emit_int_to_float(self, source, target):
        self.temps[target] = self.builder.sitofp(self.temps[source], DoubleType(),name=target)

class GenerateBlocksLLVM(object):

    def __init__(self, generator):
        self.gen = generator

    def perebor(self, func):
        global continue_mass
        global break_mass
        i=0
        while (i < len(func)):
            if func[i][0]=='if_block':
                i=i+1
                self.visit_IfBlock(func[i])
            elif func[i][0] == 'while_block':
                i = i + 1
                self.visit_WhileBlock(func[i])
            elif func[i][0] == 'break':
                self.gen.branch(break_mass[len(break_mass)-1])
                return
            elif func[i][0] == 'continue':
                self.gen.branch(continue_mass[len(continue_mass)-1])
                return
            else:
                self.visit_BasicBlock([func[i]])
            i=i+1


    def generate_function(self, func):
        func_name=func[0][1]
        if func[0][1]=='__init':
            func_return_type = func[0][2]
            func_parameters=[]
        elif func[0][0]=='proc':
            func_parameters = []
            func_return_type = 'void'
            for i in range (2, len(func[0])):
                func_parameters.append(func[0][i])
        elif func[0][0]=='func':
            func_parameters = []
            func_return_type = func[0][len(func[0])-1]
            for i in range (2, (len(func[0])-1)):
                func_parameters.append(func[0][i])
        self.gen.start_function(func_name, func_return_type, func_parameters)
        if func_name!='main':
            if len(func) >= 2 and type(func[1]) == list:
                self.visit_BasicBlock(func[1])
                self.visit_BasicBlock(func[2])
                self.perebor(func[3])
                self.gen.terminate()
            else:
                self.visit_BasicBlock(func)
                self.gen.terminate()
        else:
            self.perebor(func[1])
            self.gen.terminate()


    def visit_BasicBlock(self, func):
        self.gen.generate_code(func)


    def visit_IfBlock(self, func):
        if_block = self.gen.add_block("if_block")
        self.gen.branch(if_block)
        self.gen.set_block(if_block)
        result=func[0][len(func[0])-1][len(func[0][len(func[0])-1])-1]
        self.gen.generate_code(func[0])
        true_if_block = self.gen.add_block("true_if_block")
        false_if_block = self.gen.add_block("false_if_block")
        end_if_block = self.gen.add_block("end_if_block")
        self.gen.cbranch(result, true_if_block, false_if_block)
        self.gen.set_block(true_if_block)
        self.perebor(func[1])
        self.gen.branch(end_if_block)
        self.gen.set_block(false_if_block)
        self.gen.branch(end_if_block)
        self.gen.set_block(end_if_block)

    def visit_WhileBlock(self, func):
        global continue_mass
        global break_mass
        while_block = self.gen.add_block("while_block")
        self.gen.branch(while_block)
        self.gen.set_block(while_block)
        self.gen.generate_code(func[0])
        result = func[0][len(func[0]) - 1][len(func[0][len(func[0]) - 1]) - 1]
        true_while_block = self.gen.add_block("true_while_block")
        end_while_block = self.gen.add_block("end_while_block")
        self.gen.cbranch(result, true_while_block, end_while_block)
        continue_mass.append(while_block)
        break_mass.append(end_while_block)
        self.gen.set_block(true_while_block)
        self.perebor(func[1])
        self.gen.branch(while_block)
        self.gen.set_block(end_while_block)
        continue_mass.pop()
        break_mass.pop()


def generate_llvm(tac):
    generator = GenerateLLVM()
    blockgen = GenerateBlocksLLVM(generator)

    blockgen.generate_function(tac[0])
    for i in range(0, len(tac[1])):
        blockgen.generate_function(tac[1][i])
    blockgen.generate_function(tac[2])

    llvm_code = str(generator.module)
    with open('tt.ll', 'wb') as f:
        f.write(llvm_code.encode('utf-8'))
        f.flush()
    return str(generator.module)



if __name__ == '__main__':
    import sys
    import Parser
    import Table
    import TAC

    text = open(sys.argv[1]).read()
    AST = Parser.start_parser(text)
    table = Table.table_scope(AST)
    tac = TAC.start(AST, table)
    generate_llvm(tac)
