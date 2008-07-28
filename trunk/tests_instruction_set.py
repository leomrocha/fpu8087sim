#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Casos de prueba de instruction_set.py
"""
import random
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
		a = random.random()
		b = random.random()
		c = a + b
		pila.push(a)
		pila.push(b)
		FADD(0,1)
		self.assertEqual(pila._pst[pila.head()],c)

	def testFADD_1(self):
		a = random.random()
		b = random.random()
		c = a + b
		pila.push(a)
		FADD(b)
		self.assertEqual(pila._pst[pila.head()],c)

if __name__ == '__main__':
    unittest.main()

