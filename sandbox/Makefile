#
# Linux makefile
# Use with make 
#

.SUFFIXES: .o .asm .c

AS=nasm 
ASFLAGS = -f elf
CC=gcc
CFLAGS= -fPIC -c
LD=ld 
LDFLAGS= -shared -soname


all: libtest.so.1

.asm.o:
	$(AS) $(ASFLAGS) $*.asm
	
test.o: test.c cdecl.h
	$(CC) $(CFLAGS) test.c


libtest.so.1: test.o hello.o prime2.o sum.o
	$(LD) $(LDFLAGS) libtest.so.1 -o libtest.so.1.0 test.o hello.o prime2.o sum.o

clean :
	rm *.o
