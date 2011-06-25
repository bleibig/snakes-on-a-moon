#!/usr/bin/env python

# Script to automate testing the sample lua scripts in the test directory

import re
import os
from subprocess import *

# lua executable name, replace with SOAM version when neccesary
LUA = 'lua'

def main():
    # for now, do not test these because they need to be invoked in a
    # special way
    do_not_test = ['globals.lua', 'luac.lua', 'readonly.lua', 'table.lua',
                   'trace-calls.lua', 'xd.lua']

    os.chdir('test')
    testdir = os.listdir('.')
    files = [f for f in testdir if re.search('\.lua$', f)]
    for f in files:
        if f in do_not_test:
            continue
        if f + 'c' not in testdir:
            # compile lua file
            print 'compiling', f
            Popen(['luac', '-o', f + 'c', f])
        f = f + 'c'
        print 'testing', f
        Popen([LUA, f], stdout=open(os.devnull, 'w'))
    print 'tests complete'

if __name__ == '__main__':
    main()
