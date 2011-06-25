#!/bin/sh

for f in *.lua
do
    luac -o "$f"c "$f"
done
