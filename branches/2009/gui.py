#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass
try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)


from fpu_structure import * #mas comentarios
#from instruction_set import * #Por el momento queda así
import reduced_instruction_set as iset
from datahandling import *
import main #debe estar después de la instanciación de iset



class FPU_GUI:
	def __init__(self):
		main.saveState()
		self._last_instruction = ""
		#Set the Glade file
		self.gladefile = "gui/fpugui.glade/fpuguiglade"
		self.wTree = gtk.glade.XML(self.gladefile) 
		#Get the Main Window, and connect the "destroy" event
		self.windowST = self.wTree.get_widget("ST_Stack")
		if (self.windowST):
			self.windowST.connect("destroy", gtk.main_quit)
		#self.windowReg = self.wTree.get_widget("Registers")
		#if (self.windowReg):
		#	self.windowReg.connect("destroy", gtk.main_quit)
		self.windowConsole = self.wTree.get_widget("Consola")
		if (self.windowConsole):
			self.windowConsole.connect("destroy", gtk.main_quit)
		
		#Create our dictionay and connect it
		dic = {
			"on_Salir_destroy" : gtk.main_quit,
			"on_Ejecutar_clicked" : self.ejecutar,
			"on_Deshacer_clicked" : self.deshacer,
			"on_Reiniciar_clicked" : self.reiniciar,
			"on_Salir_clicked" : gtk.main_quit,
			}
		self.wTree.signal_autoconnect(dic)

	def ejecutar(self, widget):
		lines = [] #cargar las líneas de manera auxiliar acá, 
					#para sacarlas en orden hay que usar pop(0) (ojo con el 0 que debe estar)
		#obtener la consola de entrada
		consola=self.wTree.get_widget("entrada_consola")
		buffConsola = consola.get_buffer()
		numlines=buffConsola.get_line_count()
		beginIter = buffConsola.get_start_iter() #buffConsola.get_iter_at_line(0)
		endIter = buffConsola.get_end_iter()
		text= buffConsola.get_text(beginIter,endIter)
		#parsear los datos de entrada		
		#verificar que sean datos válidos
		#enviarselos a main para su ejecución
		commands = main.parse(text)
		for comm in commands:
			main.execute_command(comm)
		self._last_instruction = comm

		#actualizar registros
		self.actualizarRegs()
		self.actualizarPila()
		self.actualizarResultados()

	def deshacer(self, widget):
		main.undo()
		self.actualizarRegs()
		self.actualizarPila()



	def reiniciar(self, widget):
		main.rebootFPU()
		self.actualizarRegs()
		self.actualizarPila()

	#actualiza los valores de la salida de los registros
	def actualizarRegs(self):
		try:		
			#actualizar registros de status
			#print "actualizando registros de status"
			regs_vals = iset.status.getRegs()
			regs_noms = iset.status.getRegNames()
			#print regs_vals
			#print regs_noms
			for i in range (16):
				self.wTree.get_widget(regs_noms[i]).set_text(str(regs_vals[i]))
		except:
			pass
		try:
			#actualizar registros de control
			#print "actualizando registros de control"
			regc_vals = iset.control.getRegs()
			regc_noms = iset.control.getRegNames()
			#print regc_vals
			#print regc_noms
			for i in range (16):
				self.wTree.get_widget(regc_noms[i]).set_text(str(regc_vals[i]))
			#actualizar registros de statusX86
		except:
			pass

	def actualizarResultados(self):
		nom_res = "resultados"
		self.wTree.get_widget(nom_res).set_text(str(iset.pila.getI(iset.pila.head())[0]))#(str(iset.res))		
		nom_text = "lastInstruction"
		lastI = ""
		for el in self._last_instruction:
			lastI+=" "
			lastI+=str(el)
		self.wTree.get_widget(nom_text).set_text(lastI)
		
	#actualiza los valores de la salida de la Pila
	def actualizarPila(self):
		for i in range(8):
			reg=[None,None]
			nom_bin = "ST"+str(i)+"_bin"
			nom_rep = "ST"+str(i)+"_rep"
			nom_tag = "tag"+str(i)
			#print nom_bin
			#print nom_rep
			#print nom_tag
			head = iset.pila.head()-i
			#print head
			try:
				#print "pila.head()= ", pila.head()
				reg=iset.pila.getI(head)
			except:
				reg[0] = 00000000000000000000 
				reg[1] = [1,1] 
			#print reg
			#print i
			self.wTree.get_widget(nom_bin).set_text(str(f2bin(reg[0])))
			self.wTree.get_widget(nom_rep).set_text(str(reg[0]))
			self.wTree.get_widget(nom_tag).set_text(str(reg[1]))

if __name__ == "__main__":
	fpugui = FPU_GUI()
	gtk.main()


