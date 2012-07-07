#!/usr/bin/env python

import struct
import library
from luatypes import *

FIELDS_PER_FLUSH = 50 # for use by setlist

lua_globals = {
    'assert': library.lua_assert,
    'collectgarbage': library.lua_collectgarbage,
    'dofile': library.lua_dofile,
    'error': library.lua_error,
    '_G': library._G,
    'getfenv': library.lua_getfenv,
    'getmetatable': library.lua_getmetatable,
    'ipairs': library.lua_ipairs,
    'load': library.lua_load,
    'loadfile': library.lua_loadfile,
    'loadstring': library.lua_loadstring,
    'next': library.lua_next,
    'pairs': library.lua_pairs,
    'pcall': library.lua_pcall,
    'print': library.lua_print,
    'rawequal': library.lua_rawequal,
    'rawget': library.lua_rawget,
    'rawset': library.lua_rawset,
    'select': library.lua_select,
    'setfenv': library.lua_setfenv,
    'setmetatable': library.lua_setmetatable,
    'tonumber': library.lua_tonumber,
    'tostring': library.lua_tostring,
    'type': library.lua_type,
    'unpack': library.lua_unpack,
    '_VERSION': library._VERSION, 
    'xpcall': library.lua_xpcall,
    'coroutine': library.coroutine,
    'module': library.module,
    'string': library.string,
    'table': library.table,
    'math': library.math,
    'io': library.io,
    'os': library.os,
    'debug': library.debug,
    }

class Frame:
    def __init__(self, function, registers, upvalues, pc):
        self.function = function
        self.registers = registers
        self.upvalues = upvalues
        self.pc = pc

class Interpreter:
    def __init__(self, lua_object, arg, print_trace=False):
        self.globals = LuaTable(hash=lua_globals)
        self.globals['arg'] = LuaTable(array=arg[1:], hash={0: arg[0]})
        self.top_level_func = lua_object.top_level_func
        self.stack = [] # call stack
        self.done = False
        self.print_trace = print_trace
        self.op_functions = \
            [self.move, self.loadk, self.loadbool, self.loadnil,
             self.getupval, self.getglobal, self.gettable,
             self.setglobal, self.setupval, self.settable,
             self.newtable, self.self_, self.add, self.sub, self.mul,
             self.div, self.mod, self.pow, self.unm, self.not_, self.len,
             self.concat, self.jmp, self.eq, self.lt, self.le,
             self.test, self.testset, self.call, self.tailcall,
             self.return_, self.forloop, self.forprep, self.tforloop,
             self.setlist, self.close, self.closure, self.vararg]

    # runs the top level function
    def run(self):
        # initialize data for current function
        self.function = self.top_level_func
        self.registers = [None for _ in xrange(self.function.max_stack_size)]
        self.upvalues = function.upv if hasattr(self.function, 'upv') else None
        self.pc = 0 # program counter
        # main loop
        while not self.done and self.pc < len(self.function.instructions):
            inst_bytestring = self.function.instructions[self.pc]
            inst = struct.unpack('I', inst_bytestring)[0]
            opcode = inst & 0x0000003f
            self.op_functions[opcode](inst)
            self.pc += 1

    @staticmethod
    def getabc(inst):
        a = (inst >> 6)  & 0x000000ff
        c = (inst >> 14) & 0x000001ff
        b = (inst >> 23) & 0x000001ff
        return (a, b, c)

    @staticmethod
    def getabx(inst):
        a  = (inst >> 6)  & 0x0000003f
        bx = (inst >> 14) & 0x0003ffff
        return (a, bx)

    @staticmethod
    def getasbx(inst):
        a   = (inst >> 6)  & 0x0000003f
        sbx = ((inst >> 14) & 0x0003ffff) - (0x0003ffff >> 1)
        return (a, sbx)

    def move(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = self.registers[b]
        self.trace('MOVE', [a, b], [a])

    def loadk(self, inst):
        a, bx = self.getabx(inst)
        self.registers[a] = self.function.constants[bx]
        self.trace('LOADK', [a, bx], [a])
        
    def loadbool(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = True if b else False
        if c:
            self.pc += 1
        self.trace('LOADBOOL', [a, b, c], [a])

    def loadnil(self, inst):
        a, b, _ = self.getabc(inst)
        for i in xrange(a, b+1):
            self.registers[i] = None
        self.trace('LOADNIL', [a, b], range(a, b+1))

    def getupval(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = self.upvalues[b].value
        self.trace('GETUPVAL', [a, b], [a])

    def getglobal(self, inst):
        a, bx = self.getabx(inst)
        global_name = self.function.constants[bx]
        self.registers[a] = self.globals[global_name]
        self.trace('GETGLOBAL', [a, bx], [a])

    def gettable(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[b]
        index = self.rk(c)
        self.registers[a] = table[index]
        self.trace('GETTABLE', [a, b, c], [a])

    def setglobal(self, inst):
        a, bx = self.getabx(inst)
        global_name = self.function.constants[bx]
        self.globals[global_name] = self.registers[a]
        self.trace('SETGLOBAL', [a, bx], [])

    def setupval(self, inst):
        a, b, _ = self.getabc(inst)
        upv = self.upvalues[b]
        upv.value = self.registers[a]
        # TODO also need to update the original register
        self.trace('SETUPVAL', [a, b], [])

    def settable(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[a]
        index = self.rk(b)
        table[index] = self.rk(c)
        self.trace('SETTABLE', [a, b, c], [])

    def newtable(self, inst):
        a, b, c = self.getabc(inst)
        if b or c:
            b_x =  b & 0x07       # right 3 bits
            b_e = (b & 0xf8) >> 3 # left 5 bits
            c_x =  c * 0x07
            c_e = (c & 0x1f) >> 3
            array_size = b_x if b_e == 0 else (10 + b_x) * (2 ** (b_e - 1))
            hash_size  = c_x if c_e == 0 else (10 + c_x) * (2 ** (c_e - 1))
            array = [None for _ in xrange(array_size)]
            self.registers[a] = LuaTable(array=array, hash={})
        else:
            self.registers[a] = LuaTable(array=[], hash={})
        self.trace('NEWTABLE', [a, b, c], [a])

    def self_(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[b]
        self.registers[a + 1] = b
        self.registers[a] = table[self.rk(c)]
        self.trace('SELF', [a, b, c], [a+1, a])
        
    def add(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) + self.rk(c)
        self.trace('ADD', [a, b, c], [a])

    def sub(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) - self.rk(c)
        self.trace('SUB', [a, b, c], [a])

    def mul(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) * self.rk(c)
        self.trace('MUL', [a, b, c], [a])

    def div(self, inst):
        a, b, c, = self.getabc(inst)
        self.registers[a] = self.rk(b) / self.rk(c)
        self.trace('DIV', [a, b, c], [a])

    def mod(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) % self.rk(c)
        self.trace('MOD', [a, b, c], [a])

    def pow(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) ** self.rk(c)
        self.trace('POW', [a, b, c], [a])

    def unm(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = -self.registers[b]
        self.trace('UNM', [a, b], [a])

    def not_(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = not self.registers[b]
        self.trace('NOT', [a, b], [a])

    def len(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = len(self.registers[b])
        self.trace('LEN', [a, b], [a])

    def concat(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = ''.join([self.registers[i] for i in xrange(b, c+1)])
        self.trace('CONCAT', [a, b, c], [a])

    def jmp(self, inst):
        _, sbx = self.getasbx(inst)
        self.pc += sbx
        self.trace('JMP', [sbx], [])

    def eq(self, inst):
        a, b, c = self.getabc(inst)
        rkb = self.rk(b)
        rkc = self.rk(c)
        if (rkb == rkc) != a:
            self.pc += 1
        self.trace('EQ', [a, b, c], [])

    def lt(self, inst):
        a, b, c = self.getabc(inst)
        rkb = self.rk(b)
        rkc = self.rk(c)
        if (rkb < rkc) != a:
            self.pc += 1
        self.trace('LT', [a, b, c], [])

    def le(self, inst):
        a, b, c = self.getabc(inst)
        rkb = self.rk(b)
        rkc = self.rk(c)
        if (rkb <= rkc) != a:
            self.pc += 1
        self.trace('LE', [a, b, c], [])

    def test(self, inst):
        a, _, c = self.getabc(inst)
        ra = self.registers[a] if a < len(self.registers) else None
        if ra == c:
            self.pc += 1
        self.trace('TEST', [a, c], [])

    def testset(self, inst):
        a, b, c = self.getabc(inst)
        rb = self.registers[b] if b < len(self.registers) else None
        if rb == c:
            self.pc += 1
        else:
            self.registers[a] = rb
        self.trace('TESTSET', [a, b, c], [a] if rb == c else [])

    def call(self, inst):
        a, b, c = self.getabc(inst)
        function = self.registers[a]
        args = []
        if b == 0:
            # parameters are self.registers[a+1] to top of stack
            args.extend(self.registers[a+1:])
        elif b >= 2:
            # there are b-1 parameters
            # so add b-1 parameters from registers to the args list
            args.extend(self.registers[a+1:a+b])
        # call function
        results = self.fcall(function, args)
        # save results here if it was a library function
        modified_regs = []
        is_lua_function = not hasattr(function, '__call__')
        if is_lua_function:
            # store current a and c operand values into this frame,
            # the return instruction will use it
            self.stack[len(self.stack)-1].call_a = a
            self.stack[len(self.stack)-1].call_c = c
        else:
            if c == 0:
                # save return results into registers staring from r[a]
                modified_regs = range(a, len(results))
                for i in xrange(len(results)):
                    self.registers[a + i] = results[i]
            elif c >= 2:
                # save c-1 return results starting from r[a]
                modified_regs = range(a, c-1)
                for i in xrange(c-1):
                    self.registers[a + i] = results[i]
        self.trace('CALL', [a, b, c], modified_regs, is_lua_function)

    def tailcall(self, inst):
        a, b, _ = self.getabc(inst)
        function = self.registers[a]
        args = self.registers[a+1:a+b]
        self.freturn(self.fcall(function, args))
        self.trace('TAILCALL', [a, b], [])

    def return_(self, inst):
        a, b, _ = self.getabc(inst)
        results = []
        if b == 0:
            # results are in registers r[a] onwards
            results.extend(self.registers[a:])
        elif b >= 2:
            # there are b - 1 results starting from r[a]
            results.extend(self.registers[a:b-1])
        # done if the call stack is empty
        if len(self.stack) == 0:
            self.done = True
            return
        # pop last frame
        last_frame = self.stack.pop()
        self.function = last_frame.function
        self.registers = last_frame.registers
        self.upvalues = last_frame.upvalues
        self.pc = last_frame.pc
        a = last_frame.call_a
        c = last_frame.call_c
        if c == 0:
            # save return results into registers staring from r[a]
            for i in xrange(len(results)):
                self.registers[a + i] = results[i]
        elif c >= 2:
            # save c-1 return results starting from r[a]
            for i in xrange(c-1):
                self.registers[a + i] = results[i]
        self.trace('RETURN', [a, b], [], True)
        
    def forloop(self, inst):
        a, sbx = self.getasbx(inst)
        self.registers[a] += self.registers[a+2]
        ra = self.registers[a]
        ra1 = self.registers[a+1]
        ra2 = self.registers[a+2]
        do_loop = False
        if (ra2 > 0 and ra <= ra1) or (ra2 < 0 and ra >= ra1):
            do_loop = True
            self.pc += sbx
            self.registers[a + 3] = ra
        self.trace('FORLOOP', [a, sbx], [a+3] if do_loop else [])

    def forprep(self, inst):
        a, sbx = self.getasbx(inst)
        self.registers[a] -= self.registers[a+2]
        self.pc += sbx
        self.trace('FORPREP', [a, sbx], [a])

    def tforloop(self, inst):
        a, _, c = self.getabc(inst)
        iter_func = self.registers[a]
        state = self.registers[a+1]
        index = self.registers[a+2] if len(self.registers) > a+2 else None
        modified_regs = []
        for i in xrange(a + 3, a + c + 3):
            self.registers[i] = self.fcall(iter_func, [state, index])
            modified_regs.append(i)
        if self.registers[a+3] is not None:
            self.registers[a+2] = self.registers[a+3]
            modified_regs.append(a+2)
        else:
            self.pc += 1
        self.trace('TFORLOOP', [a, c], modified_regs)

    def setlist(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[a]
        if b == 0:
            # set table from elements from r[a+1] to top of stack
            for i in xrange(1, len(self.registers[(a+1):])):
                table[(c-1) * FIELDS_PER_FLUSH + i] = self.registers[a + i]
        else:
            if c == 0:
                # cast next instruction as int and let that be c
                c = self.function.instructions[self.pc+1]
                self.pc += 1 # and skip next instruction as its not an instruction
            for i in xrange(1, b + 1):
                table[(c-1) * FIELDS_PER_FLUSH + i] = self.registers[a + i]
        self.trace('SETLIST', [a, b, c], [])

    def close(self, inst):
        a, _, _ = self.getabc(inst)
        print 'CLOSE NYI'
        self.trace('CLOSE', [a], [])

    def closure(self, inst):
        a, bx = self.getabx(inst)
        self.registers[a] = self.function.prototypes[bx]
        self.function.prototypes[bx].upv = []
        for i in xrange(0, self.function.prototypes[bx].num_upvalues):
            inst_bytestring = self.function.instructions[self.pc + i + 1]
            inst = struct.unpack('I', inst_bytestring)[0]
            opcode = inst & 0x0000003f
            if opcode == 0: # MOVE
                _, b, _ = self.getabc(inst)
                # alias this function's upvalue[i] to registers[b]
            else:
                assert opcode == 4 # GETUPVAL
                _, b, _ = self.getabc(inst)
                # TODO ditto
        self.pc += self.function.prototypes[bx].num_upvalues
        self.trace('CLOSURE', [a, bx], [a])

    def vararg(self, inst):
        a, b, _ = self.getabc(inst)
        argtable = self.registers[self.function.num_parameters] \
            if self.function.is_vararg_flag & 0x2 \
            else None
        modified_regs = []
        for i in xrange(a, len(self.registers) if b == 0 else a+b-1):
            modified_regs.append(i)
            self.registers[i] = argtable[i-a+1] if argtable else None
        self.trace('VARARG', [a, b], modified_regs)

    def fcall(self, function, args):
        if hasattr(function, '__call__'):
            # function is a python function i.e. a native library function
            # so call it like a python function
            return function(args)
        else:
            # otherwise function must be a lua function
            # truncate args list to match number of parameters
            if len(args) > function.num_parameters:
                new_args = args[:function.num_parameters]
                if function.is_vararg_flag & 0x2:
                    # put the extra args in an 'arg' table
                    arg_array = args[function.num_parameters:]
                    arg_hash = {'n': len(arg_array)}
                    arg = LuaTable(array=arg_array, hash=arg_hash)
                    # and set that as the last parameter
                    new_args.append(arg)
                args = new_args
            # push current frame onto stack
            self.stack.append(Frame(self.function, self.registers,
                                    self.upvalues, self.pc))
            # initialize data for current function
            self.function = function
            self.registers = args
            while len(self.registers) < function.max_stack_size:
                self.registers.append(None)
            self.upvalues = function.upv if hasattr(function, 'upv') else None
            self.pc = -1

    def rk(self, o):
        if o & 256:
            return self.function.constants[o-256]
        else:
            return self.registers[o] if o < len(self.registers) else None

    def trace(self, instruction, operands, registers, print_hr=False):
        """ Print trace of an instruction, showing what instruction
        was executed, what the operands were, and what state the
        instruction modified.

        Parameters:
            instruction - The instruction name as a string
            operands - List of the instructions operands as numbers
            registers - List of indicies of registers being modified
                by this instruction
            print_hr - If true, prints a horizontal rule after the trace,
                to separate instructions from different function calls
        """
        if not self.print_trace:
            return
        indent = ' ' * len(self.stack) * 2
        if instruction == 'CALL':
            indent = indent[2:]
        elif instruction == 'RETURN':
            indent = '  ' + indent
        regstr = ' '.join(['r[{}]={}'.format(x, self.registers[x]) for x in registers])
        op0 = operands[0] if len(operands) > 0 else ''
        op1 = operands[1] if len(operands) > 1 else ''
        op2 = operands[2] if len(operands) > 2 else ''
        print '{0}{1:9}  {2:3} {3:3} {4:3}  {5}'.format(
            indent, instruction, op0, op1, op2, regstr)
        if print_hr:
            print '-' * 60

def main():
    import sys
    import parser
    trace = False
    if '--trace' in sys.argv:
        trace=True
        sys.argv.remove('--trace')
    if len(sys.argv) < 2:
        print 'usage: interpreter.py [--trace] lua-file'
        exit(1)
    filename = sys.argv[1]
    if filename[-4:] == '.lua':
        # file is a lua script, compile with luac first
        import subprocess
        subprocess.check_call(['luac', '-o', filename + 'c', filename])
        filename += 'c'
    bcfile = open(filename, 'rb') # r = read, b = binary file
    bytecode = bcfile.read()
    lua_bytecode = parser.LuaBytecode(bytecode)
    interpreter = Interpreter(lua_bytecode, sys.argv[1:], trace)
    interpreter.run()

if __name__ == '__main__':
    main()
