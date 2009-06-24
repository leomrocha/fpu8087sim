#!/bin/sh
#compilamos el ensamblador
nasm -f elf hello.asm
#compilamos el wrapper que invoca a la funciona C
gcc -fPIC -c test.c
#linkeamos todo como biblioteca compartida!
ld -shared -soname libtest.so.1 -o libtest.so.1.0 -lc test.o hello.o
