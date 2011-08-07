# basic library: holds lua standard library functions and variables

import sys

_VERSION = 'Lua 5.1'

def lua_assert(v, message=None):
    print 'assert NYI'

def lua_collectgarbage(opt, arg=None):
    print 'collectgarbage NYI'

def lua_dofile(filename):
    print 'dofile NYI'

def lua_error(message, level=None):
    print 'error NYI'

def lua_getfenv(f=None):
    print 'getfenv NYI'

def lua_getmetatable(object_):
    print 'getmetatable NYI'

def lua_getipairs(t):
    print 'getipairs NYI'

def lua_load(func, chunkname=None):
    print 'load NYI'

def lua_loadfile(filename=None):
    print 'loadfile NYI'

def lua_loadstring(string, chunkname=None):
    print 'loadstring NYI'

def lua_next(table, index=None):
    print 'next NYI'

def lua_pairs(t):
    print 'pairs NYI'

def lua_pcall(f, args):
    print 'pcall NYI'

def lua_print(args):
    print 'print NYI'

def lua_rawequal(v1, v2):
    print 'rawequal NYI'

def lua_rawget(table, index):
    print 'rawget NYI'

def lua_rawset(table, index, value):
    print 'rawset NYI'

def lua_select(index, args):
    print 'select NYI'

def lua_setfenv(f, table):
    print 'setfenv NYI'

def lua_setmetatable(table, metatable):
    print 'setmetatable NYI'

def lua_tonumber(e, base=None):
    print 'tonumber NYI'

def lua_tostring(e):
    print 'tostring NYI'

def lua_type(v):
    print 'type NYI'

def lua_unpack(list_, i=None, j=None):
    print 'unpack NYI'

def lua_xpcall(f, err):
    print 'xpcall NYI'

# io library

__default_input = sys.stdin
__default_output = sys.stdout

def io_close(file_=None):
    print 'io.close NYI'

def io_flush():
    print 'io.flush NYI'

def io_input(file_=None):
    print 'io.input NYI'

def io_lines(filename=None):
    print 'io.lines NYI'

def io_open(filename, mode=None):
    print 'io.open NYI'

def io_output(file_=None):
    global __default_output
    if file_:
        if type(file_) == str:
            # filename, open it
            __default_output = open(file_)
        else:
            # otherwise file_ is a file handle
            __default_output = file_
    return __default_output

def io_popen(prog, mode=None):
    print 'io.popen NYI'

def io_read(args=None):
    print 'io.read NYI'

def io_tmpfile():
    print 'io.tmpfile NYI'

def io_type(obj):
    print 'io.type NYI'

def io_write(args=None):
    file_write(io_output(), args)

io = { 'close': io_close,
       'flush': io_flush,
       'input': io_input,
       'lines': io_lines,
       'open': io_open,
       'output': io_output,
       'popen': io_popen,
       'read': io_read,
       'tmpfile': io_tmpfile,
       'type': io_type,
       'write': io_write }

# file library

# The file functions are OO, so in lua all file functions implicitly
# take a file object i.e. "self" as a parameter.  Here the self
# parameter is explicitly bound as file_obj.

def file_close(file_obj):
    print 'file.close NYI'

def file_flush(file_obj):
    print 'file.flush NYI'

def file_lines(file_obj):
    print 'file.lines NYI'

def file_read(file_obj, args=None):
    print 'file.read NYI'

def file_seek(file_obj, whence=None, offset=None):
    print 'file.seek NYI'

def file_setvbuf(file_obj, mode, size=None):
    print 'file.setvbuf NYI'

def file_write(file_obj, args=None):
    if args:
        for arg in args:
            file_obj.write(arg)

file_ = { 'close': file_close,
          'flush': file_flush,
          'lines': file_lines,
          'read': file_read,
          'seek': file_seek,
          'setvbuf': file_setvbuf,
          'write': file_write }
