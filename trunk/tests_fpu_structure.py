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
	Especificado en cada test en particular
Dependencias:
	Pila
Método:
	Especificado en cada test en particular
Esperado:
	Test OK

"""
class TestPila(unittest.TestCase):
	"""
	Propósito:
		Observar que el dato que se introduce en la pila mediante
		la primer forma de realizar push
		se corresponda con los datos que se lee de la misma
	Dependencias:
		Pila
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila
		Se comprueba que el valor almacenado corresponda con el introducido
	"""
	def test_push_1(self):
		pila = Pila()
		st = 11111111
		tag = [[0,0],[0,1],[1,0],[1,1]]
		for i in range(2):
			for t in tag:
				st = random.randint(-2e10,2e10)
				pila.push(st,t)
				self.assertEqual((pila._pst[len(pila._pst)-1],pila._ptag[len(pila._pst)-1]),(st,t)) #compara la cabeza con lo insertó previamente

	"""
	Propósito:
		Observar que el dato que se introduce en la pila mediante
		la segunda forma de realizar push
		se corresponda con los datos que se lee de la misma
	Dependencias:
		Pila
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila
		Se comprueba que el valor almacenado corresponda con el introducido
	"""
	def test_push_2(self):
		pila = Pila()
		st = 11111111
		for i in range (8):
			st = random.random()
			pila.push(st)
			self.assertEqual(pila._pst[len(pila._pst)-1],st) #compara la cabeza con lo insertó previamente
	"""
	Propósito:
		Observar que el dato que se introduce en la pila mediante
		la segunda forma de realizar push
		se corresponda con los datos que se lee de la misma
	Dependencias:		
		Pila
		Considera que Pila.push(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila
		Se extraen los valores y se comprueba que correspondan con los 
		introducidos previamente
	"""
	def test_pop(self):
		#primero Deben introducirse elementos en la pila
		pila = Pila()
		st =[]
		for i in range (8):
			st.append(random.random())
			pila.push(st[i])
		#luego se extraen y comparan los valores
		#print st
		for i in range (8):
			self.assertEqual(pila.pop()[0],st[7-i])
	"""
	Propósito:
		Observar que el dato que se introduce en la pila mediante
		la segunda forma de realizar push
		se corresponda con los datos que se lee de la misma
	Dependencias:		
		Pila
		Considera que Pila.push(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila
		Se extraen los valores y se comprueba que correspondan con los 
		introducidos previamente
	"""
	def test_getI(self):
		#primero Deben introducirse elementos en la pila
		pila = Pila()
		st =[]
		for i in range (8):
			st.append(random.random())
			pila.push(st[i])
		#luego se extraen y comparan los valores
		#print st
		#print pila._pst
		#print pila._ptag
		for i in range (8):
			self.assertEqual(pila.getI(i)[0],st[i])

	"""
	Propósito:
		Observar que se devuelva correctamente el índice de la cabeza de la pila
	Dependencias:		
		Pila
		Considera que Pila.push(*args) funciona correctamente
		Considera que Pila.getI(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila.
		Luego de cada valor insertado se corrobora que el valor en ese punto
		corresponda con el valor recién insertado (lo que corrobora que es la
		cabeza de la pila)
	"""
	def test_head(self):
		pila = Pila()
		st = 11111111
		tag = [[0,0],[0,1],[1,0],[1,1]]
		for i in range(2):
			for t in tag:
				st = random.randint(-2e10,2e10)
				pila.push(st,t)
				self.assertEqual(pila.getI(pila.head()),(st,t)) 
	"""
	Propósito:
		Observar que se devuelva correctamente la longitud de la pila
	Dependencias:		
		Pila
		Considera que Pila.push(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila.
		Luego de cada valor insertado se corrobora que el índice actual (i+1 por
		que este comienza en cero) corresponda con pila.length()
	"""

	def test_length(self):
		pila = Pila()
		st = 11111111
		self.assertEqual(0,pila.length())
		for i in range (8):
			st = random.random()
			pila.push(st)
			self.assertEqual(i+1,pila.length())

	"""
	Propósito:
		Observar que se borren correctamente los valores de la pila
	Dependencias:		
		Pila
		Considera que Pila.push(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila.
		Luego  se borra siempre el primer valor de la pila con el comando
		pila.delI(0) y se espera el retorno True
	"""
	def test_delI(self):
		#primero Deben introducirse elementos en la pila
		pila = Pila()
		st =[]
		for i in range (8):
			st.append(random.random())
			pila.push(st[i])
		#luego se extraen y comparan los valores
		for i in range (8):
			#print pila.delI(0)
			self.assertEqual(True,pila.delI(0))		
	"""
	Propósito:
		Observar que el dato que se introduce en la pila mediante
		la primer forma de realizar Pila.setI() (con 2 argumentos)
		se corresponda con los datos que se lee de la misma
	Dependencias:
		Pila	
		Considera que Pila.push(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila
		Se comprueba que el valor almacenado corresponda con el introducido
	"""
	def test_setI_1(self):
		pila = Pila()
		st = 0000000
		tag = [[0,0],[0,1],[1,0],[1,1]]
		#se llena la pila con valores conocidos
		for i in range(8):
			pila.push(st,tag[3])
		#se cambian todos los valores y se corrobora que hayan sido cambiados 
		#exitosamente
		st = []
		i=0
		for j in range (2):
			for t in tag:
				st.append(random.random())
				pila.setI(i,st[i],t)
				self.assertEqual(pila.getI(i),(st[i],t))
			i+=1
	"""
	Propósito:
		Observar que el dato que se introduce en la pila mediante
		la segunda forma de realizar Pila.setI() (con 2 argumentos)
		se corresponda con los datos que se lee de la misma
	Dependencias:
		Pila	
		Considera que Pila.push(*args) funciona correctamente
	Método:
		Se crean valores enteros aleatorios y todos los posibles de TAG y se los
		inserta en la pila
		Se comprueba que el valor almacenado corresponda con el introducido
	"""
	def test_setI_2(self):
		pila = Pila()
		st = 0000000
		tag = [1,1]
		#se llena la pila con valores conocidos
		for i in range(8):
			pila.push(st,tag)
		#se cambian todos los valores y se corrobora que hayan sido cambiados 
		#exitosamente
		st = []
		for i in range (8):
			st.append(random.random())
			pila.setI(i,st[i])
			self.assertEqual(pila.getI(i)[0],st[i])


#class TestStatusX86(unittest.TestCase):
#	pass

class TestControlRegister(unittest.TestCase):

	def test_setPC_1(self):
		control = ControlRegister()
		PC =[[0,0],[0,1],[1,0],[1,1]]
		for pc in PC:
			control.setPC(pc)
			self.assertEqual(pc,control._PC)

	def test_setPC_2(self):
		control = ControlRegister()
		PC =[[0,0],[0,1],[1,0],[1,1]]
		for pc in PC:
			control.setPC(pc[0],pc[1])
			self.assertEqual(pc,control._PC)

	#asume que setPC() funciona correctamente
	def getPC(self):
		control = ControlRegister()
		PC =[[0,0],[0,1],[1,0],[1,1]]
		for pc in PC:
			control.setPC(pc[0],pc[1])
			self.assertEqual(control.getPC(),pc)


	def test_setRC_1(self):
		control = ControlRegister()
		RC =[[0,0],[0,1],[1,0],[1,1]]
		for rc in RC:
			control.setRC(rc)
			self.assertEqual(rc,control._RC)

	def test_setRC_2(self):
		control = ControlRegister()
		RC =[[0,0],[0,1],[1,0],[1,1]]
		for rc in RC:
			control.setRC(rc[0],rc[1])
			self.assertEqual(rc,control._RC)

	#asume que setRC() funciona correctamente
	def getRC(self):
		control = ControlRegister()
		RC =[[0,0],[0,1],[1,0],[1,1]]
		for rc in RC:
			control.setRC(rc[0],rc[1])
			self.assertEqual(control.getRC(),rc)


	def test_setIC_1(self):
		control = ControlRegister()
		IC =[[0,0],[0,1],[1,0],[1,1]]
		for ic in IC:
			control.setIC(ic)
			self.assertEqual(ic,control._IC)

	def test_setIC_2(self):
		control = ControlRegister()
		IC =[[0,0],[0,1],[1,0],[1,1]]
		for ic in IC:
			control.setIC(ic[0],ic[1])
			self.assertEqual(ic,control._IC)

	#asume que setIC() funciona correctamente
	def getIC(self):
		control = ControlRegister()
		IC =[[0,0],[0,1],[1,0],[1,1]]
		for ic in IC:
			control.setIC(rc[0],rc[1])
			self.assertEqual(control.getIC(),ic)

class TestStatusRegister(unittest.TestCase):
	pass
"""
	def test_setTOP_1(self):

	def test_setTOP_2(self):

	def getTOP(self):

	def test_setC_1(self):

	def test_setC_2(self):

	def test_getC(self):

	def test_decTOP(self):

	def test_incTOP(self):
"""


if __name__ == '__main__':
    unittest.main()
