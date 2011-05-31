#!/usr/bin/env python

import struct
import pprint

class LuaParseError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class LuaBytecode:
    """ Reads a bytestring of an object compiled with luac and parses
    it, organizing its data into fields of this object.
    """
    def __init__(self, bytecode):
        # parse header
        signature = bytecode[:4]
        if signature != '\x1b\x4c\x75\x61':
            raise LuaParseError('signature of bytecode file is invalid')
        version = ord(bytecode[4])
        if version != 81:
            raise LuaParseError('invalid version, must be 0x51 (dec 81)')
        format_version = ord(bytecode[5])
        if format_version != 0:
            raise LuaParseError('format version is not official')
        endianness = ord(bytecode[6])
        size_of_int = ord(bytecode[7])
        size_of_size_t = ord(bytecode[8])
        size_of_instruction = ord(bytecode[9])
        size_of_lua_Number = ord(bytecode[10])
        integral_flag = ord(bytecode[11])
        self.header = { 'signature': signature,
                        'version': version,
                        'format version': format_version,
                        'endianness': endianness,
                        'size of int': size_of_int,
                        'size of size_t': size_of_size_t,
                        'size of instruction': size_of_instruction,
                        'size of lua_Number': size_of_lua_Number,
                        'integral flag': integral_flag }
        print '=== header ==='
        pprint.pprint(self.header)

        self.top_level_func, i = self.parse_function(bytecode, 12)
        print '=== top level function ==='
        pprint.pprint(self.top_level_func)

        # check if it reached end of file
        assert i == len(bytecode), 'i = %d, bytecode size = %d' % \
            (i, len(bytecode))

    def parse_function(self, bytecode, i):
        """ Parses a function as well as all function prototypes it contains.

        Parameters:
            bytecode - The bytecode object being parsed
            i - bytecode index to start at

        Returns: A pair containing a dict with the function's data,
            and an int being the index it ended at
        """
        end = '>' if self.header['endianness'] == 0 else '<'
        sizeof_int = self.header['size of int']
        int_ = None
        if sizeof_int == 4:
            int_ = 'i'
        elif sizeof_int == 8:
            int_ = 'l'
        sizeof_sizet = self.header['size of size_t']
        sizeof_inst = self.header['size of instruction']
        sizeof_ln = self.header['size of lua_Number']
        integral = self.header['integral flag'] == 1
        num_type = None
        if integral:
            if sizeof_ln == 4:
                num_type = 'i' # 32-bit integer
            elif sizeof_ln == 8:
                num_type = 'l' # 64-bit integer
        else:
            if sizeof_ln == 4:
                num_type = 'f' # 32-bit float
            elif sizeof_ln == 8:
                num_type = 'd' # 64-bit double
        size_t = None
        if sizeof_sizet == 4:
            size_t = 'i'
        else:
            size_t = 'l'

        sourcename_size = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        sourcename = bytecode[i:i+sourcename_size-1]
        i += sourcename_size

        line_defined = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        last_line_defined = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        num_upvalues = ord(bytecode[i])
        i += 1
        num_parameters = ord(bytecode[i])
        i += 1
        is_vararg_flag = ord(bytecode[i])
        i += 1
        max_stack_size = ord(bytecode[i])
        i += 1

        # list of instructions
        num_instructions = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        instructions = []
        for _ in xrange(num_instructions):
            inst = bytecode[i:i+sizeof_inst]
            i = i + sizeof_inst
            instructions.append(inst)
        
        # list of constants
        sizek = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        constants = []
        for _ in xrange(sizek):
            constant_type = ord(bytecode[i])
            i += 1
            if constant_type == 0: # nil
                pass
            elif constant_type == 1: # boolean
                pass
            elif constant_type == 3: # number
                value = struct.unpack(end + num_type,
                                      bytecode[i:i+sizeof_ln])[0]
                i += sizeof_ln
                constants.append(value)
            elif constant_type == 4: # string
                value_length = struct.unpack(end + size_t,
                                             bytecode[i:i+sizeof_sizet])[0]
                i += sizeof_sizet
                value = bytecode[i:i+value_length-1]
                i += value_length
                constants.append(value)

        # list of function prototypes
        sizep = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        prototypes = []
        for _ in xrange(sizep):
            prototype, new_i = self.parse_function(bytecode, i)
            prototypes.append(prototype)
            i = new_i

        # debugging info
        # source line position list
        sizelineinfo = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        inst_positions = []
        for j in xrange(sizelineinfo):
            inst_positions.append((j, struct.unpack(end + int_,
                                                    bytecode[i:i+sizeof_int])[0]))
            i += sizeof_int

        # local list
        sizelocvars = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        locvars = []
        for j in xrange(sizelocvars):
            varname_length = struct.unpack(end + size_t,
                                           bytecode[i:i+sizeof_sizet])[0]
            i += sizeof_sizet
            varname = bytecode[i:i+varname_length-1]
            i += varname_length
            startpc = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
            i += sizeof_int
            endpc = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
            i += sizeof_int
            locvars.append((varname, startpc, endpc))

        # upvalue list
        sizeupvalues = struct.unpack(end + int_, bytecode[i:i+sizeof_int])[0]
        i += sizeof_int
        upvalues = []
        for _ in xrange(sizeupvalues):
            upvalue_length = struct.unpack(end + size_t,
                                           bytecode[i:i+sizeof_sizet])[0]
            i += sizeof_sizet
            upvalue = bytecode[i:i+upvalue_length-1]
            i += upvalue_length
            upvalues.append(upvalue)

        result = { 'sourcename': sourcename,
                 'line defined': line_defined,
                 'last line defined': last_line_defined,
                 'number of upvalues': num_upvalues,
                 'number of parameters': num_parameters,
                 'is vararg flag': is_vararg_flag,
                 'max stack size': max_stack_size,
                 'instructions': instructions,
                 'constants': constants,
                 'prototypes': prototypes,
                 'instructions positions': inst_positions,
                 'local variables': locvars,
                 'upvalues': upvalues
                 }
        return result, i

def main():
    import sys
    if len(sys.argv) != 2:
        print 'usage: interpreter lua-bytecode-file'
        exit(1)
    bcfile = open(sys.argv[1], 'rb') # r = read, b = binary file
    bytecode = bcfile.read()
    LuaBytecode(bytecode)

if __name__ == '__main__':
    main()
