#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from fpu_structure import *
from datahandling import *
import math

#TODO, faltan agregar las modificaciones que se hacen a las banderas de los diferentes registros
#TODO, faltan un montón de instrucciones
uesp = None #ultimo_elemento_sacado_de_pila

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

#pag 123
def FABS():
	pila.push(abs(pila.pop()[0]))

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
def FADD(self, *args):
	assert 1 <= len(args) <= 2
	st0 = args[0]
	sti = args[1]
	if len(args) == 2:
		if st0 == sti or (sti != 0 and st0 != 0):
			print "Error en FADD, st0"
			#raise()
		else:
			#print st0,";", sti
			pila.setI(pila.head(), pila.getI(pila.head())[0]+pila.getI(1)[0])#pila[0] = pila[st0] + pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2
	elif len(args) == 1:
		#if 32 bits => op de 32 bits
		#else if 64 bits => op de 64 bits
		#else, todo mal
		#aux = pila.pop()[0]
		#print "num=", num
		pila.push(pila.pop()[0]+args[0])
	else:
		print "Error de argumentos", args

#FADDP
def FADDP():
	pila.setI(1,pila.getI(1)[0]+ pila.getI(pila.head())[0]) #pila[1]=pila[1]+pila[0]
	uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
	return uesp

def FADDP(sti,st0):
	uesp = None
	if st0 == sti or (st0!= 0 and sti != 0):
		print "Error en FADDP, st0"
		#raise()
	else:
		pila.setI(1,pila.getI(1)[0]+ pila.getI(pila.head())[0])	#pila[1]=pila[1]+pila[0]
		uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
		#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp


def FIADD(num): #operación entera
	#if 32 bits => op de 32 bits 
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(pila.pop()[0]+num)


"""
Opcode  Instruction        Description
D8 /4   FSUB m32real       Subtract m32real from ST(0) and store result in ST(0)
DC /4   FSUB m64real       Subtract m64real from ST(0) and store result in ST(0)
D8 E0+i FSUB ST(0), ST(i)  Subtract ST(i) from ST(0) and store result in ST(0)
DC E8+i FSUB ST(i), ST(0)  Subtract ST(0) from ST(i) and store result in ST(i)
DE E8+i FSUBP ST(i), ST(0) Subtract ST(0) from ST(i), store result in ST(i), and pop
                           register stack
DE E9   FSUBP              Subtract ST(0) from ST(1), store result in ST(1), and pop
                           register stack
DA /4   FISUB m32int       Subtract m32int from ST(0) and store result in ST(0)
DE /4   FISUB m16int       Subtract m16int from ST(0) and store result in ST(0)

"""
#FSUB
def FSUB(num):
	#if 32 bits => op de 32 bits
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(pila.pop()[0]-num)

'''
def FSUB(m64real)
	pass
'''
def FSUB(st0=0,sti=0):
	if st0 == sti or (sti != 0 and st0 != 0):
		print "Error en FSUB, st0"
		#raise()
	else:
		 pila.setI(pila.head(), pila.getI(pila.head())[0]-pila.getI(1)[0])#pila[0] = pila[st0] - pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2

#FSUBP
def FSUBP():
	pila.setI(1,pila.getI(1)[0]- pila.getI(pila.head())[0]) #pila[1]=pila[1]-pila[0]
	uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FSUBP(sti,st0):
	uesp = None
	if st0 == sti or (st0!= 0 and sti != 0):
		print "Error en FSUBP, st0"
		#raise()
	else:
		pila.setI(1,pila.getI(1)[0]- pila.getI(pila.head())[0])	#pila[1]=pila[1]-pila[0]
		uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
		#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp


def FISUB(num): #operación entera
	#if 32 bits => op de 32 bits 
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(pila.pop()[0]-num)

"""
Opcode  Instruction         Description
D8 /5   FSUBR m32real       Subtract ST(0) from m32real and store result in ST(0)
DC /5   FSUBR m64real       Subtract ST(0) from m64real and store result in ST(0)
D8 E8+i FSUBR ST(0), ST(i)  Subtract ST(0) from ST(i) and store result in ST(0)
DC E0+i FSUBR ST(i), ST(0)  Subtract ST(i) from ST(0) and store result in ST(i)
DE E0+i FSUBRP ST(i), ST(0) Subtract ST(i) from ST(0), store result in ST(i), and pop
                            register stack
DE E1   FSUBRP              Subtract ST(1) from ST(0), store result in ST(1), and pop
                            register stack
DA /5   FISUBR m32int       Subtract ST(0) from m32int and store result in ST(0)
DE /5   FISUBR m16int       Subtract ST(0) from m16int and store result in ST(0)
"""
#FSUBR
def FSUBR(num):
	#if 32 bits => op de 32 bits
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(num - pila.pop()[0])
'''
def FSUBR(m64real)
	pass
'''
def FSUBR(st0=0,sti=0):
	if st0 == sti or (sti != 0 and st0 != 0):
		print "Error en FSUBR, st0"
		#raise()
	else:
		 pila.setI(pila.head(),pila.getI(1)[0]- pila.getI(pila.head())[0])#pila[0] = pila[st0] - pila[sti] #TODO, OJO, acá puede haber errores cuando cambie el tema a complemento a 2

#FSUBRP
def FSUBRR():
	pila.setI(1, pila.getI(pila.head())[0]-pila.getI(1)[0]) #pila[1]=pila[1]-pila[0]
	uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FSUBRP(sti,st0):
	uesp = None
	if st0 == sti or (st0!= 0 and sti != 0):
		print "Error en FSUBRP, st0"
		#raise()
	else:
		pila.setI(1, pila.getI(pila.head())[0]-pila.getI(1)[0])	#pila[1]=pila[1]-pila[0]
		uesp = pila.pop()[0] #OJO acá cuando cambie el registro intermedio de pop
		#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp


def FISUBR(num): #operación entera
	#if 32 bits => op de 32 bits 
	#else if 64 bits => op de 64 bits
	#else, todo mal
	pila.push(num-pila.pop()[0])


#Operaciones de BCD
def FBLD(bcd): #convertir bcd a real y hacerle push
	#numreal = bcd
	#acá hay que convertirlo
	#acá se lo empuja
	pila.push(BCD2dec(bcd))


def FBSTP(bcd):
	uesp=pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá



#Operaciones de Signo

def FCHS():
	 pila.setI(pila.head(),-1* pila.getI(pila.head())[0])

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
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVE():
	if statusX86._ZF:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVBE():
	if statusX86._CF or status._ZF:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVU():
	if statusX86._PF:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVNB():
	if not statusX86._CF:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVNE():
	if not statusX86._ZF:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVNBE():
	if statusX86._CF == 0 and statusX86._ZF == 0:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


def FCMOVNU():
	if not statusX86._PF:
		 pila.setI(pila.head(), pila.getI(pila.head()-sti)[0])
		 pila.delI(pila.head()-sti)


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

def FCOM():
	#if 32 bits => op de 32 bits
	#else if 64 bits => op de 64 bits
	#else, todo mal
	FCOMST(1)

def FCOMST(sti):
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

def FCOM(num):
	#esto sobrepasa el encapsulamiento de la pila y está a propósito
	#es para resolver un problema puntual, para que no salte excepción por el largo de pila
	pila.__pst.append(num) #este es el valor necesario
	pila.__ptag.append([0,0]) #este es solo por cuidado
	FCOM()
	#limpiando lo agregado extra
	pila.__pst.pop()
	pila.__ptag.pop()

def FCOMP():
	FCOM()
	uesp = pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá

def FCOMPST(sti):
	FCOMST(sti)
	uesp = pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá
def FCOMP(num):
	FCOM(num)
	uesp = pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá
def FCOMPP():
	FCOM()
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	uesp = pila.pop()[0] #segundo pop, necesario
	#status.incTOP() #TODO, revisar si no hay fallo acá

#Operaciones de  Comparación de enteros

"""
Opcode  Instruction       Description
DB F0+i FCOMI ST, ST(i)   Compare ST(0) with ST(i) and set status flags accordingly
DF F0+i FCOMIP ST, ST(i)  Compare ST(0) with ST(i), set status flags accordingly, and
                          pop register stack
DB E8+i FUCOMI ST, ST(i)  Compare ST(0) with ST(i), check for ordered values, and
                          set status flags accordingly
DF E8+i FUCOMIP ST, ST(i) Compare ST(0) with ST(i), check for ordered values, set
                          status flags accordingly, and pop register stack

"""

def FCOMI(sti):
	#if 32 bits => op de 32 bits
	#else if 64 bits => op de 64 bits
	#else, todo mal
	if  pila.getI(pila.head())[0] >  pila.getI(pila.head()-sti)[0]:
		statusX86._CF= 0
		statusX86._PF= 0
		statusX86._ZF= 0
	elif  pila.getI(pila.head())[0] <  pila.getI(pila.head()-sti)[0]:
		statusX86._CF= 1
		statusX86._PF= 0
		statusX86._ZF= 0
	elif  pila.getI(pila.head())[0] ==  pila.getI(pila.head()-sti)[0]:
		statusX86._CF= 0
		statusX86._PF= 0
		statusX86._ZF= 1
	else:
		statusX86._CF= 1
		statusX86._PF= 1
		statusX86._ZF= 1

def FCOMIP(sti):
	FCOMI(sti)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá

def FUCOMI(sti):
	#TODO, check for ordered values
	FCOMI(sti)

def FUCOMIP(sti):
	#TODO, check for ordered values
	FCOMIP(sti)

"""
Opcode Instruction Description
D9 E4  FTST        Compare ST(0) with 0.0.
"""

def FTST():
	FCOM(0.0)


"""
Opcode  Instruction  Description
DD E0+i FUCOM ST(i)  Compare ST(0) with ST(i)
DD E1   FUCOM        Compare ST(0) with ST(1)
DD E8+i FUCOMP ST(i) Compare ST(0) with ST(i) and pop register stack
DD E9   FUCOMP       Compare ST(0) with ST(1) and pop register stack
DA E9   FUCOMPP      Compare ST(0) with ST(1) and pop register stack twice
"""
def FUCOM():
	FUCOM(1)

def FUCOM(sti):
	FCOM(sti)

def FUCOMP():
	return FUCOMP(1)

def FUCOMP(sti):
	FCOMP(sti)

def FUCOMPP():
	FUCOM()
	uesp= pila.pop()[0]
	status.incTOP() #TODO, revisar si esto está bien
	uesp= pila.pop()[0]
	status.incTOP() #TODO, revisar si esto está bien


#Operaciones sobre st0

def FCOS():
	caux = status.getC()
	if abs( pila.getI(pila.head())[0]) > (2**63):
		caux[2]=1
		status.setC(caux)
	else:
		caux[2]=0
		status.setC(caux)
		pila.push(math.cos(pila.pop()[0]))	


"""
Opcode Instruction Description
D9 FE  FSIN        Replace ST(0) with its sine.
"""
def FSIN():
	caux = status.getC()
	if abs( pila.getI(pila.head())[0]) > (2**63):
		caux[2]=1
		status.setC(caux)
	else:
		caux[2]=0
		status.setC(caux)
		pila.push(math.sin(pila.pop()[0]))	


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
		status.setC(caux)
	else:
		caux[2]=0
		status.setC(caux)
		pila.push(math.sin(pila.pop()[0]))	
		pila.push(math.cos(aux))
		status.decTOP()


"""
Opcode Instruction Description
D9 FA  FSQRT       Calculates square root of ST(0) and stores the result in
                   ST(0)
"""

def FSQRT():
	pila.push(math.sqrt(pila.pop()[0]))


def FDECSTP():
	pila.decTOP()
	#TODO, faltan realizar las operaciones sonbre C1, el manual está incorrecto :S
#operaciones de división
"""
Opcode  Instruction        Description
D8 /6   FDIV m32real       Divide ST(0) by m32real and store result in ST(0)
DC /6   FDIV m64real       Divide ST(0) by m64real and store result in ST(0)
D8 F0+i FDIV ST(0), ST(i)  Divide ST(0) by ST(i) and store result in ST(0)
DC F8+i FDIV ST(i), ST(0)  Divide ST(i) by ST(0) and store result in ST(i)
DE F8+i FDIVP ST(i), ST(0) Divide ST(i) by ST(0), store result in ST(i), and pop the
                           register stack
DE F9   FDIVP              Divide ST(1) by ST(0), store result in ST(1), and pop the
                           register stack
DA /6   FIDIV m32int       Divide ST(0) by m32int and store result in ST(0)
DE /6   FIDIV m16int       Divide ST(0) by m64int and store result in ST(0)
"""

def FDIV(num):
	 pila.setI(pila.head(), pila.getI(pila.head())[0]/num)

def FDIV (sti):
	 pila.setI(pila.head(), pila.getI(pila.head())[0]/ pila.getI(pila.head()-sti)[0])

def FDIV (sti,st0):
	pila.setI(i, pila.getI(pila.head()-sti)[0]/ pila.getI(pila.head())[0])

def FDIVP():
	FDIV(1,0)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FDIVP (sti,st0):
	FDIV(sti,st0)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FIDIV(num):
	FDIV(num)


#Operaciones de división inversas

"""
Opcode  Instruction         Description
D8 /7   FDIVR m32real       Divide m32real by ST(0) and store result in ST(0)
DC /7   FDIVR m64real       Divide m64real by ST(0) and store result in ST(0)
D8 F8+i FDIVR ST(0), ST(i)  Divide ST(i) by ST(0) and store result in ST(0)
DC F0+i FDIVR ST(i), ST(0)  Divide ST(0) by ST(i) and store result in ST(i)
DE F0+i FDIVRP ST(i), ST(0) Divide ST(0) by ST(i), store result in ST(i), and pop the
                            register stack
DE F1   FDIVRP              Divide ST(0) by ST(1), store result in ST(1), and pop the
                            register stack
DA /7   FIDIVR m32int       Divide m32int by ST(0) and store result in ST(0)
DE /7   FIDIVR m16int       Divide m64int by ST(0) and store result in ST(0)

"""

def FDIVR(num):
	 pila.setI(pila.head(),num/ pila.getI(pila.head())[0])

def FDIVR (sti):
	 pila.setI(pila.head(),pila.getI(i)[0]/ pila.getI(pila.head())[0])

def FDIVR (sti,st0):
	 pila.setI(pila.head()-sti, pila.getI(pila.head())[0]/ pila.getI(pila.head()-sti)[0])

def FDIVPR():
	FDIV(1,0)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FDIVPR (sti,st0):
	FDIVR(sti,st0)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FIDIVR(num):
	FDIVR(num)

#Operaciones de liberación de cabeza de pila

def FFREE():
	 pila.setI(pila.head(),None,[1,1])

#Operaciones de comparación de enteros
"""
Opcode Instruction   Description
DE /2  FICOM m16int  Compare ST(0) with m16int
DA /2  FICOM m32int  Compare ST(0) with m32int
DE /3  FICOMP m16int Compare ST(0) with m16int and pop stack register
DA /3  FICOMP m32int Compare ST(0) with m32int and pop stack register

"""
def FICOM(num):
	FCOM(num)

def FICOMP(num):
	FICOM(num)
	uesp = pila.pop()[0] #primer pop	
	#status.incTOP() #TODO, revisar si no hay fallo acá

#Operaciones de carga de pila
"""
Opcode Instruction Description
DF /0  FILD m16int Push m16int onto the FPU register stack.
DB /0  FILD m32int Push m32int onto the FPU register stack.
DF /5  FILD m64int Push m64int onto the FPU register stack.

"""

def FILD(num):
	status.decTOP()
	pila.push(num)

"""
Opcode  Instruction Description
D9 /0   FLD m32real Push m32real onto the FPU register stack.
DD /0   FLD m64real Push m64real onto the FPU register stack.
DB /5   FLD m80real Push m80real onto the FPU register stack.
D9 C0+i FLD ST(i)   Push ST(i) onto the FPU register stack.
"""
def FLD(num):
	pila.push(num)
	status.decTOP()

def FLDST(sti): #¿esto es así? no es muy claro en el manual, pag 167
	pila.push( pila.getI(pila.head()-sti))
	status.decTOP()
 
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

def FLDL2T():
	FLD(math.log(10,2)) #log en base 2 de 10

def FLDL2E():
	FLD(math.log(math.e,2))#log en base 2 de e

def FLDPI():
	FLD(math.pi)

def FLDLG2():
	FLD(math.log10(2))

def FLDLN2():
	FLD(math.log(2,math.e))

def FLDZ():
	FLD(0.0)

"""
Opcode Instruction Description
D9 /5 FLDCW m2byte Load FPU control word from m2byte.
"""
def FLDCW(m2byte):
	FLD(m2byte) #TODO, modelo de memoria, para poder cargar solo lo que hace falta

"""
Opcode Instruction       Description
D9 /4  FLDENV m14/28byte Load FPU environment from m14byte or m28byte.
"""

def FLDENV(mbyte):
	pass #TODO

#operaciones de extracción de stack
"""
Opcode Instruction  Description
DF /2  FIST m16int  Store ST(0) in m16int
DB /2  FIST m32int  Store ST(0) in m32int
DF /3  FISTP m16int Store ST(0) in m16int and pop register stack
DB /3  FISTP m32int Store ST(0) in m32int and pop register stack
DF /7  FISTP m64int Store ST(0) in m64int and pop register stack
"""
def FIST(dirmem):
	uesp =  pila.getI(pila.head())[0]
	#acá falta agregar un modelo de memoria RAM para poder cargar el valor donde corresponde
	return uesp

def FISTP(dirmem):
	uesp = pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá
	#acá falta agregar un modelo de memoria RAM para poder cargar el valor donde corresponde
	
	return uesp
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
	return uesp
	
def FST_ST(i):
	pila.setI(1, pila.getI(pila.head())[0], pila.getI(pila.head())[1])


def FSTP(mreal):
	uesp= pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FSTP_ST(i):
	FST_ST(i)
	uesp=pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

#incrementa TOP de status
def FINCSTP():
	status.incTOP()



#Inicialización de la FPU
def FINIT():
	#TODO, check for and handles any pending unmasked floating-point exceptions
	FNINIT()
	pass

def FNINIT():
	#TODO, poner
	# control en 1101111111 #037Fh
	# TAG word en FFFFh
	# los demás: status, data pointer instruction pointer, last instruction opcode, en 0 (cero)
	pass

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
def FMUL(num):
	 pila.setI(pila.head(), pila.getI(pila.head())[0]*num)
 
def FMUL_ST (sti):
	 pila.setI(pila.head(), pila.getI(pila.head())[0]* pila.getI(pila.head()-sti)[0])
 
def FMUL (sti,st0):
	pila.setI(pila.head()-sti, pila.getI(pila.head()-sti)[0]* pila.getI(pila.head())[0])
 
def FMULP():
	FMUL(1,0)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FMULP (sti,st0):
	FMUL(sti,st0)
	uesp = pila.pop()[0] #primer pop
	#status.incTOP() #TODO, revisar si no hay fallo acá
	return uesp

def FIMUL(num):
	FMUL(num)

#No Oeration

def FNOP():
	pass

"""
Opcode Instruction Description
D9 F3  FPATAN      Replace ST(1) with arctan(ST(1)/ST(0)) and pop the register stack

"""
def FPATAN():
	pila.setI(1,math.atan(pila.getI(1)[0]/ pila.getI(pila.head())[0]))
	uesp=pila.pop()[0]
	#status.incTOP() #TODO, revisar si no hay fallo acá
 
"""
Opcode Instruction Description
D9 F8  FPREM       Replace ST(0) with the remainder obtained from
                   dividing ST(0) by ST(1)
"""

def FPREM():
	 pila.setI(pila.head(), pila.getI(pila.head())[0]%pila.getI(1)[0])
	#TODO, setear las variables status._C # pag 182

"""
Opcode Instruction Description
D9 F5  FPREM1      Replace ST(0) with the IEEE remainder obtained from
                   dividing ST(0) by ST(1)
"""

def FPREM1():
	FPREM() #TODO, cuando se cambien los modelos, esto hay que cambiarlo para que cumpla con la IEEE que ahora no cumple

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
		status.decTOP()
		FLD1()
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

"""
Opcode Instruction        Description
DD /4  FRSTOR m94/108byte Load FPU state from m94byte or m108byte.
Restaura el estado de la FPU desde memoria
"""
def FRSTOR():
	pass #TODO, pag190

"""
Opcode   Instruction         Description
9B DD /6 FSAVE m94/108byte   Store FPU state to m94byte or m108byte after checking for
                             pending unmasked floating-point exceptions. Then re-
                             initialize the FPU.
DD /6    FNSAVE* m94/108byte Store FPU environment to m94byte or m108byte without
                             checking for pending unmasked floating-point exceptions.
                             Then re-initialize the FPU.

Guarda el estado de la FPU en  la dirección memoria dada
"""

def FSAVE(m94_108byte):
	pass #TODO

def FSAVE(m94_108byte):
	pass #TODO

"""
Opcode   Instruction    Description
9B D9 /7 FSTCW m2byte   Store FPU control word to m2byte after checking for
                        pending unmasked floating-point exceptions.
D9 /7    FNSTCW* m2byte Store FPU control word to m2byte without checking for
                        pending unmasked floating-point exceptions.
"""
def FSTCW(m2byte):
	pass

def FNSTCW(m2byte):
	pass

"""
Opcode   Instruction         Description
9B D9 /6 FSTENV m14/28byte   Store FPU environment to m14byte or m28byte after
                             checking for pending unmasked floating-point exceptions.
                             Then mask all floating-point exceptions.
D9 /6    FNSTENV* m14/28byte Store FPU environment to m14byte or m28byte without
                             checking for pending unmasked floating-point exceptions.
                             Then mask all floating-point exceptions.
"""
def FSTENV(m14_28byte):
	pass

def FNSTENV(m14_28byte):
	pass

"""
Opcode   Instruction    Description
9B DD /7 FSTSW m2byte   Store FPU status word at m2byte after checking for
                        pending unmasked floating-point exceptions.
9B DF E0 FSTSW AX       Store FPU status word in AX register after checking for
                        pending unmasked floating-point exceptions.
DD /7    FNSTSW* m2byte Store FPU status word at m2byte without checking for
                        pending unmasked floating-point exceptions.
DF E0    FNSTSW* AX     Store FPU status word in AX register without checking for
                        pending unmasked floating-point exceptions.
"""

def FSTSW(m2byte):
	pass

def FSTSW(): #guarda en AX
	pass

def FNSTSW(m2byte):
	pass

def FNSTSW(): #guarda en  AX
	pass

"""
Opcode Instruction Description
D9 FD  FSCALE      Scale ST(0) by ST(1).

"""

def FSCALE():
	 pila.setI(pila.head(), pila.getI(pila.head())*(2**pila.getI(1)))
	#TODO, set flags


def FWAIT():
	pass

"""
Opcode Instruction Description
D9 E5  FXAM        Classify value or number in ST(0)
"""
#TODO
def FXAM():
	"""
	C1 ← sign bit of ST; (* 0 for positive, 1 for negative *)
	CASE (class of value or number in ST(0)) OF
	   Unsupported:C3, C2, C0 ← 000;
	   NaN:          C3, C2, C0 ← 001;
	   Normal:       C3, C2, C0 ← 010;
	   Infinity:     C3, C2, C0 ← 011;
	   Zero:         C3, C2, C0 ← 100;
	   Empty:        C3, C2, C0 ← 101;
	   Denormal: C3, C2, C0 ← 110;
	ESAC;
	"""
	pass

"""
Opcode  Instruction Description
D9 C8+i FXCH ST(i)  Exchange the contents of ST(0) and ST(i)
D9 C9   FXCH        Exchange the contents of ST(0) and ST(1)
"""
def FXCH():
	FXCH(1)

def FXCH(sti):
	aux =  pila.getI(pila.head()-sti)
	pila.setI(pila.head()-sti, pila.getI(pila.head())[0], pila.getI(pila.head())[1])
	pila.setI(pila.head(),aux[0],aux[1])

"""
Opcode Instruction Description
D9 F4  FXTRACT     Separate value in ST(0) into exponent and significand,
                   store exponent in ST(0), and push the significand onto the
                   register stack.
"""

def FXTRACT():
	pass #TODO

"""
Opcode Instruction Description
D9 F1  FYL2X       Replace ST(1) with (ST(1) ∗ log2ST(0)) and pop the
                   register stack
"""

def FYL2X():
	pila.setI(1,math.log( pila.getI(pila.head()),2))
	uesp=pila.pop()[0]
	#status.incTOP() #TODO, ver si está bien esto
	return uesp

"""
Opcode Instruction Description
D9 F9  FYL2XP1     Replace ST(1) with ST(1) ∗ log2(ST(0) + 1.0) and pop the
                   register stack
"""
def FYL2X():
	pila.setI(1,math.log( pila.getI(pila.head()),2)+1)
	uesp=pila.pop()[0]
	#status.incTOP() #TODO, ver si está bien esto
	return uesp

#Si es llamado como ejecutable, entonces decir que esto es una librería del set de instrucción de la fpu 8087, mostrar la doc y salir.

