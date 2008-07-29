# -*- coding: utf-8 -*-

"""
Tipos de Datos
"""
"""
BCD, será considerado como una lista ordenada de números enteros entre 0 y 9
Para convertirlo se pasará  multiplicando
sea a = [1,2,3,4,5,6,7...] donde el último dígito es el más significativo y el primero el menos
sea b el número decimal, entonces
b=0
j=0
for i in a:
    b+=i*(10**j)
    j+=1
b ahora es el número en decimal

conversión de decimal a bcd
a = lista
b= número decimal
while c >0:
	a.append(c%10)
	c/=10

"""

def BCD2dec(bcd):
	dec=0
	j=0
	for i in bcd:
		dec+=i*(10**j)
		j+=1
	return dec

def dec2BCD(dec):
	bcd=[]
	while dec >0:
		bcd.append(dec%10)
		dec/=10
	return bcd

"""
representación binaria

arreglo de unos y ceros

[b0,b1,b2,b3 .... ]
"""
def dec2bin(dec):
	bin=[]
	while dec >0:
		bin.append(dec%2)
		dec/=2
	return bin


def bin2dec(bin):
	dec=0
	j=0
	for i in bin:
		dec+=i*(2**j)
		j+=1
	return dec

def f2bin(num):
	return dec2bin(num*(10000000))
	
