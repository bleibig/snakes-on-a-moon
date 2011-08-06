#!/usr/bin/env python

import struct

opcodes = ['MOVE', 'LOADK', 'LOADBOOL', 'LOADNIL', 'GETUPVAL', 'GETGLOBAL',
           'GETTABLE', 'SETGLOBAL', 'SETUPVAL', 'SETTABLE', 'NEWTABLE', 'SELF',
           'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'UNM', 'NOT', 'LEN',
           'CONCAT', 'JMP', 'EQ', 'LT', 'LE', 'TEST', 'TESTSET', 'CALL',
           'TAILCALL', 'RETURN', 'FORLOOP', 'FORPREP', 'TFORLOOP', 'SETLIST',
           'CLOSE', 'CLOSURE', 'VARARG']

class Interpreter:
    def __init__(self, lua_object):
        self.inst_size = lua_object.header['size of instruction']
        self.constants = {
            '*toplevel*': lua_object.top_level_func['constants']
            }
        self.instructions = {
            '*toplevel*': lua_object.top_level_func['instructions']
            }
        self.registers = []

    def run(self):
        for inst_bytestring in self.instructions['*toplevel*']:
            inst = struct.unpack('I', inst_bytestring)[0]
            opcode = inst & 0x0000003f
            # opcode type 1
            # a = (inst >> 6)  & 0x000000ff
            # c = (inst >> 14) & 0x000001ff
            # b = (inst >> 23) & 0x000001ff
            # opcode type 2 or 3
            # a  = (inst >> 6)  & 0x0000003f
            # bx = (inst >> 14) & 0x0003ffff
            if opcode == 0: # MOVE
                # iABC instruction
                print 'MOVE NYI'
            elif opcode == 1: # LOADK
                # iABx instruction
                a  = (inst >> 6)  & 0x0000003f
                bx = (inst >> 14) & 0x0003ffff
                self.register_put(a, self.constants['*toplevel*'][bx])

            elif opcode == 2: # LOADBOOL
                # iABC instruction
                print 'LOADBOOL NYI'
            elif opcode == 3: # LOADNIL
                # iABC instruction
                print 'LOADNIL NYI'
            elif opcode == 4: # GETUPVAL
                # iABC instruction
                print 'GETUPVAL NYI'
            elif opcode == 5: # GETGLOBAL
                # iABx instruction
                a  = (inst >> 6)  & 0x0000003f
                bx = (inst >> 14) & 0x0003ffff
                self.register_put(a, self.constants['*toplevel*'][bx])
            elif opcode == 6: # GETTABLE
                # iABC instruction
                a = (inst >> 6)  & 0x000000ff
                c = (inst >> 14) & 0x000001ff
                b = (inst >> 23) & 0x000001ff
                table = self.registers[b]
                index = self.constants['*toplevel*'][c - 256] if 256 & c else c
                # TODO check if index is a valid index of table
                self.register_put(a, index)

            elif opcode == 7: # SETGLOBAL
                # iABx instruction
                print 'SETGLOBAL NYI'
            elif opcode == 8: # SETUPVAL
                # iABC instruction
                print 'SETUPVAL NYI'
            elif opcode == 9: # SETTABLE
                # iABC instruction
                print 'SETTABLE NYI'
            elif opcode == 10: # NEWTABLE
                # iABC instruction
                print 'NEWTABLE NYI'
            elif opcode == 11: # SELF
                # iABC instruction
                print 'SELF NYI'
            elif opcode == 12: # ADD
                # iABC instruction
                print 'ADD NYI'
            elif opcode == 13: # SUB
                # iABC instruction
                print 'SUB NYI'
            elif opcode == 14: # MUL
                # iABC instruction
                print 'MUL NYI'
            elif opcode == 15: # DIV
                # iABC instruction
                print 'DIV NYI'
            elif opcode == 16: # MOD
                # iABC instruction
                print 'MOD NYI'
            elif opcode == 17: # POW
                # iABC instruction
                print 'POW NYI'
            elif opcode == 18: # UNM
                # iABC instruction
                print 'UNM NYI'
            elif opcode == 19: # NOT
                # iABC instruction
                print 'NOT NYI'
            elif opcode == 20: # LEN
                # iABC instruction
                print 'LEN NYI'
            elif opcode == 21: # CONCAT
                # iABC instruction
                print 'CONCAT NYI'
            elif opcode == 22: # JMP
                # iAsBx instruction
                print 'JMP NYI'
            elif opcode == 23: # EQ
                # iABC instruction
                print 'EQ NYI'
            elif opcode == 24: # LT
                # iABC instruction
                print 'LT NYI'
            elif opcode == 25: # LE
                # iABC instruction
                print 'LE NYI'
            elif opcode == 26: # TEST
                # iABC instruction
                print 'TEST NYI'
            elif opcode == 27: # TESTSET
                # iABC instruction
                print 'TESTSET NYI'
            elif opcode == 28: # CALL
                # iABC instruction
                a = (inst >> 6)  & 0x000000ff
                c = (inst >> 14) & 0x000001ff
                b = (inst >> 23) & 0x000001ff
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
                # iABC instruction
                print 'TAILCALL NYI'
            elif opcode == 30: # RETURN
                # iABC instruction
                a = (inst >> 6)  & 0x000000ff
                b = (inst >> 23) & 0x000001ff
                results = []
                if b == 0:
                    # results are in registers r[a] onwards
                    results.extend(self.registers[a:])
                elif b >= 2:
                    # there are b - 1 results starting from r[a]
                    results.extend(self.registers[a:b-1])
                self.return_(results)

            elif opcode == 31: # FORLOOP
                # iAsBx instruction
                print 'FORLOOP NYI'
            elif opcode == 32: # FORPREP
                # iAsBx instruction
                print 'FORPREP NYI'
            elif opcode == 33: # TFORLOOP
                # iABC instruction
                print 'TFORLOOP NYI'
            elif opcode == 34: # SETLIST
                # iABC instruction
                print 'SETLIST NYI'
            elif opcode == 35: # CLOSE
                # iABC instruction
                print 'CLOSE NYI'
            elif opcode == 36: # CLOSURE
                # iABx instruction
                print 'CLOSURE NYI'
            elif opcode == 37: # VARARG
                # iABC instruction
                print 'VARARG NYI'

    def register_put(self, i, item):
        while (i >= len(self.registers)):
            self.registers.append(None)
        self.registers[i] = item

    def call(self, function, args):
        # TODO do function call
        pass

    def return_(self, results):
        # TODO do function return
        pass


def main():
    import sys
    import parser
    if len(sys.argv) != 2:
        print 'usage: interpreter.py lua-bytecode-file'
        exit(1)
    bcfile = open(sys.argv[1], 'rb') # r = read, b = binary file
    bytecode = bcfile.read()
    lua_bytecode = parser.LuaBytecode(bytecode)
    interpreter = Interpreter(lua_bytecode)
    interpreter.run()

if __name__ == '__main__':
    main()
