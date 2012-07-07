#!/usr/bin/env python

import struct
import pprint

class LuaParseError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class LuaHeader:
    """ Holds header data for a Lua binary chunck.  Has the following fields:

    signature: 4 bytes, header signature: ESC "Lua" or 0x1B4C7561 hexadecimal
    version: 1 byte, version number, 0x51 (81 decimal) for Lua 5.1
    format_version: 1 byte, 0 = official version
    endianness: 1 byte, 0 = big endian, 1 = little endian (default is 1)
    size_of_int: 1 byte, size of int in bytes (default is 4)
    size_of_size_t: 1 byte, size of size_t in bytes (default is 4)
    size_of_instruction: 1 byte, size of instruction in bytes (default is 4)
    size_of_lua_Number: 1 byte, size of lua_Number in bytes (default is 8)
    integral_flag: 1 byte, 0 = floating point, 1 = integral number types
        (default is 0)
    """
    def __init__(self, signature, version, format_version, endianness,
                 size_of_int, size_of_size_t, size_of_instruction,
                 size_of_lua_Number, integral_flag):
        self.signature = signature
        self.version = version
        self.format_version = format_version
        self.endianness = endianness
        self.size_of_int = size_of_int
        self.size_of_size_t = size_of_size_t
        self.size_of_instruction = size_of_instruction
        self.size_of_lua_Number = size_of_lua_Number
        self.integral_flag = integral_flag

    def as_dict(self):
        return {'signature': self.signature,
                'version': self.version,
                'format_version': self.format_version,
                'endianness': self.endianness,
                'size_of_int': self.size_of_int,
                'size_of_size_t': self.size_of_size_t,
                'size_of_instruction': self.size_of_instruction,
                'size_of_lua_Number': self.size_of_lua_Number,
                'integral_flag': self.integral_flag}

    def __str__(self):
        return pprint.pformat(self.as_dict())

class LuaFunction:
    """ Holds function data for a lua binary chunck.  Has the following fields:

    sourcename: string, name of lua source file
    line_defined: int, line of source file this function begins
    last_line_defined: int, line of source file this function ends
    num_upvalues: 1 byte, number of upvalues for this function
    num_parameters: 1 byte, number of parameters
    is_vararg_flag, 1 byte, 1 = VARARG_HASARG, 2 = VARARG_ISVARARG,
        4 = VARARG_NEEDSARG
    max_stack_size: 1 byte, number of registers used
    instructions: list of instructions (each one a 4-byte string)
    constants: list of constants
    prototypes: list of inner functions of LuaFunction type
    inst_positions: list of source line positions (optional debug data)
    locvars: list of local variables (optional debug data)
    upvalues: list of upvalues (optional debug data)
    """
    def __init__(self, sourcename, line_defined, last_line_defined,
                 num_upvalues, num_parameters, is_vararg_flag, max_stack_size,
                 instructions, constants, prototypes, inst_positions, locvars,
                 upvalues):
        self.sourcename = sourcename
        self.line_defined = line_defined
        self.last_line_defined = last_line_defined
        self.num_upvalues = num_upvalues
        self.num_parameters = num_parameters
        self.is_vararg_flag = is_vararg_flag
        self.max_stack_size = max_stack_size
        self.instructions = instructions
        self.constants = constants
        self.prototypes = prototypes
        self.inst_positions = inst_positions
        self.locvars = locvars
        self.upvalues = upvalues

    def as_dict(self):
        return {'sourcename': self.sourcename,
                'line_defined': self.line_defined,
                'num_upvalues': self.num_upvalues,
                'num_parameters': self.num_parameters,
                'is_vararg_flag': self.is_vararg_flag,
                'max_stack_size': self.max_stack_size,
                'instructions': self.instructions,
                'constants': self.constants,
                'prototypes': [p.as_dict() for p in self.prototypes],
                'inst_positions': self.inst_positions,
                'locvars': self.locvars,
                'upvalues': self.upvalues}

    def __str__(self):
#        return pprint.pformat(self.as_dict())
        return 'LuaFunction@{}:{}'.format(self.line_defined, self.last_line_defined)

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
        self.header = LuaHeader(signature, version, format_version, endianness,
                                size_of_int, size_of_size_t,
                                size_of_instruction, size_of_lua_Number,
                                integral_flag)

        self.top_level_func, i = self.parse_function(bytecode, 12)

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
        end = '>' if self.header.endianness == 0 else '<'
        sizeof_int = self.header.size_of_int
        int_ = None
        if sizeof_int == 4:
            int_ = 'i'
        elif sizeof_int == 8:
            int_ = 'l'
        sizeof_sizet = self.header.size_of_size_t
        sizeof_inst = self.header.size_of_instruction
        sizeof_ln = self.header.size_of_lua_Number
        integral = self.header.integral_flag == 1
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

        sourcename_size = struct.unpack(size_t, bytecode[i:i+sizeof_sizet])[0]
        i += sizeof_sizet
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
            i += sizeof_inst
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
                value_length = struct.unpack(size_t,
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
            varname_length = struct.unpack(size_t,
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
            upvalue_length = struct.unpack(size_t,
                                           bytecode[i:i+sizeof_sizet])[0]
            i += sizeof_sizet
            upvalue = bytecode[i:i+upvalue_length-1]
            i += upvalue_length
            upvalues.append(upvalue)

        result = LuaFunction(sourcename, line_defined, last_line_defined,
                             num_upvalues, num_parameters, is_vararg_flag,
                             max_stack_size, instructions, constants,
                             prototypes, inst_positions, locvars, upvalues)
        return result, i

def main():
    import sys
    if len(sys.argv) != 2:
        print 'usage: parser.py lua-file'
        exit(1)
    filename = sys.argv[1]
    if filename[-4:] == '.lua':
        # file is a lua script, compile with luac first
        import subprocess
        subprocess.check_call(['luac', '-o', filename + 'c', filename])
        filename += 'c'
    bcfile = open(filename, 'rb') # r = read, b = binary file
    bytecode = bcfile.read()
    lua_bytecode = LuaBytecode(bytecode)
    print '=== header ==='
    print lua_bytecode.header
    print '=== top level function ==='
    print lua_bytecode.top_level_func
    

if __name__ == '__main__':
    main()
