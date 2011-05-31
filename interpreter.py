#!/usr/bin/env python

import struct

opcode_list = ['MOVE', 'LOADK', 'LOADBOOL', 'LOADNIL', 'GETUPVAL', 'GETGLOBAL',
               'GETTABLE', 'SETGLOBAL', 'SETUPVAL', 'SETTABLE', 'NEWTABLE',
               'SELF', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'UNM', 'NOT',
               'LEN', 'CONCAT', 'JMP', 'EQ', 'LT', 'LE', 'TEST', 'TESTSET',
               'CALL', 'TAILCALL', 'RETURN', 'FORLOOP', 'FORPREP', 'TFORLOOP',
               'SETLIST', 'CLOSE', 'CLOSURE', 'VARARG']

class Interpreter:
    def __init__(self, lua_object):
        self.inst_size = lua_object.header['size of instruction']
        self.instructions = {
            '*toplevel*': lua_object.top_level_func['instructions']
            }

    def run(self):
        for inst in self.instructions['*toplevel*']:
            print hex(struct.unpack('i', inst)[0])

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
