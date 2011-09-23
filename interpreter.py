#!/usr/bin/env python

import struct
import library

FIELDS_PER_FLUSH = 50

opcodes = ['MOVE', 'LOADK', 'LOADBOOL', 'LOADNIL', 'GETUPVAL', 'GETGLOBAL',
           'GETTABLE', 'SETGLOBAL', 'SETUPVAL', 'SETTABLE', 'NEWTABLE', 'SELF',
           'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'UNM', 'NOT', 'LEN',
           'CONCAT', 'JMP', 'EQ', 'LT', 'LE', 'TEST', 'TESTSET', 'CALL',
           'TAILCALL', 'RETURN', 'FORLOOP', 'FORPREP', 'TFORLOOP', 'SETLIST',
           'CLOSE', 'CLOSURE', 'VARARG']

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
        self.inst_size = lua_object.header['size of instruction']
        self.constants = {
            '*toplevel*': lua_object.top_level_func['constants']
            }
        self.globals = LuaTable(hash=lua_globals)
        self.globals['arg'] = LuaTable(array=arg[1:], hash={0: arg[0]})
        self.instructions = {
            '*toplevel*': lua_object.top_level_func['instructions']
            }
        self.registers = []

    def run(self):
        pc = 0 # program counter
        while pc < len(self.instructions['*toplevel*']):
            inst_bytestring = self.instructions['*toplevel*'][pc]
            inst = struct.unpack('I', inst_bytestring)[0]
            opcode = inst & 0x0000003f
            # opcode type 1
            # a = (inst >> 6)  & 0x000000ff
            # c = (inst >> 14) & 0x000001ff
            # b = (inst >> 23) & 0x000001ff
            # opcode type 2
            # a  = (inst >> 6)  & 0x0000003f
            # bx = (inst >> 14) & 0x0003ffff
            # opcode type 3
            # a   = (inst >> 6)  & 0x0000003f
            # sbx = ((inst >> 14) & 0x0003ffff) - (0x0003ffff >> 1)
            if opcode == 0: # MOVE
                a, b, _ = self.getabc(inst)
                self.register_put(a, self.registers[b])
                
            elif opcode == 1: # LOADK
                a, bx = self.getabx(inst)
                self.register_put(a, self.constants['*toplevel*'][bx])

            elif opcode == 2: # LOADBOOL
                a, b, c = self.getabc(inst)
                self.register_put(a, True if b else False)
                if c:
                    pc += 1
                
            elif opcode == 3: # LOADNIL
                a, b, _ = self.getabc(inst)
                for i in xrange(a, b+1):
                    self.register_put(i, None)

            elif opcode == 4: # GETUPVAL
                a, b, _ = self.getabc(inst)
                print 'GETUPVAL NYI'
                
            elif opcode == 5: # GETGLOBAL
                a, bx = self.getabx(inst)
                global_name = self.constants['*toplevel*'][bx]
                self.register_put(a, self.globals[global_name])

            elif opcode == 6: # GETTABLE
                a, b, c = self.getabc(inst)
                table = self.registers[b]
                index = self.rk(c)
                self.register_put(a, table[index])

            elif opcode == 7: # SETGLOBAL
                a, bx = self.getabx(inst)
                global_name = self.constants['*toplevel*'][bx]
                self.globals[global_name] = self.registers[a]

            elif opcode == 8: # SETUPVAL
                a, b, _ = self.getabc(inst)
                print 'SETUPVAL NYI'
                
            elif opcode == 9: # SETTABLE
                a, b, c = self.getabc(inst)
                table = self.registers[a]
                index = self.rk(b)
                table[index] = self.rk(c)

            elif opcode == 10: # NEWTABLE
                a, b, c = self.getabc(inst)
                if b or c:
                    b_x =  b & 0x07       # right 3 bits
                    b_e = (b & 0xf8) >> 3 # left 5 bits
                    c_x =  c * 0x07
                    c_e = (c & 0x1f) >> 3
                    array_size = b_x if b_e == 0 else (10 + b_x) * (2 ** (b_e - 1))
                    hash_size  = c_x if c_e == 0 else (10 + c_x) * (2 ** (c_e - 1))
                    array = [None for _ in xrange(array_size)]
                    self.register_put(a, LuaTable(array=array, hash={}))
                else:
                    self.register_put(a, LuaTable(array=[], hash={}))
                
            elif opcode == 11: # SELF
                a, b, c = self.getabc(inst)
                table = self.registers[b]
                self.register_put(a + 1, b)
                self.register_put(a, table[self.rk(c)]);

            elif opcode == 12: # ADD
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                self.register_put(a, rkb + rkc)
                
            elif opcode == 13: # SUB
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                self.register_put(a, rkb - rkc)

            elif opcode == 14: # MUL
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                self.register_put(a, rkb * rkc)

            elif opcode == 15: # DIV
                a, b, c, = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                self.register_put(a, rkb / rkc)

            elif opcode == 16: # MOD
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                self.register_put(a, rkb % rkc)

            elif opcode == 17: # POW
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                self.register_put(a, rkb**rkc)

            elif opcode == 18: # UNM
                a, b, _ = self.getabc(inst)
                self.register_put(a, -self.registers[b])

            elif opcode == 19: # NOT
                a, b, _ = self.getabc(inst)
                self.register_put(a, not self.registers[b])

            elif opcode == 20: # LEN
                a, b, _ = self.getabc(inst)
                self.register_put(a, len(self.registers[b]))

            elif opcode == 21: # CONCAT
                a, b, c = self.getabc(inst)
                newstr = ''.join([self.registers[i] for i in xrange(b, c+1)])
                self.register_put(a, newstr)

            elif opcode == 22: # JMP
                _, sbx = self.getasbx(inst)
                pc += sbx

            elif opcode == 23: # EQ
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                if (rkb == rkc) != a:
                    pc += 1
                
            elif opcode == 24: # LT
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                if (rkb < rkc) != a:
                    pc += 1

            elif opcode == 25: # LE
                a, b, c = self.getabc(inst)
                rkb = self.rk(b)
                rkc = self.rk(c)
                if (rkb <= rkc) != a:
                    pc += 1

            elif opcode == 26: # TEST
                a, _, c = self.getabc(inst)
                ra = self.registers[a] if a < len(self.registers) else None
                if ra == c:
                    pc += 1

            elif opcode == 27: # TESTSET
                a, b, c = self.getabc(inst)
                rb = self.registers[b] if b < len(self.registers) else None
                if rb == c:
                    pc += 1
                else:
                    self.register_put(a, rb)

            elif opcode == 28: # CALL
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
                results = self.call(function, args)

                if c == 0:
                    # save return results into registers staring from r[a]
                    for i in xrange(len(results)):
                        self.register_put(a+i, results[i])
                elif c == 2:
                    # save c-1 return results starting from r[a]
                    for i in xrange(c-1):
                        self.register_put(a+i, results[i])

            elif opcode == 29: # TAILCALL
                a, b, _ = self.getabc(inst)
                function = self.registers[a]
                args = self.registers[a+1:a+b]
                self.return_(self.call(function, args))

            elif opcode == 30: # RETURN
                a, b, _ = self.getabc(inst)
                results = []
                if b == 0:
                    # results are in registers r[a] onwards
                    results.extend(self.registers[a:])
                elif b >= 2:
                    # there are b - 1 results starting from r[a]
                    results.extend(self.registers[a:b-1])
                self.return_(results)

            elif opcode == 31: # FORLOOP
                a, sbx = self.getasbx(inst)
                self.registers[a] += self.registers[a+2]
                ra = self.registers[a]
                ra1 = self.registers[a+1]
                ra2 = self.registers[a+2]
                if (ra2 > 0 and ra <= ra1) or (ra2 < 0 and ra >= ra1):
                    pc += sbx
                    self.register_put(a+3, ra)

            elif opcode == 32: # FORPREP
                a, sbx = self.getasbx(inst)
                self.registers[a] -= self.registers[a+2]
                pc += sbx

            elif opcode == 33: # TFORLOOP
                a, _, c = self.getabc(inst)
                iter_func = self.registers[a]
                state = self.registers[a+1]
                index = self.registers[a+2] if len(self.registers) > a+2 else None
                for i in xrange(a + 3, a + c + 3):
                    self.register_put(i, self.call(iter_func, [state, index]))
                if self.registers[a+3] is not None:
                    self.registers[a+2] = self.registers[a+3]
                else:
                    pc += 1

            elif opcode == 34: # SETLIST
                a, b, c = self.getabc(inst)
                table = self.registers[a]
                if b == 0:
                    # set table from elements from r[a+1] to top of stack
                    for i in xrange(1, len(self.registers[(a+1):])):
                        table[(c-1) * FIELDS_PER_FLUSH + i] = self.registers[a + i]
                else:
                    if c == 0:
                        # cast next instruction as int and let that be c
                        c = self.instructions['*toplevel*'][pc+1]
                        pc += 1 # and skip next instruction as its not an instruction
                    for i in xrange(1, b + 1):
                        table[(c-1) * FIELDS_PER_FLUSH + i] = self.registers[a + i]

            elif opcode == 35: # CLOSE
                a, _, _ = self.getabc(inst)
                print 'CLOSE NYI'
                
            elif opcode == 36: # CLOSURE
                a, bx = self.getabx(inst)
                print 'CLOSURE NYI'
                
            elif opcode == 37: # VARARG
                a, b, _ = self.getabc(inst)
                if b == 0:
                    # TODO
                    pass
                else:
                    for i in xrange(a, a + b):
                        self.register_put(i, None)

            pc += 1

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

    def register_put(self, i, item):
        while i >= len(self.registers):
            self.registers.append(None)
        self.registers[i] = item

    def call(self, function, args):
        function(args)

    def return_(self, results):
        # TODO do function return
        pass

    def rk(self, o):
        if o & 256:
            return self.constants['*toplevel*'][o-256]
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
    interpreter.run()

if __name__ == '__main__':
    main()
