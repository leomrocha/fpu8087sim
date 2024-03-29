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
		self.iniciar()

	def iniciar(self): #iniciar en ...
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
		self.iniciar()

	def iniciar(self): #iniciar en 0000h
		self._pst=[] #pila st
		self._ptag=[] #pila de tags

	def push(self, *args):
		assert 1 <= len(args) <= 2
		if len(args) == 2:
			st,tag = args
		if len(args) == 2:
			st,tag = args
		elif len(args) == 1:
			st=args[0]
			tag = [0,0]
		else:
			print "Error de argumentos", args
		if len(self._pst) < 8 :
			self._pst.append(st)
			self._ptag.append(tag)
		else:
			print "fallo al empujar valor a la pila, demasiados valores"
			#raise  #excepción

	def pop(self):
		try:
			return(self._pst.pop(),self._ptag.pop())
		except:
			return(0,[1,1])			

	def getI(self,i):
		if len(self._pst) > 8 or i<0:
			#print "Valor de índice fuera de la pila"
			return(0,[1,1])
		try:
			return(self._pst[i],self._ptag[i])
		except:
			return(0,[1,1])

	def setI(self,*args):
		assert 2 <= len(args) <= 3
		if len(args) == 3:
			i,st,tag = args
		elif len(args) == 2:
			i,st = args
			tag = [0,0]
		elif len(args) == 1:
			i=args[0]
			st=0
			tag = [0,0]
		else:
			print "Error de argumentos", args
		if len(self._pst) > 8 or i <0:
			#print "Valor de índice fuera de la pila"
			return(0,[1,1])
		self._pst[i]=st
		self._ptag[i]=tag

	def delI(self,i):
		try:
			del(self._pst[i])
			del(self._ptag[i])
			return True
		except:
			return False

	def length(self):
		return len(self._pst)

	def head(self):
		return (len(self._pst)-1)

	def getRegs(self):
		return [ self.getI(i) for i in range (8)]
			
	def setRegs(self,pilatemp):
		print pilatemp
		print "holaaa"
		for st in pilatemp:
			print st
			self.setI(st[0],st[1])


"""
Control Register (16 bits)
"""

class ControlRegister:
	def __init__(self): 
		self.iniciar()

	def iniciar(self): #iniciar en 037Fh
		self._IM=1 #invalid operation
		self._DM=1 #Denormalized Operand
		self._ZM=1 #Zero Divide
		self._OM=1 #Overflow
		self._UM=1 #Underflow
		self._PM=1 #Precision
		self._X=1	  #Reserved
		self._M=0 #Interrupt Mask
		self._PC = [1, 1] #Precition Control
		self._PC0= self._PC[0] #
		self._PC1= self._PC[0] #
		self._RC=[0, 0] #Rounding Control
		self._RC0=self._RC[0] #
		self._RC1=self._RC[1] #
		self._IC =[0, 0] #Infinity Control (0=projective, 1= affine)
		self._IC0 =self._IC[0]
		self._IC1 =self._IC[1]
		self._XX=[0,0] #últimos 3 bits reservados

	def setPC(self, *args):
		assert 1 <= len(args) <= 2
		if len(args) == 2:
			self._PC[0] =args[0]
			self._PC[1] =args[1]
		elif len(args) == 1:
			self._PC = args[0]
		else:
			print "Error de argumentos", args

	def getPC(self):
		return _PC
	
	def setRC(self, *args):
		assert 1 <= len(args) <= 2
		if len(args) == 2:
			self._RC[0] =args[0]
			self._RC[1] =args[1]
		elif len(args) == 1:
			self._RC = args[0]
		else:
			print "Error de argumentos", args


	def getRC(self):
		return _RC

	def setIC(self, *args):
		assert 1 <= len(args) <= 2
		if len(args) == 2:
			self._IC[0] =args[0]
			self._IC[1] =args[1]
		elif len(args) == 1:
			self._IC = args[0]
		else:
			print "Error de argumentos", args


	def getIC(self):
		return _IC

	def getRegs(self):
		return [self._IM, self._DM, self._ZM,self._OM,self._UM,	self._PM,self._X,self._M,self._PC[0], self._PC[1],self._RC[0],self._RC[1],self._IC[0],self._IC[1],self._XX[0],self._XX[1]]


	def setRegs(IM,DM,ZM,OM,UM,PM,X0,M,PC0,PC1,RC0,RC1,IC0,IC1,X1,X2):
		self._IM=IM
		self._DM=DM
		self._ZM=ZM
		self._OM=OM
		self._UM=UM
		self._PM=PM
		self._X=X0
		self._M=M
		self._PC[0]=PC0
		self._PC[1]=PC1
		self._RC[0]=RC0
		self._RC[1]=RC1
		self._IC[0]=IC0
		self._IC[1]=IC1
		self._XX[0]=X1
		self._XX[1]=X2

	def getRegNames(self):
		return ['IM','DM','ZM','OM','UM','PM','X0','M','PC0','PC1','RC0','RC1','IC0','IC1','X1','X2']


"""
Status Register (16 bits)
"""
class StatusRegister:
	def __init__(self):
		self.iniciar()

	def iniciar(self): #iniciar en 0000h
		self._IE=0 #invalid operation
		self._DE=0 #Denormalized Operand
		self._ZE=0 #Zero Divide
		self._OE=0 #Overflow
		self._UE=0 #Underflow
		self._PE=0 #Precision
		self._X=0	  #Reserved
		self._IR=0 #Interrupt Request
		self._C=[0, 0, 0, 0 ] #Condition Code
		self._C0=0 #Condition Code
		self._C1=0 #
		self._C2=0 #
		self._TOP=[0, 0, 0]#Top Of Stack Pointer
		self._C3=0 #
		self._B=0 #NEU busy

	def setTOP(self,*args):
		assert 1 <= len(args) <= 3
		if len(args) == 3:
			self._TOP[0] = args[0]
			self._TOP[1] = args[1]
			self._TOP[2] = args[2]

		elif len(args) == 1:
			self._TOP = args[0]
		else:
			print "Error de argumentos", args

	def getTOP(self):
		return self._TOP

	def setC(self,*args):
		assert 1 <= len(args) <= 4
		if len(args) == 4:
			self._C[0] = args[0]
			self._C[1] = args[1]
			self._C[2] = args[2]
			self._C[3] = args[3]

		elif len(args) == 1:
			self._C = args[0]
		else:
			print "Error de argumentos", args

	def getC(self):
		return self._C

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

	def getRegs(self):
		return [self._IE, self._DE, self._ZE, self._OE,	self._UE, self._PE,	self._X, self._IR, self._C[0], self._C[1],self._C[2], self._TOP[0], self._TOP[1], self._TOP[2],	self._C[3], self._B]

	def setRegs(IE,DE,ZE,OE,UE,PE,X,IR,C0,C1,C2,TOP0,TOP1,TOP2,C3,B):
		self._IE=IE
		self._DE=DE
		self._ZE=ZE
		self._OE=OE
		self._UE=UE
		self._PE=PE
		self._X = X
		self._IR=IR
		self._C[0]=C0
		self._C[1]=C1
		self._C[2]=C2
		self._TOP[0]=TOP0
		self._TOP[1]=TOP1
		self._TOP[2]=TOP2
		self._C[3]=C3
		self._B=B

	def getRegNames(self):
		return ['IE','DE','ZE','OE','UE','PE','X','IR','C0','C1','C2','TOP0','TOP1','TOP2','C3','B']

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
		self.iniciar()

	def iniciar(self): #iniciar en 0000h
		self._CF=0 
		self._PF=0 
		self._AF=0 
		self._ZF=0 
		self._SF=0 
		self._TF=0 
		self._IF=0 
		self._DF=0 
		self._OF=0 

	def getRegs(self):
		return [self._CF,self._PF,self._AF,self._ZF,self._SF,self._TF,self._IF,self._DF,self._OF ]

	def setRegs(CF,PF,AF,ZF,SF,TF,IF,DF,OF):
		self._CF= CF
		self._PF= PF
		self._AF= AF
		self._ZF= ZF
		self._SF= SF
		self._TF= TF
		self._IF= IF
		self._DF= DF
		self._OF= OF

	def getRegNames(self):
		return ['CF','PF','DF','AF','ZF','SF','TF','IF','DF','OF']

#Si es llamado como ejecutable, entonces decir que esto es una librería que contiene las estructuras básicas de una fpu 8087 (pilas y registros), mostrar la doc y salir.

