#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from fpu_structure import *
from datahandling import *
import math

#TODO, faltan agregar las modificaciones que se hacen a las banderas de los diferentes registros
#TODO, faltan un montón de instrucciones
uesp = None #ultimo_elemento_sacado_de_pila
res = None #resultado de la última operación

#hay que poner a res y uesp como global en cada una de las funciones, debo escribir un script que lo haga :P: global uesp,res

pila = Pila()
control = ControlRegister()
status = StatusRegister()

pinout = Pinout()

statusX86 = StatusX86()

overflow = False
underflow = False

#pag 121
def F2XM1():
	pila.push((2**pila.pop()[0] )-1)
	res = pila.getI(pila.head())[0]
	return res
#pag 123
def FABS():
	pila.push(abs(pila.pop()[0]))
	res = pila.getI(pila.head())[0]
	if res == 0 :
		statusX86._ZF=1
	return res
# Operaciones de Adición
"""
Operaciones de adición
Opcode Instruction Description
D8 C0+i FADD ST(0), ST(i)Add ST(0) to ST(i) and store result in ST(0)
DC C0+i FADD ST(i), ST(0)Add ST(i) to ST(0) and store result in ST(i)
DE C0+i FADDP ST(i), ST(0) Add ST(0) to ST(i), store result in ST(i), and pop the
 register stack
DE C1 FADDP Add ST(0) to ST(1), store result in ST(1), and pop the

"""

#FADD
def FADD(st0=0,sti=1):
	if st0 == sti or (sti != 0 and st0 != 0):
		print "Error en FADD, st0"
		#raise()
	else:
		a = pila.getI(pila.head())[0]
		b = pila.getI(pila.head()-1)[0]
		res = a + b
		#print st0,";", sti
		pila.setI(pila.head(), res)#pila[0] = pila[st0] + pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2
		if res == 0 :
			statusX86._ZF=1
		return res

#FADDP
def FADDP(sti=1,st0=0):
	uesp = None
	if st0 == sti or (st0!= 0 and sti != 0):
		print "Error en FADDP, st0"
		#raise()
	else:
		a = pila.getI(pila.head())[0]
		b = pila.getI(pila.head()-1)[0]
		res = a + b
		pila.setI(pila.head()-1,res)	#pila[1]=pila[1]+pila[0]
		uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
		#status.incTOP() #TODO, revisar si no hay fallo acá
		if res == 0 :
			statusX86._ZF=1
	return uesp

"""
Opcode  Instruction        Description
D8 E0+i FSUB ST(0), ST(i)  Subtract ST(i) from ST(0) and store result in ST(0)
DC E8+i FSUB ST(i), ST(0)  Subtract ST(0) from ST(i) and store result in ST(i)
DE E8+i FSUBP ST(i), ST(0) Subtract ST(0) from ST(i), store result in ST(i), and pop
                           register stack
DE E9   FSUBP              Subtract ST(0) from ST(1), store result in ST(1), and pop
                           register stack

"""

def FSUB(st0=0,sti=1):
	if st0 == sti or (sti != 0 and st0 != 0):
		print "Error en FSUB, st0"
		#raise()
	else:
		a = pila.getI(pila.head())[0]
		b = pila.getI(pila.head()-1)[0]
		res = a - b
		pila.setI(pila.head(), res)#pila[0] = pila[st0] + pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2
		if res == 0 :
			statusX86._ZF=1
		return pila.getI(pila.head())[0]

def FSUBP(st0=0,sti=1):
	uesp = None
	if st0 == sti or (st0!= 0 and sti != 0):
		print "Error en FSUBP, st0"
		#raise()
	else:
		a = pila.getI(pila.head())[0]
		b = pila.getI(pila.head()-1)[0]
		res = a - b
		pila.setI(pila.head(), res)#pila[0] = pila[st0] + pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2
		if res == 0 :
			statusX86._ZF=1
		uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
		#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp


#Operaciones de Signo

def FCHS():
	pila.setI(pila.head(),-1* pila.getI(pila.head())[0])
	res = pila.getI(pila.head())[0]
	return res

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

def FCOM(sti):
	#if 32 bits => op de 32 bits
	#else if 64 bits => op de 64 bits
	#else, todo mal
	c=status.getC()
	if  pila.getI(pila.head())[0] >  pila.getI(pila.head()-sti)[0]:
		c[0]= 0
		c[2]= 0
		c[3]= 0
	elif  pila.getI(pila.head())[0] <  pila.getI(pila.head()-sti)[0]:
		c[0]= 1
		c[2]= 0
		c[3]= 0
	elif  pila.getI(pila.head())[0] ==  pila.getI(pila.head()-sti)[0]:
		c[0]= 0
		c[2]= 0
		c[3]= 1
	else:
		c[0]= 1
		c[2]= 1
		c[3]= 1
	status.setC(c)


def FCOMP(sti):
	FCOM(sti)
	uesp = pila.pop()[0]
	res = uesp
	status.incTOP() #TODO, revisar si no hay fallo acá

def FCOMPP():
	FCOM(1)
	uesp = pila.pop()[0] #primer pop
	status.incTOP() #TODO, revisar si no hay fallo acá
	uesp = pila.pop()[0] #segundo pop, necesario
	res = uesp
	status.incTOP() #TODO, revisar si no hay fallo acá

#Operaciones sobre st0

def FCOS():
	caux = status.getC()
	if abs(pila.getI(pila.head())[0]) > (2**63):
		caux[2]=1
	else:
		caux[2]=0
		pila.push(math.cos(pila.pop()[0]))
		if pila.getI(pila.head())[0] == 0 :
			statusX86._ZF=1
	status.setC(caux)
	res =pila.getI(pila.head())[0]
	return res
"""
Opcode Instruction Description
D9 FE  FSIN        Replace ST(0) with its sine.
"""
def FSIN():
	caux = status.getC()
	if abs( pila.getI(pila.head())[0]) > (2**63):
		caux[2]=1
	else:
		caux[2]=0
		pila.push(math.sin(pila.pop()[0]))	
		if pila.getI(pila.head())[0] == 0 :
			statusX86._ZF=1
	status.setC(caux)
	res =pila.getI(pila.head())[0]
	return res

"""
Opcode Instruction Description
D9 FB  FSINCOS     Compute the sine and cosine of ST(0); replace ST(0) with
                   the sine, and push the cosine onto the register stack.

"""
def FSINCOS():
	caux = status.getC()	
	aux=  pila.getI(pila.head())[0]
	if abs(aux) > (2**63):
		caux[2]=1
	else:
		caux[2]=0
		pila.push(math.sin(pila.pop()[0]))	
		pila.push(math.cos(aux))
		status.decTOP()
		if pila.getI(pila.head())[0] == 0 :
			statusX86._ZF=1
	status.setC(caux)
	res =pila.getI(pila.head())[0]
	return res

"""
Opcode Instruction Description
D9 FA  FSQRT       Calculates square root of ST(0) and stores the result in
                   ST(0)
"""

def FSQRT():
	pila.push(math.sqrt(pila.pop()[0]))
	if pila.getI(pila.head())[0] == 0 :
		statusX86._ZF=1
	res =pila.getI(pila.head())[0]
	return res

"""
Opcode  Instruction        Description
D8 F0+i FDIV ST(0), ST(i)  Divide ST(0) by ST(i) and store result in ST(0)
DC F8+i FDIV ST(i), ST(0)  Divide ST(i) by ST(0) and store result in ST(i)
DE F8+i FDIVP ST(i), ST(0) Divide ST(i) by ST(0), store result in ST(i), and pop the
                           register stack
"""


def FDIV (st0,sti):
	a = pila.getI(pila.head()-sti)[0]
	b = pila.getI(pila.head())[0]
	if a == 0:
		status._ZE = 1
	res = b / a
	pila.setI(pila.head(),res)
	if b == 0:
		statusX86._ZF=1
	return pila.getI(pila.head())[0]

def FDIVP (sti,st0):
	FDIV(sti,st0)
	uesp = pila.pop()[0] #primer pop
	status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp


#Operaciones de liberación de cabeza de pila

def FFREE():
	pila.setI(pila.head(),None,[1,1])
	res =pila.getI(pila.head())[0]


def FLD(num):
	pila.push(num)
	status.decTOP()
	res =pila.getI(pila.head())[0]

"""
Opcode Instruction Description
D9 E8  FLD1        Push +1.0 onto the FPU register stack.
D9 E9  FLDL2T      Push log210 onto the FPU register stack.
D9 EA  FLDL2E      Push log2e onto the FPU register stack.
D9 EB  FLDPI       Push π onto the FPU register stack.
D9 EC  FLDLG2      Push log102 onto the FPU register stack.
D9 ED  FLDLN2      Push loge2 onto the FPU register stack.
D9 EE  FLDZ        Push +0.0 onto the FPU register stack.
"""
def FLD1():
	FLD(1.0)
	#status.decTOP()

def FLDL2T():
	FLD(math.log(10,2)) #log en base 2 de 10
	#status.decTOP()

def FLDL2E():
	FLD(math.log(math.e,2))#log en base 2 de e
	#status.decTOP()

def FLDPI():
	FLD(math.pi)
	#status.decTOP()

def FLDLG2():
	FLD(math.log10(2))
	#status.decTOP()

def FLDLN2():
	FLD(math.log(2,math.e))
	#status.decTOP()

def FLDZ():
	FLD(0.0)
	#status.decTOP()

"""
Opcode  Instruction  Description
D9 /2   FST m32real  Copy ST(0) to m32real
DD /2   FST m64real  Copy ST(0) to m64real
DD D0+i FST ST(i)    Copy ST(0) to ST(i)
D9 /3   FSTP m32real Copy ST(0) to m32real and pop register stack
DD /3   FSTP m64real Copy ST(0) to m64real and pop register stack
DB /7   FSTP m80real Copy ST(0) to m80real and pop register stack
DD D8+i FSTP ST(i)   Copy ST(0) to ST(i) and pop register stack
"""

def FST(mreal):
	uesp= pila.getI(pila.head())[0]
	res =uesp
	return uesp


def FSTP(mreal):
	uesp= pila.pop()[0]
	status.incTOP() #TODO, revisar si no hay fallo acá
	res = uesp
	return uesp

#incrementa TOP de status
def FINCSTP():
	status.incTOP()

#Multiplicación
"""
Opcode  Instruction        Description
D8 /1   FMUL m32real       Multiply ST(0) by m32real and store result in ST(0)
DC /1   FMUL m64real       Multiply ST(0) by m64real and store result in ST(0)
D8 C8+i FMUL ST(0), ST(i)  Multiply ST(0) by ST(i) and store result in ST(0)
DC C8+i FMUL ST(i), ST(0)  Multiply ST(i) by ST(0) and store result in ST(i)
DE C8+i FMULP ST(i), ST(0) Multiply ST(i) by ST(0), store result in ST(i), and pop the
                           register stack
DE C9   FMULP              Multiply ST(1) by ST(0), store result in ST(1), and pop the
                           register stack
DA /1   FIMUL m32int       Multiply ST(0) by m32int and store result in ST(0)
DE /1   FIMUL m16int       Multiply ST(0) by m16int and store result in ST(0)
"""

def FMUL (st0=0,sti=1):
	a = pila.getI(pila.head()-sti)[0]
	b = pila.getI(pila.head())[0]
	res = a * b
	pila.setI(pila.head(),res)
	if res == 0 :
		statusX86._ZF=1
	return pila.getI(pila.head())[0]

def FMULP (st0,sti):
	FMUL(st0,sti)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

#No Operation

def FNOP():
	pass

"""
Opcode Instruction Description
D9 F3  FPATAN      Replace ST(1) with arctan(ST(1)/ST(0)) and pop the register stack

"""
def FPATAN():
	pila.setI(1,math.atan(pila.getI(1)[0]/ pila.getI(pila.head())[0]))
	uesp=pila.pop()[0]
	status.incTOP() #TODO, revisar si no hay fallo acá
	if uesp == 0 :
		statusX86._ZF=1
	res = uesp
 	return uesp

"""
Opcode Instruction Clocks Description
D9 F2  FPTAN       17-173 Replace ST(0) with its tangent and push 1
                          onto the FPU stack.
"""

def FPTAN():
	caux=status.getC()
	if  pila.getI(pila.head()) < 2**63:
		caux[2]=0
		status.setC(caux)
		pila.setI(pila.head(),math.tan( pila.getI(pila.head())))
		if pila.getI(pila.head())[0] == 0 :
			statusX86._ZF=1
		FLD1()
		status.decTOP()
	else:
		caux[2]=1
		status.setC(caux)
		print "Operando fuera de rango"


"""
Opcode Instruction Description
D9 FC  FRNDINT     Round ST(0) to an integer.
"""
def FRNDINT():
	pila.push(int(round(pila.pop()[0])))
	res =pila.getI(pila.head())[0]

def FSCALE():
	pila.setI(pila.head(), pila.getI(pila.head())*(2**pila.getI(1)))
	res =pila.getI(pila.head())[0]
	#TODO, set flags



"""
Opcode  Instruction Description
D9 C8+i FXCH ST(i)  Exchange the contents of ST(0) and ST(i)
D9 C9   FXCH        Exchange the contents of ST(0) and ST(1)
"""
def FXCH(sti):
	aux =  pila.getI(pila.head()-sti)
	pila.setI(pila.head()-sti, pila.getI(pila.head())[0], pila.getI(pila.head())[1])
	pila.setI(pila.head(),aux[0],aux[1])
	res =pila.getI(pila.head())[0]
"""
Opcode Instruction Description
D9 F1  FYL2X       Replace ST(1) with (ST(1) ∗ log2ST(0)) and pop the
                   register stack
"""

def FYL2X():
	pila.setI(1,math.log( pila.getI(pila.head()),2))
	uesp=pila.pop()[0]
	status.incTOP() #TODO, ver si está bien esto
	res = uesp
	return uesp

"""
Opcode Instruction Description
D9 F9  FYL2XP1     Replace ST(1) with ST(1) ∗ log2(ST(0) + 1.0) and pop the
                   register stack
"""
def FYL2X():
	pila.setI(1,math.log( pila.getI(pila.head()),2)+1)
	uesp=pila.pop()[0]
	status.incTOP() #TODO, ver si está bien esto
	res = uesp
	return uesp

#Si es llamado como ejecutable, entonces decir que esto es una librería del set de instrucción de la fpu 8087, mostrar la doc y salir.

