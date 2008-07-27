#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from fpu_structure import *
from datahandling import *


#TODO, faltan agregar las modificaciones que se hacen a las banderas de los diferentes registros
#TODO, faltan un montón de instrucciones
uesp = None #ultimo_elemento_sacado_de_pila

pila = Pila()
control = ControlRegister()
status = StatusRegister()
pinout = Pinout()

overflow = False
underflow = False

#pag 121
def F2XM1():
	pila.push((2**pila.pop()[0] )-1)
	if underflow:
		status.setC(status.getC()[1]=1)
#pag 123
def FABS():
	pila.push(abs(pila.pop()[0]))
	if underflow:
		status.setC(status.getC()[1]=1)
# Operaciones de Adición
"""
Operaciones de adición
OpcodeInstructionDescription
D8 /0 FADD m32 realAdd m32real to ST(0) and store result in ST(0)
DC /0 FADD m64real Add m64real to ST(0) and store result in ST(0)
D8 C0+i FADD ST(0), ST(i)Add ST(0) to ST(i) and store result in ST(0)
DC C0+i FADD ST(i), ST(0)Add ST(i) to ST(0) and store result in ST(i)
DE C0+i FADDP ST(i), ST(0) Add ST(0) to ST(i), store result in ST(i), and pop the
 register stack
DE C1 FADDPAdd ST(0) to ST(1), store result in ST(1), and pop the
 register stack
DA /0 FIADD m32int Add m32int to ST(0) and store result in ST(0)
DE /0 FIADD m16int Add m16int to ST(0) and store result in ST(0)
"""

#FADD
def FADD(num):
	#if 32 bits => op de 32 bits
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(pila.pop()+num)
	if underflow:
		status.setC(status.getC()[1]=1)
'''
def FADD(m64real)
	pass
'''
def FADD(st0=0,sti=0):
	if st0 == sti or (sti != 0 and st0 != 0):
		print "Error en FADD, st0"
		#raise()
	else:
		pila.setI(0,pila.getI(0)[0]+pila.getI(1)[0])#pila[0] = pila[st0] + pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2
		if underflow:
			status.setC(status.getC()[1]=1)

#FADDP
def FADDP():
	pila.setI(1,pila.getI(1)[0]+pila.getI(0)[0]) #pila[1]=pila[1]+pila[0]
	if underflow:
		status.setC(status.getC()[1]=1)
	uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
	return uesp

def FADDP(sti,st0):
	uesp = None
	if st0 == sti or (st0!= 0 and sti != 0):
		print "Error en FADDP, st0"
		#raise()
	else:
		pila.setI(1,pila.getI(1)[0]+pila.getI(0)[0])	#pila[1]=pila[1]+pila[0]
		uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
		if underflow:
			status.setC(status.getC()[1]=1)
	return uesp


def FIADD(num): #operación entera
	#if 32 bits => op de 32 bits 
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(pila.pop()[0]+num)
	if underflow:
		status.setC(status.getC()[1]=1)

#Operaciones de BCD
def FBLD(bcd): #convertir bcd a real y hacerle push
	#numreal = bcd
	#acá hay que convertirlo
	#acá se lo empuja
	pila.push(BCD2dec(bcd))
	if underflow:
		status.setC(status.getC()[1]=1)


def FBSTP(bcd):
	uesp=pila.pop()[0]
	if underflow:
		status.setC(status.getC()[1]=1)



#Operaciones de Signo

def FCHS():
	pila.setI(0,-1*pila.getI(0)[0])


#Operaciones de Registros (no de pila)
def FCLEX():
	pass

def FNCLEX():
	pass

#Operaciones de Movimientos condicionales (pag 137)

def FCMOVB():
	pass

def FCMOVE():
	pass

def FCMOVBE():
	pass

def FCMOVU():
	pass

def FCMOVNB():
	pass

def FCMOVNE():
	pass

def FCMOVNBE():
	pass

def FCMOVNU():
	pass

#Operaciones de 


#Operaciones de 

#Si es llamado como ejecutable, entonces decir que esto es una librería del set de instrucción de la fpu 8087, mostrar la doc y salir.

