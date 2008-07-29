#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Casos de prueba de instruction_set.py
"""
import random
import math
#módulo de Tests Unitarios
import unittest

#importa el módulo a testear:
from reduced_instruction_set import *

"""
Test FLD
Fecha: 28/07/2008
Leonardo Manuel Rocha
Propósito:
	Observar que el dato que se introduce mediante FLD de instruction_set.py
	se corresponda con los datos que se almacenan en la pila
Dependencias:
	Pila
	StatusRegister
Método:
	Se crean valores enteros positivos, cero y negativos los que se introducirán
	mediante FLD.
	Se comprueba que el valor almacenado corresponda con el introducido
Esperado:
	Test OK

"""
class TestFLD(unittest.TestCase):
	def testFLDpos(self):
		pos = 111111 #usar un valor positivo
		#usar FLD
		FLD(pos)
		#verificar que el valor de la pila sea el que se ingresó
		self.assertEqual(pila.getI(pila.head())[0],pos)
	def testFLDneg(self):
		neg = -111111 #usar un valor negativo
		#usar FLD
		FLD(neg)
		#verificar que el valor de la pila sea el que se ingresó
		self.assertEqual(pila.getI(pila.head())[0],neg)
	def testFLDcero(self):
		cero = 0 #usar el cero
		#usar FLD
		FLD(cero)
		#verificar que el valor de la pila sea el que se ingresó
		self.assertEqual(pila.getI(pila.head())[0],cero)

#Test ABS
#
#class TestFABS(unittest.TestCase):
#	pass

#Test FADD
class TestFADD(unittest.TestCase):

	def testFADD_1(self):
		a = random.randint(-2**10,2**10)
		b = random.randint(-2**10,2**10)
		c = a + b
		pila.push(a)
		pila.push(b)
		#print pila._pst
		FADD(0,1)
		#print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],c)

#Test FSUB
class TestFSUB(unittest.TestCase):
	def testFSUB(self):
		for i in range(8):
			pila.pop()
		a = random.randint(-2**10,2**10)
		b = random.randint(-2**10,2**10)
		c =   b - a 
		pila.push(a)
		pila.push(b)
		#print pila._pst
		FSUB(0,1)
		#print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],c)

class TestFMUL(unittest.TestCase):
	def testFMUL(self):
		for i in range(8):
			pila.pop()
		a = random.randint(-2**6,2**6)
		b = random.randint(-2**6,2**6)
		c =   a * b
		pila.push(a)
		pila.push(b)
		print pila._pst
		FMUL(0,1)
		print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],c)

class TestFDIV(unittest.TestCase):
	def testFDIV(self):
		for i in range(8):
			pila.pop()
		a = random.randint(-2**6,2**6)
		b = random.randint(-2**6,2**6)
		c =   b / a
		pila.push(a)
		pila.push(b)
		print pila._pst
		FDIV(0,1)
		print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],c)

class TestFCOS(unittest.TestCase):
	def testFCOS(self):
		for i in range(8):
			pila.pop()
		a = random.randint(-2**6,2**6)
		b = math.cos(a)
		pila.push(a)
		#print pila._pst
		FCOS()
		#print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],b)

class TestFIN(unittest.TestCase):
	def testFSIN(self):
		for i in range(8):
			pila.pop()
		a = random.randint(-2**6,2**6)
		b = math.sin(a)
		pila.push(a)
		#print pila._pst
		FSIN()
		#print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],b)

class TestFSINCOS(unittest.TestCase):
	def testFSINCOS(self):
		for i in range(8):
			pila.pop()
		a = random.randint(-2**6,2**6)
		b = math.cos(a)
		c = math.sin(a)
		pila.push(a)
		#print pila._pst
		FSINCOS()
		#print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],b)
		self.assertEqual(pila.getI(pila.head()-1)[0],c)

class TestFSQRT(unittest.TestCase):
	def testFSQRT(self):
		for i in range(8):
			pila.pop()
		a = random.randint(0,2**6)
		b = math.sqrt(a)
		pila.push(a)
		#print pila._pst
		FSQRT()
		#print pila._pst
		self.assertEqual(pila.getI(pila.head())[0],b)



if __name__ == '__main__':
    unittest.main()

