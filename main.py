#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import re
import copy
#import instruction_set as iset #modificado por el momento
import reduced_instruction_set as iset
from fpu_structure import *

uesp = None #ultimo_elemento_sacado_de_pila

uesp_temp = None #ultimo_elemento_sacado_de_pila
pila_temp = None
control_temp = None
status_temp = None
pinout_temp = None
statusX86_temp = None

def parse(text):
	lines = text.splitlines()
	i = 0
	for l in lines:
		lines[i]=l.split() 
		j=0
		for param in lines[i]: #aca convierte a entero el elemento de entrada
			try:
				lines[i][j]=int(param)#por el momento solo soporta enteros, de todas formas, la entrada debe ser un número en decimal, binario, octal u hexadecimal, puesto que el fpu no sabe que es
			except:
				pass
			j+=1
		i+=1
	return lines

def execute_command(commlista):
	saveState()
	comm = commlista[0]
	params = commlista[1:]
	#probando una nueva manera de hacer las cosas, con una cadena de texto
	paramline = "("
	i=0
	for p in params:
		if i>0:
			paramline+=", "
		paramline+=str(p)
		i+=1
	paramline += ")"
	commline = "iset."+comm + paramline
	try:
		#iset.__getattribute__(comm)(params)
		#eval(comm)(p1,p2,p3...)
		exec commline
		#print "uesp", iset.uesp
		#print "res", iset.res
	except:
		#print "No existe la función", comm
		#print "o los parámetros",params," son incorrectos"
		print "línea incorrecta:",commline

def undo():
	global uesp_temp, pila_temp, control_temp, status_temp
	uesp = uesp_temp #ultimo_elemento_sacado_de_pila
	iset.pila = pila_temp#copy.copy(pila_temp) #copy.deepcopy(pila_temp)
	iset.control = control_temp#copy.copy(control_temp) # copy.deepcopy(control_temp)
	iset.status = status_temp#copy.copy(status_temp) #copy.deepcopy(status_temp)
	#iset.pinout = #copy.copy(pinout_temp) #copy.deepcopy(pinout_temp)
	#iset.statusX86 = #copy.copy(statusX86_temp) #copy.deepcopy(statusX86_temp)

def rebootFPU():
	iset.pila = None
	iset.pila = Pila()
	iset.control.iniciar()
	iset.status.iniciar()
	iset.pinout.iniciar()
	iset.statusX86.iniciar()

def saveState():
	global uesp_temp, pila_temp, control_temp, status_temp
	#print "Guarda el estado"
	uesp_temp = uesp #ultimo_elemento_sacado_de_pila
	pila_temp = copy.deepcopy(iset.pila) #copy.copy(iset.pila) #
	control_temp = copy.deepcopy(iset.control) #copy.copy(iset.control) #
	status_temp = copy.deepcopy(iset.status) #copy.copy(iset.status) #
	pinout_temp = copy.deepcopy(iset.pinout)# copy.copy(iset.pinout) #
	statusX86_temp = copy.deepcopy(iset.statusX86) #copy.copy(iset.statusX86) #

def cleanState():
	global uesp_temp, pila_temp, control_temp, status_temp
	uesp_temp = None #ultimo_elemento_sacado_de_pila
	pila_temp = None
	control_temp = None
	status_temp = None
	#pinout_temp = None
	#statusX86_temp = None
	
#si es llamado como ejecutable
#Realizar la instanciación de los módulos necesarios
if __name__ == "__main__":
	pass

