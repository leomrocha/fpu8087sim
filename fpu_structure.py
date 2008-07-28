#!/usr/bin/env python
 # -*- coding: utf-8 -*-

from datahandling import *

"""
Pin Configuration

"""
"""
pin[ 1 ]='GND'
pin[ 2:16 ]= AD[14:0]
pin[ 17 ]= 'NC'
pin[ 18 ]= 'NC'
pin[ 19 ]= 'CLK'
pin[ 20 ]= 'GND'
pin[ 21 ]= 'RESET'
pin[ 22 ]= 'READY'
pin[ 23 ]= 'BUSY'
pin[ 24 ]= QS1
pin[ 25 ]= QS0
pin[ 26 ]= S0 #neg
pin[ 27 ]= S1 #neg
pin[ 28 ]= S2 #neg
pin[ 29 ]= 'NC'
pin[ 30 ]= 'NC'
pin[ 31 ]= RQ/GT0 #neg
pin[ 32 ]= INT
pin[ 33 ]= RQ/GT1 #neg
pin[ 34 ]= BHE #neg
pin[ 35 : 38 ]= S[6:3]
pin[ 39 ]= AD[15]
pin[ 40 ]= 'VCC'
"""
class Pinout:
	def __init__(self):
		self._AD =[0 for i in range(16)] #Líneas de dirección
		self._pin=[None for i in range(40)]
"""		self.pin[ 1 ]='GND'
		self.pin[ 2:16 ]= _AD[14:0]
		self.pin[ 17 ]= 'NC'
		self.pin[ 18 ]= 'NC'
		self.pin[ 19 ]= 'CLK'
		self.pin[ 20 ]= 'GND'
		self.pin[ 21 ]= 'RESET'
		self.pin[ 22 ]= 'READY'
		self.pin[ 23 ]= 'BUSY'
		self.pin[ 24 ]= 'QS1'
		self.pin[ 25 ]= 'QS0'
		self.pin[ 26 ]= 'S0' #neg
		self.pin[ 27 ]= 'S1' #neg
		self.pin[ 28 ]= 'S2' #neg
		self.pin[ 29 ]= 'NC'
		self.pin[ 30 ]= 'NC'
		self.pin[ 31 ]= 'RQ/GT0' #neg
		self.pin[ 32 ]= 'INT'
		self.pin[ 33 ]= 'RQ/GT1' #neg
		self.pin[ 34 ]= 'BHE' #neg
		self.pin[ 35 : 38 ]= [0,0,0,0]#S[6:3]
		self.pin[ 39 ]= self._AD[15]
		self.pin[ 40 ]= 'VCC'
"""

"""
Control Unit (CU)
Recibe las instrucciones
Decodifica los operandos
Ejecuta rutinas de control
"""

"""
Numeric Execution Unit (NEU)
Ejecuta las instrucciones numéricas
"""


"""
Data Field:
Compuesto por la Pila 

"""

"""
Pila
Esta está compuesta de 7 registros de 80 bits.
Cada registro consta de 
64 bits mas bajos de significand
15 bits de exponente
1 bit de signo
"""

"""
Tag Field
Cada registro tiene correspondencia uno a uno con un registro del data field
"""

class Pila:
	def __init__(self):
		self._pst=[] #pila st
		self._ptag=[] #pila de tags

	def push(self, st,tag):
		if self._pst.__len__() < 8 :
			self._pst.append(st)
			self._ptag.append(tag)
		else:
			print "fallo al empujar valor a la pila, demasiados valores"
			#raise  #excepción

	def push(self, st):
		if self._pst.__len__() < 8 :
			self._pst.append(st)
			self._ptag.append([0, 0])
		else:
			print "fallo al empujar valor a la pila, demasiados valores"
			#raise  #excepción

	def pop(self):
		try:
			return(self._pst.pop(),self._ptag.pop())
		except:
			return(0,[1,1])			

	def getI(self,i):
		if self._pst.__len__() >= 8 or i<0:
			#print "Valor de índice fuera de la pila"
			return(0,[1,1])
		try:
			return(self._pst[i],self._ptag[i])
		except:
			return(0,[1,1])

	def setI(self,i,st,tag):
		if self._pst.__len__() >= 8 or i <0:
			#print "Valor de índice fuera de la pila"
			return(0,[1,1])
		self._pst[i]=st
		self._ptag[i]=tag

	def setI(self,i,st):
		if self._pst.__len__() >= 8 or i <0:
			#print "Valor de índice fuera de la pila"
			return(0,[1,1])
		self._pst[i]=st
		self._ptag[i]=[0, 0]

	def delI(self,i):
		if self._pst.__len__() >= 8 or i <0:
			#print "Valor de índice fuera de la pila"
			return(0,[1,1])
		del(self._pst[i])
		del(self._ptag[i])
	
	def length(self):
		return len(self._pst)

	def head(self):
		return (len(self._pst)-1)


"""
Control Register (16 bits)
"""

class ControlRegister:
	def __init__(self):
		self._IM=0 #invalid operation
		self._DM=0 #Denormalized Operand
		self._ZM=0 #Zero Divide
		self._OM=0 #Overflow
		self._UM=0 #Underflow
		self._PM=0 #Precision
		self._X='X'	  #Reserved
		self._M=0 #Interrupt Mask
		self._PC = [0, 0] #Precition Control
		self._PC0=0 #
		self._PC1=0 #
		self._RC=[0, 0] #Rounding Control
		self._RC0=0 #
		self._RC1=0 #
		self._IC =[0, 0] #Infinity Control (0=projective, 1= affine)
		self._IC0 =0
		self._IC1 =0
		self._XXX=['X','X','X'] #últimos 3 bits reservados

	def setPC(self,pc):
		#falta checkear si pc es de dos dígitos y es solo unos y ceros
		_PC = pc

	def setPC(self,pc0,pc1):
		_PC[0] =pc0
		_PC[1] =pc1

	def getPC(self):
		return _PC
	
	def setRC(self,rc):
		_RC = rc

	def setRC(self,rc0,rc1):
		_RC[0] =rc0
		_RC[1] =rc1

	def getRC(self):
		return _RC

	def setIC(self,ic):
		_IC = ic

	def setIC(self,ic0,ic1):
		_IC[0] =ic0
		_IC[1] =ic1

	def getIC(self):
		return _IC


"""
Status Register (16 bits)
"""
class StatusRegister:
	def __init__(self):
		self._IE=0 #invalid operation
		self._DE=0 #Denormalized Operand
		self._ZE=0 #Zero Divide
		self._OE=0 #Overflow
		self._UE=0 #Underflow
		self._PE=0 #Precision
		self._X='X'	  #Reserved
		self._IR=0 #Interrupt Request
		self._C=[0, 0, 0, 0 ] #Condition Code
		self._C0=0 #Condition Code
		self._C1=0 #
		self._C2=0 #
		self._TOP=[0, 0, 0]#Top Of Stack Pointer
		self._C3=0 #
		self._B=0 #NEU busy

	def setTOP(self,top):
		self._TOP = top

	def setTOP(self,top0,top1,top2):
		self._TOP[0] = top0
		self._TOP[1] = top1
		self._TOP[2] = top2

	def getTOP(self):
		return self._TOP

	def setC(self,c):
		_C = c

	def setC(self,c0,c1,c2,c3):
		_C[0] = c0
		_C[1] = c1
		_C[2] = c2
		_C[3] = c3

	def getC(self):
		return _C

	def decTOP(self):
		aux=bin2dec(self._TOP)
		if aux== 0:
			aux=7
		else:
			aux-=1
		self._TOP=dec2bin(aux)

	def incTOP(self):
		aux=bin2dec(self._TOP)
		if aux== 7:
			aux=0
		else:
			aux+=1
		self._TOP=dec2bin(aux)


"""
Tag Word (16 bits) #listo
"""

"""
Instruction Pointer (32 bits)
"""

"""
Data Pointer (32 bits)
"""

"""
Registros necesarios del procesador 8086
"""

class StatusX86:
	def __init__(self):
		self._CF=0 
		self._PF=0 
		self._AF=0 
		self._ZF=0 
		self._SF=0 
		self._TF=0 
		self._IF=0 
		self._DF=0 
		self._OF=0 
#Si es llamado como ejecutable, entonces decir que esto es una librería que contiene las estructuras básicas de una fpu 8087 (pilas y registros), mostrar la doc y salir.
