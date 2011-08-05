#!/bin/sh

if hash luac 2>&-
then
    for f in *.lua
    do
        echo "compiling $f"
        luac -o "$f"c "$f"
    done
else
    echo "error: luac not found"
    return
fi

