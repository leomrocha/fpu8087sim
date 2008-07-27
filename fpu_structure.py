#!/usr/bin/env python
 # -*- coding: utf-8 -*-


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
		self.__AD =[0 for i in range(16)] #Líneas de dirección
		self.pin=[None for i in range(40)]
		self.pin[ 1 ]='GND'
		self.pin[ 2:16 ]= AD[14:0]
		self.pin[ 17 ]= 'NC'
		self.pin[ 18 ]= 'NC'
		self.pin[ 19 ]= 'CLK'
		self.pin[ 20 ]= 'GND'
		self.pin[ 21 ]= 'RESET'
		self.pin[ 22 ]= 'READY'
		self.pin[ 23 ]= 'BUSY'
		self.pin[ 24 ]= QS1
		self.pin[ 25 ]= QS0
		self.pin[ 26 ]= S0 #neg
		self.pin[ 27 ]= S1 #neg
		self.pin[ 28 ]= S2 #neg
		self.pin[ 29 ]= 'NC'
		self.pin[ 30 ]= 'NC'
		self.pin[ 31 ]= RQ/GT0 #neg
		self.pin[ 32 ]= INT
		self.pin[ 33 ]= RQ/GT1 #neg
		self.pin[ 34 ]= BHE #neg
		self.pin[ 35 : 38 ]= [0,0,0,0]#S[6:3]
		self.pin[ 39 ]= AD[15]
		self.pin[ 40 ]= 'VCC'


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
		self.__pst=[] #pila st
		self.__ptag=[] #pila de tags

	def push(self, st,tag):
		if __pst.__len__() <= 8 :
			__pst.append(st)
			__ptag.append(tag)
		else:
			print "fallo al empujar valor a la pila, demasiados valores"
			#raise  #excepción

	def push(self, st):
		if __pst.__len__() <= 8 :
			__pst.append(st)
			__ptag.append([0, 0])
		else:
			print "fallo al empujar valor a la pila, demasiados valores"
			#raise  #excepción

	def pop(self):
		return(__pst.pop(),__ptag.pop())

	def getI(self,i):
		try:
			return(__pst[i],__ptag[i])
		except:
			return(0,[1,1])

	def setI(self,i,st,tag):
		__pst[i]=st
		__ptag[i]=tag

	def setI(self,i,st):
		__pst[i]=st
		__ptag[i]=[0, 0]


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
		self.__PC = [0, 0] #Precition Control
		self._PC0=0 #
		self._PC1=0 #
		self.__RC=[0, 0] #Rounding Control
		self._RC0=0 #
		self._RC1=0 #
		self.__IC =[0, 0] #Infinity Control (0=projective, 1= affine)
		self._IC0 =0
		self._IC1 =0
		self._XXX=['X','X','X'] #últimos 3 bits reservados

	def setPC(self,pc):
		#falta checkear si pc es de dos dígitos y es solo unos y ceros
		__PC = pc

	def setPC(self,pc0,pc1):
		__PC[0] =pc0
		__PC[1] =pc1

	def getPC(self):
		return __PC
	
	def setRC(self,rc):
		__RC = rc

	def setRC(self,rc0,rc1):
		__RC[0] =rc0
		__RC[1] =rc1

	def getRC(self):
		return __RC

	def setIC(self,ic):
		__IC = ic

	def setIC(self,ic0,ic1):
		__IC[0] =ic0
		__IC[1] =ic1

	def getIC(self):
		return __IC


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
		self.__C=[0, 0, 0, 0 ] #Condition Code
		self._C0=0 #Condition Code
		self._C1=0 #
		self._C2=0 #
		self.__TOP=[0, 0, 0]#Top Of Stack Pointer
		self._C3=0 #
		self._B=0 #NEU busy

	def setTOP(self,top):
		__TOP = top

	def setTOP(self,top0,top1,top2):
		__TOP[0] = top0
		__TOP[1] = top1
		__TOP[2] = top2

	def getTOP(self):
		return __TOP

	def setC(self,c):
		__C = c

	def setC(self,c0,c1,c2,c3):
		__C[0] = c0
		__C[1] = c1
		__C[2] = c2
		__C[3] = c3

	def getC(self):
		return __C

"""
Tag Word (16 bits) #listo
"""

"""
Instruction Pointer (32 bits)
"""

"""
Data Pointer (32 bits)
"""


#Si es llamado como ejecutable, entonces decir que esto es una librería que contiene las estructuras básicas de una fpu 8087 (pilas y registros), mostrar la doc y salir.

