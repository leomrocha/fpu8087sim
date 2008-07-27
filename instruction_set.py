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
		status.setC(status.getC()[1]=1); underflow=False
#pag 123
def FABS():
	pila.push(abs(pila.pop()[0]))
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False
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
		status.setC(status.getC()[1]=1); underflow=False
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
			status.setC(status.getC()[1]=1); underflow=False

#FADDP
def FADDP():
	pila.setI(1,pila.getI(1)[0]+pila.getI(0)[0]) #pila[1]=pila[1]+pila[0]
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False
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
			status.setC(status.getC()[1]=1); underflow=False
	return uesp


def FIADD(num): #operación entera
	#if 32 bits => op de 32 bits 
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(pila.pop()[0]+num)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False

#Operaciones de BCD
def FBLD(bcd): #convertir bcd a real y hacerle push
	#numreal = bcd
	#acá hay que convertirlo
	#acá se lo empuja
	pila.push(BCD2dec(bcd))
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FBSTP(bcd):
	uesp=pila.pop()[0]
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False



#Operaciones de Signo

def FCHS():
	pila.setI(0,-1*pila.getI(0)[0])
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False

#Operaciones de Registros (no de pila)
def FCLEX():
	#TODO check first  for and handles any pending unmasked floating-point exceptions before cleaning
	#clean flags
	status._PE=0
	status._UE=0
	status._OE=0
	status._ZE=0
	status._DE=0
	status._IE=0
#	status._ES=0 # pentium processors
#	status._EF=0 # pentium processors
	status._B=0

def FNCLEX():
	#clean flags without checking
	status._PE=0
	status._UE=0
	status._OE=0
	status._ZE=0
	status._DE=0
	status._IE=0
#	status._ES=0 # pentium processors
#	status._EF=0 # pentium processors
	status._B=0


#Operaciones de Movimientos condicionales (pag 137)

def FCMOVB(sti):
	if statusX86._CF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False

def FCMOVE():
	if statusX86._ZF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FCMOVBE():
	if statusX86._CF or status._ZF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FCMOVU():
	if statusX86._PF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FCMOVNB():
	if not statusX86._CF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FCMOVNE():
	if not statusX86._ZF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FCMOVNBE():
	if statusX86._CF == 0 and statusX86._ZF == 0:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


def FCMOVNU():
	if not statusX86._PF:
		pila.setI(0,pila.getI(sti)[0])
		pila.delI(sti)
	if underflow:
		status.setC(status.getC()[1]=1); underflow=False


#Operaciones de Comparación
"""
Opcode  Instruction   Description
D8 /2   FCOM m32real  Compare ST(0) with m32real.
DC /2   FCOM m64real  Compare ST(0) with m64real.
D8 D0+i FCOM ST(i)    Compare ST(0) with ST(i).
D8 D1   FCOM          Compare ST(0) with ST(1).
D8 /3   FCOMP m32real Compare ST(0) with m32real and pop register stack.
DC /3   FCOMP m64real Compare ST(0) with m64real and pop register stack.
D8 D8+i FCOMP ST(i)   Compare ST(0) with ST(i) and pop register stack.
D8 D9   FCOMP         Compare ST(0) with ST(1) and pop register stack.
DE D9   FCOMPP        Compare ST(0) with ST(1) and pop register stack twice.
"""


#Operaciones de 

#Si es llamado como ejecutable, entonces decir que esto es una librería del set de instrucción de la fpu 8087, mostrar la doc y salir.

