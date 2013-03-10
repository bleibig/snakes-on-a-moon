#!/usr/bin/env python

try:
    from rpython.rlib.rstruct.runpack import runpack
except ImportError:
    import struct
    def runpack(fmt, input):
        return struct.unpack(fmt, input)[0]

class LuaParseError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class LuaObject:
    pass

class LuaNumber(LuaObject):
    def __init__(self, value):
        self.value = value

class LuaString(LuaObject):
    def __init__(self, value):
        self.value = value

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

    def as_str(self):
        return '%s%s\n%s%d\n%s%d\n%s%d\n%s%d\n%s%d\n%s%d\n%s%d\n%s%d\n' % \
            ('signature: ', self.signature,
            'version: ', self.version,
            'format_version: ', self.format_version,
            'endianness: ', self.endianness,
            'size_of_int: ', self.size_of_int,
            'size_of_size_t: ', self.size_of_size_t,
            'size_of_instruction: ', self.size_of_instruction,
            'size_of_lua_Number: ', self.size_of_lua_Number,
            'integral_flag: ', self.integral_flag)

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

    def as_str(self):
        return 'LuaFunction@%d:%d' % (self.line_defined, self.last_line_defined)

class LuaBytecode:
    """ Reads a bytestring of an object compiled with luac and parses
    it, organizing its data into fields of this object.
    """
    def __init__(self, bytecode):
        # Parse header.
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

        # Parse top level function, which is an implicit lua function
        # containing all statements defined at the top level of the
        # script. All other functions are technically inner functions
        # defined in this one.
        self.top_level_func, i = self.parse_function(bytecode, 12)

        # Check if it reached end of file.
        assert i == len(bytecode), 'i = %d, bytecode size = %d' % \
            (i, len(bytecode))

    # These unpack functions are written the way they are because
    # runpack's first argument must be a constant.
    def unpack_sizet(self, input):
        if self.header.size_of_size_t == 4:
            return runpack('i', input)
        else:
            return runpack('l', input)

    def unpack_int(self, input):
        if self.header.endianness == 0:
            if self.header.size_of_int == 4:
                return runpack('>i', input)
            else:
                return runpack('>l', input)
        else:
            if self.header.size_of_int == 4:
                return runpack('<i', input)
            else:
                return runpack('<l', input)

    def unpack_number(self, input):
        if self.header.endianness == 0:
            if self.header.integral_flag == 1:
                if self.header.size_of_lua_Number == 4:
                    return runpack('>i', input)
                else:
                    return runpack('>l', input)
            else:
                if self.header.size_of_lua_Number == 4:
                    return runpack('>f', input)
                else:
                    return runpack('>d', input)
        else:
            if self.header.integral_flag == 1:
                if self.header.size_of_lua_Number == 4:
                    return runpack('<i', input)
                else:
                    return runpack('<l', input)
            else:
                if self.header.size_of_lua_Number == 4:
                    return runpack('<f', input)
                else:
                    return runpack('<d', input)

    def parse_function(self, bytecode, i):
        """ Parses a function as well as all function prototypes it contains.

        Parameters:
            bytecode - The bytecode object being parsed
            i - bytecode index to start at

        Returns: A pair containing a dict with the function's data,
            and an int being the index it ended at
        """
        sizeof_int = self.header.size_of_int
        sizeof_sizet = self.header.size_of_size_t
        sizeof_inst = self.header.size_of_instruction
        sizeof_ln = self.header.size_of_lua_Number

        sourcename_size = self.unpack_sizet(bytecode[i:i+sizeof_sizet])
        i += sizeof_sizet
        sourcename = ''
        if sourcename_size > 0:
            sourcename_size_idx = max(0, sourcename_size - 1)
            sourcename = bytecode[i:i+sourcename_size_idx]
            i += sourcename_size

        line_defined = self.unpack_int(bytecode[i:i+sizeof_int])
        i += sizeof_int
        last_line_defined = self.unpack_int(bytecode[i:i+sizeof_int])
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
        num_instructions = self.unpack_int(bytecode[i:i+sizeof_int])
        i += sizeof_int
        instructions = []
        for _ in xrange(num_instructions):
            inst = bytecode[i:i+sizeof_inst]
            i += sizeof_inst
            instructions.append(inst)
        
        # list of constants
        sizek = self.unpack_int(bytecode[i:i+sizeof_int])
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
                value = self.unpack_number(bytecode[i:i+sizeof_ln])
                i += sizeof_ln
                luavalue = LuaNumber(value)
                constants.append(luavalue)
            elif constant_type == 4: # string
                value_length = self.unpack_sizet(bytecode[i:i+sizeof_sizet])
                i += sizeof_sizet
                value = ''
                if value_length > 0:
                    value_length_idx = max(0, value_length - 1)
                    value = bytecode[i:i+value_length_idx]
                    i += value_length
                luavalue = LuaString(value)
                constants.append(luavalue)

        # list of function prototypes
        sizep = self.unpack_int(bytecode[i:i+sizeof_int])
        i += sizeof_int
        prototypes = []
        for _ in xrange(sizep):
            prototype, new_i = self.parse_function(bytecode, i)
            prototypes.append(prototype)
            i = new_i

        # debugging info
        # source line position list
        sizelineinfo = self.unpack_int(bytecode[i:i+sizeof_int])
        i += sizeof_int
        inst_positions = []
        for j in xrange(sizelineinfo):
            inst_positions.append((j, self.unpack_int(bytecode[i:i+sizeof_int])))
            i += sizeof_int

        # local list
        sizelocvars = self.unpack_int(bytecode[i:i+sizeof_int])
        i += sizeof_int
        locvars = []
        for _ in xrange(sizelocvars):
            varname_length = self.unpack_sizet(bytecode[i:i+sizeof_sizet])
            i += sizeof_sizet
            varname = ''
            if varname_length > 0:
                varname_length_idx = max(0, varname_length - 1)
                varname = bytecode[i:i+varname_length_idx]
                i += varname_length
            startpc = self.unpack_int(bytecode[i:i+sizeof_int])
            i += sizeof_int
            endpc = self.unpack_int(bytecode[i:i+sizeof_int])
            i += sizeof_int
            locvars.append((varname, startpc, endpc))

        # upvalue list
        sizeupvalues = self.unpack_int(bytecode[i:i+sizeof_int])
        i += sizeof_int
        upvalues = []
        for _ in xrange(sizeupvalues):
            upvalue_length = self.unpack_sizet(bytecode[i:i+sizeof_sizet])
            i += sizeof_sizet
            upvalue = ''
            if upvalue_length > 0:
                upvalue_length_idx = max(0, upvalue_length - 1)
                upvalue = bytecode[i:i+upvalue_length_idx]
                i += upvalue_length
            upvalues.append(upvalue)

        result = LuaFunction(sourcename, line_defined, last_line_defined,
                             num_upvalues, num_parameters, is_vararg_flag,
                             max_stack_size, instructions, constants,
                             prototypes, inst_positions, locvars, upvalues)
        return result, i

def entry_point(argv):
    import os
    if len(argv) != 2:
        print 'usage: parser.py lua-file'
        raise AssertionError()
    filename = argv[1] # must be luac-generated file
    bcfile = os.open(filename, os.O_RDONLY, 0777)
    bytecode = ""
    while True:
        read = os.read(bcfile, 4096)
        if len(read) == 0:
            break
        bytecode += read
    os.close(bcfile)
    lua_bytecode = LuaBytecode(bytecode)
    print '=== header ==='
    print lua_bytecode.header.as_str()
    return 0

def target(*args):
    return entry_point, None

if __name__ == '__main__':
    import sys
    entry_point(sys.argv)
