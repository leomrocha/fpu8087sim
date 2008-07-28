#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Casos de prueba de isntruction_set.py
"""
import unittest
import random
from fpu_structure import Pila, StatusRegister, ControlRegister, StatusX86

"""
Test Pila
Fecha: 28/07/2008
Leonardo Manuel Rocha
Propósito:
	Observar que el dato que se introduce mediante FLD de instruction_set.py
	se corresponda con los datos que se almacenan en la pila
Dependencias:
	Pila
Método:
	Se crean valores enteros aleatorios y todos los posibles de TAG y se los
	inserta en la pila 
	Se comprueba que el valor almacenado corresponda con el introducido
Esperado:
	Test OK

"""
class TestPila(unittest.TestCase):

	def test_push_1(self):
		pila = Pila()
		st = 11111111
		tag = [[0,0],[0,1],[1,0],[1,1]]
		for i in range(2):
			for t in tag:
				st = random.randint(-2e10,2e10)
				pila.push(st,t)
				self.assertEqual((pila._pst[len(pila._pst)-1],pila._ptag[len(pila._pst)-1]),(st,t)) #compara la cabeza con lo insertó previamente

	def test_push_2(self):
		pila = Pila()
		st = 11111111
		for i in range (8):
			st = random.random()
			pila.push(st)
			self.assertEqual(pila._pst[len(pila._pst)-1],st) #compara la cabeza con lo insertó previamente

	def test_pop(self):
		#primero Deben introducirse elementos en la pila
		pila = Pila()
		st =[]
		for i in range (8):
			st.append(random.random())
			pila.push(st[i])
		#luego se extraen y comparan los valores
		for i in range (8):
			st.append(random.random())
			self.assertEqual(pila.pop()[0],st[i])
"""
	def test_getI(self,i):
		pass
	def test_setI(self,i,st,tag):
		pass
	def test_setI(self,i,st):
		pass
	def test_delI(self,i):
		pass
	def test_length(self):
		pass
	def test_head(self):
		pass
"""

class TestStatusRegister(unittest.TestCase):
	pass
"""
	def setTOP(self,top):

	def setTOP(self,top0,top1,top2):

	def getTOP(self):

	def setC(self,c):

	def setC(self,c0,c1,c2,c3):

	def getC(self):

	def decTOP(self):

	def incTOP(self):

"""

#class TestStatusX86(unittest.TestCase):
#	pass

class TestControlRegister(unittest.TestCase):
	pass
"""
	def setPC(self,pc):

	def setPC(self,pc0,pc1):

	def getPC(self):
	
	def setRC(self,rc):

	def setRC(self,rc0,rc1):

	def getRC(self):

	def setIC(self,ic):

	def setIC(self,ic0,ic1):

	def getIC(self):

"""


if __name__ == '__main__':
    unittest.main()
