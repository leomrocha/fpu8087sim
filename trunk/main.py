#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import re
import copy
#import instruction_set as iset #modificado por el momento
import reduced_instruction_set as iset

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
	except:
		#print "No existe la función", comm
		#print "o los parámetros",params," son incorrectos"
		print "línea incorrecta:",commline

def undo():
	uesp = uesp_temp #ultimo_elemento_sacado_de_pila
	pila = copy.deepcopy(pila_temp)
	control = copy.deepcopy(control_temp)
	status = copy.deepcopy(status_temp)
	pinout = copy.deepcopy(pinout_temp)
	statusX86 = copy.deepcopy(statusX86_temp)

def rebootFPU():
	uesp.iniciar()
	pila.iniciar()
	control.iniciar()
	status.iniciar()
	pinout.iniciar()
	statusX86.iniciar()

def saveState():
	uesp_temp = uesp #ultimo_elemento_sacado_de_pila
	pila_temp = copy.copy(pila) #copy.deepcopy(pila)
	control_temp = copy.copy(pila) #copy.deepcopy(control)
	status_temp = copy.copy(pila) #copy.deepcopy(status)
	pinout_temp = copy.copy(pila) #copy.deepcopy(pinout)
	statusX86_temp = copy.copy(pila) #copy.deepcopy(statusX86)

def cleanState():
	uesp_temp = None #ultimo_elemento_sacado_de_pila
	pila_temp = None
	control_temp = None
	status_temp = None
	pinout_temp = None
	statusX86_temp = None
	
#si es llamado como ejecutable
#Realizar la instanciación de los módulos necesarios
if __name__ == "__main__":
	pass

