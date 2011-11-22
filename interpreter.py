#!/usr/bin/env python

import struct
import library

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

class LuaTable:
    def __init__(self, array=None, hash=None):
        self.array = array or []
        self.hash = hash or {}

    def __getitem__(self, key):
        if isinstance(key, (int, long, float)) and int(key) == key and key > 0:
            key = int(key)
            return self.array[key-1] if len(self.array) >= key-1 else None
        else:
            return self.hash[key] if key in self.hash else None

    def __setitem__(self, key, value):
        if isinstance(key, (int, long, float)) and int(key) == key and key > 0:
            key = int(key)
            while key > len(self.array):
                self.array.append(None)
            self.array[key-1] = value
        else:
            self.hash[key] = value

    def __str__(self):
        return 'array = %s, hash = %s' % (self.array, self.hash)

    def __len__(self):
        return len(self.array)

class Interpreter:
    def __init__(self, lua_object, arg):
        self.globals = LuaTable(hash=lua_globals)
        self.globals['arg'] = LuaTable(array=arg[1:], hash={0: arg[0]})
        self.top_level_func = lua_object.top_level_func
        self.constants = None
        self.instructions = None
        self.prototypes = None
        self.registers = None
        self.upvalues = None
        self.pc = None
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

    def run(self, function, args):
        old_constants = self.constants
        old_instructions = self.instructions
        old_prototypes = self.prototypes
        old_registers = self.registers
        old_upvalues = self.upvalues
        old_pc = self.pc
        self.constants = function.constants
        self.instructions = function.instructions
        self.prototypes = function.prototypes
        self.registers = args
        while len(self.registers) < function.max_stack_size:
            self.registers.append(None)
        self.upvalues = function.upv if hasattr(function, 'upv') else None
        self.pc = 0 # program counter
        while self.pc < len(self.instructions):
            inst_bytestring = self.instructions[self.pc]
            inst = struct.unpack('I', inst_bytestring)[0]
            opcode = inst & 0x0000003f
            self.op_functions[opcode](inst)
            self.pc += 1
        self.constants = old_constants
        self.instructions = old_instructions
        self.prototypes = old_prototypes
        self.registers = old_registers
        self.upvalues = old_upvalues
        self.pc = old_pc

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

    def loadk(self, inst):
        a, bx = self.getabx(inst)
        self.registers[a] = self.constants[bx]
        
    def loadbool(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = True if b else False
        if c:
            self.pc += 1

    def loadnil(self, inst):
        a, b, _ = self.getabc(inst)
        for i in xrange(a, b+1):
            self.registers[i] = None

    def getupval(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = self.upvalues[b]

    def getglobal(self, inst):
        a, bx = self.getabx(inst)
        global_name = self.constants[bx]
        self.registers[a] = self.globals[global_name]

    def gettable(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[b]
        index = self.rk(c)
        self.registers[a] = table[index]

    def setglobal(self, inst):
        a, bx = self.getabx(inst)
        global_name = self.constants[bx]
        self.globals[global_name] = self.registers[a]

    def setupval(self, inst):
        a, b, _ = self.getabc(inst)
        self.upvalues[b] = self.registers[a]

    def settable(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[a]
        index = self.rk(b)
        table[index] = self.rk(c)

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

    def self_(self, inst):
        a, b, c = self.getabc(inst)
        table = self.registers[b]
        self.registers[a + 1] = b
        self.registers[a] = table[self.rk(c)]
        
    def add(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) + self.rk(c)

    def sub(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) - self.rk(c)

    def mul(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) * self.rk(c)

    def div(self, inst):
        a, b, c, = self.getabc(inst)
        self.registers[a] = self.rk(b) / self.rk(c)

    def mod(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) % self.rk(c)

    def pow(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = self.rk(b) ** self.rk(c)

    def unm(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = -self.registers[b]

    def not_(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = not self.registers[b]

    def len(self, inst):
        a, b, _ = self.getabc(inst)
        self.registers[a] = len(self.registers[b])

    def concat(self, inst):
        a, b, c = self.getabc(inst)
        self.registers[a] = ''.join([self.registers[i] for i in xrange(b, c+1)])

    def jmp(self, inst):
        _, sbx = self.getasbx(inst)
        self.pc += sbx

    def eq(self, inst):
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                if (rkb == rkc) != a:
                    self.pc += 1

    def lt(self, inst):
        a, b, c = self.getabc(inst)
        rkb = self.rk(b)
        rkc = self.rk(c)
        if (rkb < rkc) != a:
            self.pc += 1

    def le(self, inst):
        a, b, c = self.getabc(inst)
        rkb = self.rk(b)
        rkc = self.rk(c)
        if (rkb <= rkc) != a:
            self.pc += 1

    def test(self, inst):
        a, _, c = self.getabc(inst)
        ra = self.registers[a] if a < len(self.registers) else None
        if ra == c:
            self.pc += 1

    def testset(self, inst):
        a, b, c = self.getabc(inst)
        rb = self.registers[b] if b < len(self.registers) else None
        if rb == c:
            self.pc += 1
        else:
            self.registers[a] = rb

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
        # call function, saving return values in a list
        results = self.fcall(function, args)
        if c == 0:
            # save return results into registers staring from r[a]
            for i in xrange(len(results)):
                self.registers[a + i] = results[i]
        elif c >= 2:
            # save c-1 return results starting from r[a]
            for i in xrange(c-1):
                self.registers[a + i] = results[i]


    def tailcall(self, inst):
        a, b, _ = self.getabc(inst)
        function = self.registers[a]
        args = self.registers[a+1:a+b]
        self.freturn(self.fcall(function, args))

    def return_(self, inst):
        a, b, _ = self.getabc(inst)
        results = []
        if b == 0:
            # results are in registers r[a] onwards
            results.extend(self.registers[a:])
        elif b >= 2:
            # there are b - 1 results starting from r[a]
            results.extend(self.registers[a:b-1])
        self.freturn(results)
        
    def forloop(self, inst):
        a, sbx = self.getasbx(inst)
        self.registers[a] += self.registers[a+2]
        ra = self.registers[a]
        ra1 = self.registers[a+1]
        ra2 = self.registers[a+2]
        if (ra2 > 0 and ra <= ra1) or (ra2 < 0 and ra >= ra1):
            self.pc += sbx
            self.registers[a + 3] = ra

    def forprep(self, inst):
        a, sbx = self.getasbx(inst)
        self.registers[a] -= self.registers[a+2]
        self.pc += sbx

    def tforloop(self, inst):
        a, _, c = self.getabc(inst)
        iter_func = self.registers[a]
        state = self.registers[a+1]
        index = self.registers[a+2] if len(self.registers) > a+2 else None
        for i in xrange(a + 3, a + c + 3):
            self.registers[i] = self.fcall(iter_func, [state, index])
        if self.registers[a+3] is not None:
            self.registers[a+2] = self.registers[a+3]
        else:
            self.pc += 1

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
                c = self.instructions[self.pc+1]
                self.pc += 1 # and skip next instruction as its not an instruction
            for i in xrange(1, b + 1):
                table[(c-1) * FIELDS_PER_FLUSH + i] = self.registers[a + i]

    def close(self, inst):
        a, _, _ = self.getabc(inst)
        print 'CLOSE NYI'

    def closure(self, inst):
        a, bx = self.getabx(inst)
        self.registers[a] = self.prototypes[bx]
        self.prototypes[bx].upv = []
        for i in xrange(0, self.prototypes[bx].num_upvalues):
            inst_bytestring = self.instructions[self.pc + i + 1]
            inst = struct.unpack('I', inst_bytestring)[0]
            opcode = inst & 0x0000003f
            if opcode == 0: # MOVE
                _, b, _ = self.getabc(inst)
                # alias this function's upvalue[i] to registers[b]
                self.prototypes[bx].upv.append(self.registers[b])
            else:
                assert opcode == 4 # GETUPVAL
                _, b, _ = self.getabc(inst)
                # TODO ditto
        self.pc += self.prototypes[bx].num_upvalues

    def vararg(self, inst):
        a, b, _ = self.getabc(inst)
        if b == 0:
            # TODO
            pass
        else:
            for i in xrange(a, a + b):
                self.registers[i] = None

    def fcall(self, function, args):
        if hasattr(function, '__call__'):
            # function is a python function i.e. a native library function
            # so call it like a python function
            function(args)
        else:
            # otherwise function must be a lua function
            # so call run() with this function
            self.run(function, args)

    def freturn(self, results):
        # TODO do function return
        pass

    def rk(self, o):
        if o & 256:
            return self.constants[o-256]
        else:
            return self.registers[o] if o < len(self.registers) else None


def main():
    import sys
    import parser
    if len(sys.argv) < 2:
        print 'usage: interpreter.py lua-bytecode-file'
        exit(1)
    bcfile = open(sys.argv[1], 'rb') # r = read, b = binary file
    bytecode = bcfile.read()
    lua_bytecode = parser.LuaBytecode(bytecode)
    interpreter = Interpreter(lua_bytecode, sys.argv[1:])
    interpreter.run(interpreter.top_level_func, [])

if __name__ == '__main__':
    main()
