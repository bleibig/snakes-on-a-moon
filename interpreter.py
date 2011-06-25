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
        self.instructions = {
            '*toplevel*': lua_object.top_level_func['instructions']
            }

    def run(self):
        for inst_bytestring in self.instructions['*toplevel*']:
            inst = struct.unpack('i', inst_bytestring)[0]
            opcode = inst & ord('\x3f') # first 6 bits
            # # opcode type 1
            # a = inst & struct.unpack('i', '\x00\x00\x3f\xc0')[0]
            # b = inst & struct.unpack('i', '\x00\x7f\xc0\x00')[0]
            # c = inst & struct.unpack('i', '\xff\x80\x00\x00')[0]
            # # opcode type 2/3
            # a = inst & struct.unpack('i', '\x00\x00\x3f\xc0')[0]
            # bx = inst & struct.unpack('i', '\xff\xff\xc0\x00')[0]
            if opcode == 0: # MOVE
                # iABC instruction
                print 'MOVE NYI'
            elif opcode == 1: # LOADK
                # iABx instruction
                print 'LOADK NYI'
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
                print 'GETGLOBAL NYI'
            elif opcode == 6: # GETTABLE
                # iABC instruction
                print 'GETTABLE NYI'
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
                print 'CALL NYI'
            elif opcode == 29: # TAILCALL
                # iABC instruction
                print 'TAILCALL NYI'
            elif opcode == 30: # RETURN
                # iABC instruction
                print 'RETURN NYI'
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
