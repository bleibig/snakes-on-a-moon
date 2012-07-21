# basic library: holds lua standard library functions and variables

import sys
import math
import random
from luatypes import *

def lua_assert(v, message=None):
    print 'assert NYI'

def lua_collectgarbage(opt, arg=None):
    print 'collectgarbage NYI'

def lua_dofile(filename):
    print 'dofile NYI'

def lua_error(message, level=None):
    print 'error NYI'

_G = LuaTable(hash={ })
_G['_G'] = _G

def lua_getfenv(f=None):
    print 'getfenv NYI'

def lua_getmetatable(object_):
    print 'getmetatable NYI'

def lua_ipairs(t):
    def iter_func(table, index):
        assert isinstance(index, (int, long, float))
        assert int(index) == index
        assert index > 0
        index = int(index)
        if index < len(table):
            nextindex = index + 1
            return nextindex, table[nextindex]
        else:
            return None
    return iter_func, t, 0

def lua_load(func, chunkname=None):
    print 'load NYI'

def lua_loadfile(filename=None):
    print 'loadfile NYI'

def lua_loadstring(string, chunkname=None):
    print 'loadstring NYI'

def lua_next(table, index=None):
    if index:
        if isinstance(index, (int, long, float)) \
            and int(index) == index \
            and index > 0:
            # index is array index
            index = int(index)
            if index < len(table):
                nextindex = index + 1
                return nextindex, table[nextindex]
            elif index == len(table):
                # last array index, so return first index and element in hash
                key = table.hash.keys()[0]
                return key, table[key]
        # otherwise index is hash key
        keys = table.hash.keys()
        i = keys.index(index)
        if i < len(keys) - 1:
            nextkey = keys[i+1]
            return nextkey, table[nextkey]
    else:
        if table.array:
            return 1, table[1]
        elif table.hash:
            key = table.hash.keys()[0]
            return key, table[key]
    return None

def lua_pairs(t):
    return lua_next, t, None

def lua_pcall(f, args):
    print 'pcall NYI'

def lua_print(args):
    for arg in args:
        if isinstance(arg, float) and int(arg) == arg:
            print int(arg),
        else:
            print arg,
        print '\t',
    print

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

_VERSION = 'Lua 5.1'

def lua_xpcall(f, err):
    print 'xpcall NYI'

# coroutine library

def coroutine_create(f):
    print 'coroutine.create NYI'

def coroutine_resume(co, vals=None):
    print 'coroutine.resume NYI'

def coroutine_running():
    print 'coroutine.running NYI'

def coroutine_status(co):
    print 'coroutine.status NYI'

def coroutine_wrap(f):
    print 'coroutine.wrap NYI'

def coroutine_yield(f):
    print 'coroutine.yield NYI'

coroutine = LuaTable(hash={
    'create': coroutine_create,
    'resume': coroutine_resume,
    'running': coroutine_running,
    'status': coroutine_status,
    'wrap': coroutine_wrap,
    'yield': coroutine_yield,
    })

# module library

def lua_module(name, args=None):
    print 'module NYI'

def lua_require(modname):
    print 'require NYI'

package_cpath = ''

package_loaded = LuaTable()

package_loaders = LuaTable()

def package_loadlib(libname, funcname):
    print 'package.loadlib NYI'

package_path = ''

package_preload = LuaTable()

def package_seeall(module):
    print 'package.seeall NYI'

module = LuaTable(hash={
    'cpath': package_cpath,
    'loaded': package_loaded,
    'loaders': package_loaders,
    'loadlib': package_loadlib,
    'path': package_path,
    'preload': package_preload,
    'seeall': package_seeall,
    })

# string library

def string_byte(s, i=None, j=None):
    print 'string.byte NYI'

def string_char(args=None):
    print 'string.char NYI'

def string_dump(function):
    print 'string.dump NYI'

def string_find(s, pattern, init=None, plain=None):
    print 'string.find NYI'

def string_format(args):
    formatstring = args[0]
    result = formatstring % tuple(args[1:])
    return [result]

def string_gmatch(s, pattern):
    print 'string.gmatch NYI'

def string_gsub(s, pattern, repl, n=None):
    print 'string.gsub NYI'

def string_len(s):
    print 'string.len NYI'

def string_lower(s):
    print 'string.lower NYI'

def string_match(s, pattern, init=None):
    print 'string.match NYI'

def string_rep(s, n):
    print 'string.rep NYI'

def string_reverse(s):
    print 'string.reverse NYI'

def string_sub(s, i, j=None):
    print 'string.sub NYI'

def string_upper(s):
    print 'string.upper NYI'

string = LuaTable(hash={
    'byte': string_byte,
    'char': string_char,
    'dump': string_dump,
    'find': string_find,
    'format': string_format,
    'gmatch': string_gmatch,
    'gsub': string_gsub,
    'len': string_len,
    'lower': string_lower,
    'match': string_match,
    'rep': string_rep,
    'reverse': string_reverse,
    'sub': string_sub,
    'upper': string_upper,
    })

# table library

def table_concat(table, sep=None, i=None, j=None):
    print 'table.concat NYI'

def table_insert(table, pos=None, value=None):
    print 'table.insert NYI'

def table_maxn(table):
    print 'table.maxn NYI'

def table_remove(table, pos):
    print 'table.remove NYI'

def table_sort(table, comp):
    print 'table.sort NYI'

table = LuaTable(hash={
    'concat': table_concat,
    'insert': table_insert,
    'maxn': table_maxn,
    'remove': table_remove,
    'sort': table_sort,
    })

# math library

def math_abs(args):
    x = args[0]
    return [abs(x)]

def math_acos(args):
    x = args[0]
    return [math.acos(x)]

def math_asin(args):
    x = args[0]
    return [math.asin(x)]

def math_atan(args):
    x = args[0]
    return [math.atan(x)]

def math_atan2(y, x):
    x, y = args[0], args[1]
    return [math.atan2(y, x)]

def math_ceil(args):
    x = args[0]
    return [math.ceil(x)]

def math_cos(args):
    x = args[0]
    return [math.cos(x)]

def math_cosh(args):
    x = args[0]
    return [math.cosh(x)]

def math_deg(args):
    x = args[0]
    return [math.degrees(x)]

def math_exp(args):
    x = args[0]
    return [math.exp(x)]

def math_floor(args):
    x = args[0]
    return [math.floor(x)]

def math_fmod(args):
    x, y = args[0], args[1]
    return [math.fmod(x, y)]

def math_frexp(args):
    x = args[0]
    return [math.frexp(x)]

math_huge = (1 << 32) - 1

def math_ldexp(args):
    m, e = args[0], args[1]
    return [math.ldexp(m, e)]

def math_log(args):
    x = args[0]
    return [math.log(x)]

def math_log10(args):
    x = args[0]
    return [math.log10(x)]

def math_max(args):
    assert len(args) > 0
    return [max(args)]

def math_min(args):
    assert len(args) > 0
    return [min(args)]

def math_modf(args):
    x = args[0]
    return [math.modf(x)]

math_pi = math.pi

def math_pow(args):
    x, y = args[0], args[1]
    return [math.pow(x, y)]

def math_rad(args):
    x = args[0]
    return [math.radians(x)]

def math_random(args):
    argc = len(args)
    if argc == 0:
        return [random.random()]
    elif argc == 1:
        m = args[0]
        assert isinstance(m, int)
        return [random.randint(1, m)]
    else:
        m, n = args[0], args[1]
        assert isinstance(m, int)
        assert isinstance(n, int)
        return [random.randint(m, n)]

def math_randomseed(args):
    x = args[0]
    random.seed(x)

def math_sin(args):
    x = args[0]
    return [math.sin(x)]

def math_sinh(args):
    x = args[0]
    return [math.sinh(x)]

def math_sqrt(args):
    x = args[0]
    return [math.sqrt(x)]

def math_tan(args):
    x = args[0]
    return [math.tan(x)]

def math_tanh(args):
    x = args[0]
    return [math.tanh(x)]

math = LuaTable(hash={
    'abs': math_abs,
    'acos': math_acos,
    'asin': math_asin,
    'atan': math_atan,
    'atan2': math_atan2,
    'ceil': math_ceil,
    'cos': math_cos,
    'cosh': math_cosh,
    'deg': math_deg,
    'exp': math_exp,
    'floor': math_floor,
    'fmod': math_fmod,
    'frexp': math_frexp,
    'huge': math_huge,
    'ldexp': math_ldexp,
    'log': math_log,
    'log10': math_log10,
    'max': math_max,
    'min': math_min,
    'modf': math_modf,
    'pi': math_pi,
    'pow': math_pow,
    'rad': math_rad,
    'random': math_random,
    'randomseed': math_randomseed,
    'sin': math_sin,
    'sinh': math_sinh,
    'sqrt': math_sqrt,
    'tan': math_tan,
    'tanh': math_tanh,
    })

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

io = LuaTable(hash={
    'close': io_close,
    'flush': io_flush,
    'input': io_input,
    'lines': io_lines,
    'open': io_open,
    'output': io_output,
    'popen': io_popen,
    'read': io_read,
    'tmpfile': io_tmpfile,
    'type': io_type,
    'write': io_write
    })

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
    for arg in args:
        if isinstance(arg, float):
            if arg == int(arg):
                arg = str(int(arg))
            else:
                arg = str(arg)
        file_obj.write(arg)

file_ = LuaTable(hash={
    'close': file_close,
    'flush': file_flush,
    'lines': file_lines,
    'read': file_read,
    'seek': file_seek,
    'setvbuf': file_setvbuf,
    'write': file_write 
    })

# os library

def os_clock():
    print 'os.clock NYI'

def os_date(format=None, time=None):
    print 'os.date NYI'

def os_difftime(t2, t1):
    print 'os.difftime NYI'

def os_execute(command=None):
    print 'os.execute NYI'

def os_exit(code=None):
    print 'os.exit NYI'

def os_getenv(varname):
    print 'os.getenv NYI'

def os_remove(filename):
    print 'os.remove NYI'

def os_rename(oldname, newname):
    print 'os.rename NYI'

def os_setlocale(locale, category=None):
    print 'os.setlocale NYI'

def os_time(table=None):
    print 'os.time NYI'

def os_tmpname():
    print 'os.tmpname NYI'

os = LuaTable(hash={
    'clock': os_clock,
    'date': os_date,
    'difftime': os_difftime,
    'execute': os_execute,
    'exit': os_exit,
    'getenv': os_getenv,
    'remove': os_remove,
    'rename': os_rename,
    'setlocale': os_setlocale,
    'time': os_time,
    'tmpname': os_tmpname,
    })

# debug library

def debug_debug():
    print 'debug.debug NYI'

def debug_getfenv(o):
    print 'debug.getfenv NYI'

def debug_gethook(thread=None):
    print 'debug.gethook NYI'

def debug_getinfo(thread=None, function=None, what=None):
    print 'debug.getinfo NYI'

def debug_getlocal(thread=None, level=None, local=None):
    print 'debug.getlocal NYI'

def debug_getmetatable(object_):
    print 'debug.getmetatable NYI'

def debug_getregistry():
    print 'debug.getregistry NYI'

def debug_getupvalue(func, up):
    print 'debug.getupvalue NYI'

def debug_setfenv(object_, table):
    print 'debug.setfenv NYI'

def debug_sethook(thread=None, hook=None, mask=None, count=None):
    print 'debug.sethook NYI'

def debug_setlocal(thread=None, level=None, local=None, value=None):
    print 'debug.setlocal NYI'

def debug_setmetatable(object_, table):
    print 'debug.setmetatable NYI'

def debug_setupvalue(func, up, value):
    print 'debug.setupvalue NYI'

def debug_traceback(thread=None, message=None, level=None):
    print 'debug.traceback NYI'

debug = LuaTable(hash={
    'debug': debug_debug,
    'getfenv': debug_getfenv,
    'gethook': debug_gethook,
    'getinfo': debug_getinfo,
    'getlocal': debug_getlocal,
    'getmetatable': debug_getmetatable,
    'getregistry': debug_getregistry,
    'getupvalue': debug_getupvalue,
    'setfenv': debug_setfenv,
    'sethook': debug_sethook,
    'setlocal': debug_setlocal,
    'setmetatable': debug_setmetatable,
    'setupvalue': debug_setupvalue,
    'traceback': debug_traceback,
    })
