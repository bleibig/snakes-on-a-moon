#!/usr/bin/env python

opcode_list = ['MOVE', 'LOADK', 'LOADBOOL', 'LOADNIL', 'GETUPVAL', 'GETGLOBAL',
               'GETTABLE', 'SETGLOBAL', 'SETUPVAL', 'SETTABLE', 'NEWTABLE',
               'SELF', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'POW', 'UNM', 'NOT',
               'LEN', 'CONCAT', 'JMP', 'EQ', 'LT', 'LE', 'TEST', 'TESTSET',
               'CALL', 'TAILCALL', 'RETURN', 'FORLOOP', 'FORPREP', 'TFORLOOP',
               'SETLIST', 'CLOSE', 'CLOSURE', 'VARARG']

class Interpreter:
    def __init__(self, lua_object):
        pass

def main():
    pass

if __name__ == '__main__':
    main()
