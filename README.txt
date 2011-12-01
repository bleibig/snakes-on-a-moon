Snakes On A Moon - authored by Brian Leibig

== Description ==

Snakes on a moon is a Lua back-end written in Python that will use
PyPy to create a fast JIT interpreter.  Lua is a simple but powerful
scripting language suitable to be embedded in large application
written in static languages like C and C++, but can also be used as a
standalone language.  The Lua interpreting process can be seen as two
distinct phases: the first parses the lua code and generates a
compiled bytecode, and the second runs it on a virtual machine.
Snakes on a moon only implements the second part.  It consists of
a virtual machine written in RPython that parses Lua bytecode and runs
it on its own interpreter.  This code will then be translated to a
fast interpreter in C with a JIT compiler and compiled to a native
executable, and will be much faster than running the interpreter in
Python and hopefully be faster than the standard Lua implementation.
Info on PyPy can be found at http://pypy.org/

== Current Status ==

The current goal is to implement a working Lua interpreter in regular
Python, and this part is almost complete.  Afterwards, the standard
library defined in library.py will be fully implemented (currently it
is mostly stubs) and then the code will be modified to be proper
RPython that PyPy can use to translate.

== Running ==

To interpret a Lua script, run 'python interpreter.py lua-file'.  The
lua file may either be a source file or a lua bytecode file generated
by the 'luac' command.  If it is the former, a lua bytecode file will
be automatically generated.

To just parse a lua bytecode file, run 'python parser.py lua-file'.
The parser will pretty-print the layout of the file as a series of
nested dicts and lists.  Like the interpreter, you can give it a lua
source file and it will automatically use luac to generate a bytecode
file for that script.

== Design ==

There are only two files that implement the interpreter: parser.py and
interpreter.py.  The parser.py file is responsible for reading a
binary lua bytecode file for a lua script and creating a LuaBytecode
object which holds a LuaFunction object for the "top level function"
whose body is the script itself.  The LuaBytecode is used to
instantiate an Interpreter defined in interpreter.py, and the run()
method is called with the top level function.  The run() method goes
through the instructions and executes the appropriate function for the
opcode.  If the opcode is CALL and it is calling another Lua function,
it will then recursively call run() for that new function, as the
function being called is defined as a LuaFunction object.

The library.py file implements the Lua standard library of global
objects and functions defined by the reference here:
http://www.lua.org/manual/5.1/manual.html#5

== Credits & Acknowledgements ==

Snakes On A Moon is authored by Brian Leibig.  The project was
inspired by a blog post here:
http://morepypy.blogspot.com/2011/04/tutorial-writing-interpreter-with-pypy.html
and the goal is to implement a nontrivial yet still simple language
similar to the tutorial to explore how PyPy works and how well it
would work for languages other than Python.

The Lua ChunkSpy tool found here: http://chunkspy.luaforge.net/ and
the associated guide to the bytecode format found here:
http://luaforge.net/docman/83/98/ANoFrillsIntroToLua51VMInstructions.pdf
by Kein-Hong Man, esq. have been very useful to understanding the
format and meaning of Lua bytecode.  Read the guide for detailed
information on how a Lua virtual machine works and what each opcode does.
