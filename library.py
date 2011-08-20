# basic library: holds lua standard library functions and variables

import sys

def lua_assert(v, message=None):
    print 'assert NYI'

def lua_collectgarbage(opt, arg=None):
    print 'collectgarbage NYI'

def lua_dofile(filename):
    print 'dofile NYI'

def lua_error(message, level=None):
    print 'error NYI'

_G = { }
_G['_G'] = _G

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

coroutine = {
    'create': coroutine_create,
    'resume': coroutine_resume,
    'running': coroutine_running,
    'status': coroutine_status,
    'wrap': coroutine_wrap,
    'yield': coroutine_yield,
    }

# module library

def lua_module(name, args=None):
    print 'module NYI'

def lua_require(modname):
    print 'require NYI'

package_cpath = ''

package_loaded = { }

package_loaders = { }

def package_loadlib(libname, funcname):
    print 'package.loadlib NYI'

package_path = ''

package_preload = { }

def package_seeall(module):
    print 'package.seeall NYI'

module = {
    'cpath': package_cpath,
    'loaded': package_loaded,
    'loaders': package_loaders,
    'loadlib': package_loadlib,
    'path': package_path,
    'preload': package_preload,
    'seeall': package_seeall,
    }

# string library

def string_byte(s, i=None, j=None):
    print 'string.byte NYI'

def string_char(args=None):
    print 'string.char NYI'

def string_dump(function):
    print 'string.dump NYI'

def string_find(s, pattern, init=None, plain=None):
    print 'string.find NYI'

def string_format(formatstring, args=None):
    print 'string.format NYI'

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

string = {
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
    }

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

table = {
    'concat': table_concat,
    'insert': table_insert,
    'maxn': table_maxn,
    'remove': table_remove,
    'sort': table_sort,
    }

# math library

def math_abs(x):
    print 'math.abs NYI'

def math_acos(x):
    print 'math.acos NYI'

def math_asin(x):
    print 'math.asin NYI'

def math_atan(x):
    print 'math.atan NYI'

def math_atan2(y, x):
    print 'math.atan2 NYI'

def math_ceil(x):
    print 'math.ceil NYI'

def math_cos(x):
    print 'math.cos NYI'

def math_cosh(x):
    print 'math.cosh NYI'

def math_deg(x):
    print 'math.deg NYI'

def math_exp(x):
    print 'math.exp NYI'

def math_floor(x):
    print 'math.floor NYI'

def math_fmod(x, y):
    print 'math.fmod NYI'

def math_frexp(x):
    print 'math.frexp NYI'

math_huge = 9001

def math_ldexp(m, e):
    print 'math.ldexp NYI'

def math_log(x):
    print 'math.log NYI'

def math_log10(x):
    print 'math.log10 NYI'

def math_max(x, args=None):
    print 'math.max NYI'

def math_min(x, args=None):
    print 'math.min NYI'

def math_modf(x):
    print 'math.modf NYI'

math_pi = 3.14

def math_pow(x, y):
    print 'math.pow NYI'

def math_rad(x):
    print 'math.rad NYI'

def math_random(m=None, n=None):
    print 'math.random NYI'

def math_randomseed(x):
    print 'math.randomseed NYI'

def math_sin(x):
    print 'math.sin NYI'

def math_sinh(x):
    print 'math.sinh NYI'

def math_sqrt(x):
    print 'math.sqrt NYI'

def math_tan(x):
    print 'math.tan NYI'

def math_tanh(x):
    print 'math.tanh NYI'

math = {
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
    }

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

io = {
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
    }

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

file_ = {
    'close': file_close,
    'flush': file_flush,
    'lines': file_lines,
    'read': file_read,
    'seek': file_seek,
    'setvbuf': file_setvbuf,
    'write': file_write 
    }

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

os = {
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
    }

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

debug = {
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
    }
