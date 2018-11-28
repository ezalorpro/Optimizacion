#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Problema de las N reinas"""

from matplotlib import pyplot as plt
from typing import *
import random
import numpy as np
import collections


class OrderedClassMembers(type):
	
	"""Meta clase para poder extraer funciones de manera ordenada"""
	
	@classmethod
	def __prepare__(mcs, name, bases):
		return collections.OrderedDict()
	
	def __new__(mcs, name, bases, classdict):
		classdict['__ordered__'] = [key for key in classdict.keys()
									if key not in ('__module__', '__qualname__')]
		return type.__new__(mcs, name, bases, classdict)


class Nqns(metaclass=OrderedClassMembers):
	
	"""Clase para definir el problema de las N reinas."""
	
	def __init__(self):
		pass
	
	@staticmethod
	def ini_nqns(n_reinas: int, _, __, ___) -> List[int]:
		"""
		
		Inicializa el tablero tomando el numero de reinas.
		
		:param n_reinas: Numero de reinas.
		:param _: None
		:param __: None
		:param ___: None
		:return: lista desde 0 hasta n_reinas.
		
		"""
		
		tablero_base = [0]
		while len(tablero_base) < n_reinas:
			tablero_base = [i for i in range(n_reinas)]
		
		return tablero_base
	
	@staticmethod
	def crear_tablero(reinas: List[int]) -> List[int]:
		"""
		
		Genera la respuesta inicial random.
		
		:param reinas: Tablero base.
		:return: Respuesta inicial random.
		
		"""
		
		random.shuffle(reinas)
		return reinas
	
	@staticmethod
	def calcular_fitness(reinas_position: List[int], n_reinas: int) -> int:
		"""
		
		Calculo del fitness para el problema de las N reinas.
		
		:param reinas_position: Posicion actual en el tablero.
		:param n_reinas: Numero de reinas.
		:return: fitness dado por el numero total de colisiones.
		
		"""
		
		colisiones = 0
		for i in range(n_reinas):
			for j in range(n_reinas):
				if reinas_position[i] - i == reinas_position[j] - j and i != j:
					colisiones += 1
				if reinas_position[i] + i == reinas_position[j] + j and i != j:
					colisiones += 1
		
		return colisiones
	
	@staticmethod
	def imprimir_respuesta(tablero: List[int], mejor_posicion: object, cola: None = None) -> None:
		"""
		
		Metodo para impirmir la mejor posicion en funcion del mejor fitness, ademas, grafica un tablero con la posicion
		de las reinas.
		
		:param tablero: Problema base.
		:param mejor_posicion: Mejor posicion encontrada.
		:param cola: Para determinar el mostrado de las figuras.
		:return: None
		
		"""
		
		print('Problema: N-queens')
		print('Posiciones en el tablero:', mejor_posicion.position)
		print('Fitness: ', mejor_posicion.fitness)
		
		board = np.zeros((len(tablero), len(tablero), 3))
		board += [0.93, 0.81, 0.63]  # color
		board[::2, ::2] = 1  # Blanco
		board[1::2, 1::2] = 1  # Blanco
		
		fig, ax = plt.subplots(figsize=(7, 6))
		ax.imshow(board, interpolation='nearest')
		
		for x, y in enumerate(mejor_posicion.position):
			ax.text(x, y, u'\u265B', size=250/len(tablero), ha='center', va='center')
		
		ax.set(xticks=[], yticks=[])
		ax.axis('image')
		
		plt.savefig("imagenes\\nqns_output.pdf", bbox_inches='tight', pad_inches=0.1, format='pdf')
		
		if cola is None:
			plt.draw()
		else:
			plt.show()
