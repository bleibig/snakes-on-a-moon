# basic library: holds lua standard library functions and variables

import sys
import math
import random
import time
import os
from luatypes import *

def lua_assert(args):
    v = args[0]
    message = args[1] if len(args) >= 2 else 'assertion failed!'
    assert v != nil or v != False, message
    return args

def lua_collectgarbage(args):
    raise AssertionError('collectgarbage not supported')

def lua_dofile(filename):
    print 'dofile NYI'

def lua_error(args):
    message = args[0]
    level = args[1] if len(args) > 1 else 1
    raise AssertionError(message)

_G = LuaTable()
_G.set('_G', _G)

def lua_getfenv(f=None):
    print 'getfenv NYI'

def lua_getmetatable(args):
    object = args[0]
    metatable = object.metatable
    if metatable and '__metatable' in metatable.hash:
        return [metatable['__metatable']]
    else:
        return [metatable]

def lua_ipairs(args):
    t = args[0]
    def iter_func(args):
        table = args[0]
        index = args[1]
        assert isinstance(index, (int, long, float))
        assert int(index) == index
        index = int(index)
        if index < len(table):
            nextindex = index + 1
            return [nextindex, table[nextindex]]
        else:
            return [None]
    return [iter_func, t, 0]

def lua_load(func, chunkname=None):
    print 'load NYI'

def lua_loadfile(filename=None):
    print 'loadfile NYI'

def lua_loadstring(string, chunkname=None):
    print 'loadstring NYI'

def lua_next(args):
    table = args[0]
    index = args[1] if len(args) > 1 else None
    if index:
        if isinstance(index, (int, long, float)) \
            and int(index) == index \
            and index > 0:
            # index is array index
            index = int(index)
            if index < len(table):
                nextindex = index + 1
                return [nextindex, table[nextindex]]
            elif index == len(table):
                # last array index, so return first index and element in hash
                key = table.hash.keys()[0]
                return [key, table[key]]
        # otherwise index is hash key
        keys = table.hash.keys()
        i = keys.index(index)
        if i < len(keys) - 1:
            nextkey = keys[i+1]
            return [nextkey, table[nextkey]]
    else:
        if table.array:
            return [1, table[1]]
        elif table.hash:
            key = table.hash.keys()[0]
            return [key, table[key]]
    return [None]

def lua_pairs(args):
    t = args[0]
    return [lua_next, t, None]

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

def lua_select(args):
    index = args[0]
    if isinstance(index, (int, long, float)):
        return args[index+1:]
    assert index == '#'
    return [len(args) - 1]

def lua_setfenv(f, table):
    print 'setfenv NYI'

def lua_setmetatable(args):
    table = args[0]
    metatable = args[1]
    if table.metatable and '__metatable' in table.metatable.hash:
        raise AssertionError('table has a "__metatable" field')
    table.metatable = metatable
    return [table]

def lua_tonumber(args):
    e = args[0]
    base = args[1] if len(args) > 1 else 10
    try:
        if base == 10:
            return [float(e)]
        elif e == int(e):
            return [int(e, base)]
    except ValueError:
        pass
    return [None]

def lua_tostring(args):
    e = args[0]
    # TODO check __tostring metamethod
    return [str(e)]

def lua_type(args):
    v = args[0]
    if v == None:
        return ['nil']
    if isinstance(v, (int, long, float)):
        return ['number']
    if isinstance(v, str):
        return ['string']
    if isinstance(v, bool):
        return ['boolean']
    if isinstance(v, LuaTable):
        return ['table']
    if isinstance(v, LuaFunction) or hasattr(v, '__call__'):
        return ['function']
    # TODO check if thread or userdata
    return ['thread or userdata']

def lua_unpack(args):
    list = args[0]
    assert isinstance(list, LuaTable)
    i = args[1] if len(args) > 1 else 1
    j = args[2] if len(args) > 2 else len(list)
    return [t[k] for k in xrange(i, j+1)]

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

def string_byte(args):
    s = args[0]
    i = args[1] if len(args) > 1 else 1
    j = args[2] if len(args) > 2 else 1
    return [ord(s[k]) for k in xrange(i-1, j)]

def string_char(args):
    return [''.join([chr(i) for i in args])]

def string_dump(args):
    raise AssertionError('string.dump NYI')

def string_find(args):
    raise AssertionError('string.find NYI')

def string_format(args):
    formatstring = args[0]
    result = formatstring % tuple(args[1:])
    return [result]

def string_gmatch(args):
    raise AssertionError('string.gmatch NYI')

def string_gsub(args):
    raise AssertionError('string.gsub NYI')

def string_len(args):
    s = args[0]
    return [len(s)]

def string_lower(args):
    s = args[0]
    return [str.lower(s)]

def string_match(args):
    raise AssertionError('string.match NYI')

def string_rep(args):
    s = args[0]
    n = args[1]
    return [s * n]

def string_reverse(args):
    s = args[0]
    l = list(s)
    l.reverse()
    return [''.join(l)]

def string_sub(args):
    s = args[0]
    i = args[1]
    j = args[2] if len(args) > 2 else -1
    if i > 0:
        i = i - 1
    elif i == 0:
        i = 1
    if j == -1:
        j = len(s)
    return [s[i:j]]

def string_upper(args):
    s = args[0]
    return [str.upper(s)]

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

def table_concat(args):
    lenargs = len(args)
    table = args[0]
    sep = args[1] if lenargs > 1 else ''
    i = args[2] if lenargs > 2 else 1
    j = args[3] if lenargs > 3 else len(table)
    return [sep.join([str(table[k]) for k in xrange(i, j+1)])]

def table_insert(args):
    table = args[0]
    pos = args[1] if len(args) > 2 else len(table)+1
    value = args[2] if len(args) > 2 else args[1]
    table.array.insert(pos-1, value)
    return []

def table_maxn(args):
    table = args[0]
    i = len(table)
    while i > 0:
        if table[i] != None:
            return [i]
        i -= 1
    return [0]

def table_remove(args):
    table = args[0]
    pos = args[1] if len(args) > 1 else len(table)
    del table[pos]
    return []

def table_sort(args):
    raise AssertionError('table.sort NYI')

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
    if argc == 1:
        m = int(args[0])
        return [random.randint(1, m)]
    m, n = int(args[0]), int(args[1])
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

def io_close(args):
    file = args[0] if len(args) > 1 else __default_output
    if file != __default_output:
        file.close()
    return [None]

def io_flush(args):
    __default_output.flush()
    return [None]

def io_input(args):
    file = arg[0] if len(args) > 1 else None
    global __default_input
    if file:
        if isinstance(file, str):            
            __default_input = open(file)
        else:
            __default_input = file
    return [__default_input]

def io_lines(args):
    filename = args[0] if len(args) > 1 else __default_input
    f = open(filename)
    def read_line():
        try:
            line = f.next()
            return [line]
        except StopIteration:
            f.close()
            return [None]
    return [read_line]

def io_open(args):
    filename = args[0]
    mode = args[1] if len(args) > 1 else ''
    return [open(filename, mode)]

def io_output(args):
    file = args[0] if len(args) > 0 else None
    global __default_output
    if file:
        if isinstance(file, str):
            # filename, open it
            __default_output = open(file)
        else:
            # otherwise file is a file handle
            __default_output = file
    return [__default_output]

def io_popen(args):
    raise AssertionError('io.popen NYI')

def io_read(args):
    return file_read([__default_input] + args)

def io_tmpfile(args):
    return [os.tmpfile()]

def io_type(args):
    obj = args[0]
    if isinstance(obj, file):
        if obj.closed:
            return ['closed file']
        return ['file']
    return [None]

def io_write(args):
    return file_write([__default_output] + args)

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

def file_close(args):
    file_obj = args[0]
    file_obj.close()
    return [None]

def file_flush(args):
    file_obj = args[0]
    file_obj.flush()
    return [None]

def file_lines(args):
    file_obj = args[0]
    def read_line():
        try:
            line = file_obj.next()
            return [line]
        except StopIteration:
            return [None]
    return [read_line]

def file_read(args):
    raise AssertionError('file.read NYI')

def file_seek(args):
    raise AssertionError('file.seek NYI')

def file_setvbuf(args):
    raise AssertionError('file.setvbuf NYI')

def file_write(args):
    file_obj = args[0]
    for arg in args[1:]:
        if isinstance(arg, (int, long, float)):
            if arg == int(arg):
                arg = str(int(arg))
            else:
                arg = str(arg)
        file_obj.write(arg)
    return [None]

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

def os_clock(args):
    return [time.clock()]

def os_date(args):
    format = str(args[0]) if len(args) > 0 else '%c'
    time_ = args[1] if len(args) > 0 else time.time()
    utc = False
    if format[0] == '!':
        utc = True
        format = format[1:]
    st = time.gmtime(time_) if utc else time.localtime(time_)
    if format == '*t':
        return [LuaTable(hash={
                    'year': st.tm_year,
                    'month': st.tm_mon,
                    'day': st.tm_mday,
                    'hour': st.tm_hour,
                    'min': st.tm_min,
                    'sec': st.tm_sec,
                    'wday': ((st.tm_wday + 1) % 7) + 1,
                    'yday': st.tm_yday,
                    'isdst': bool(st.isdst)
                    })]
    return [time.strftime(format, st)]

def os_difftime(args):
    t2 = args[0]
    t1 = args[1]
    return [t2 - t1]

def os_execute(args):
    raise AssertionError('os.execute NYI')

def os_exit(args):
    code = args[0] if len(args) > 0 else 0
    exit(code)

def os_getenv(args):
    varname = args[0]
    return [os.getenv(varname)]

def os_remove(args):
    filename = args[0]
    try:
        os.remove(filename)
        return [None]
    except OSError as e:
        return [None, str(e)]

def os_rename(args):
    oldname = args[0]
    newname = args[1]
    try:
        os.rename(oldname, newname)
        return [None]
    except OSError as e:
        return [None, str(e)]

def os_setlocale(args):
    raise AssertionError('os.setlocale NYI')

def os_time(args):
    table = args[0] if len(args) > 0 else None
    if table:
        year = table['year']
        month = table['month']
        day = table['day']
        hour = table['hour'] or 0
        min = table['min'] or 0
        sec = table['sec'] or 0
        isdst = table['isdst'] or -1
        return [time.mktime((year, month, day, hour, min, sec, 0, 0, isdst))]
    return [int(time.time())]

def os_tmpname(args):
    return [os.tmpnam()]

os_ = LuaTable(hash={
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
