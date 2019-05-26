#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funciones de uso general, se puede heredar para los algoritmos o usar como modulo de funciones"""

from operator import itemgetter, attrgetter
import random
from typing import *


class General:
	
	"""
	
	Clase de funciones de uso general
	
	"""
	
	@staticmethod
	def calcular_centroide(grupo: object,
							problema_base: List[Tuple[int, int]],
		 					vector_len: int,
							vecinos: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
		"""
	
		Metodo para calcular el centroide
		
		:param grupo: Grupo de candidatos
		:return: xc, el centroide
	
		"""
		
		a = (x.position for x in vecinos)
		xc = [None] * vector_len
		
		for k, columna in enumerate(zip(*a)):
			cuentas = {key: columna.count(key) for key in set(columna)}
			columna_sorted = sorted(cuentas.items(), key=itemgetter(1), reverse=True)
			
			for j in columna_sorted:
				if j[0] not in xc:
					xc[k] = j[0]
					break
		
		while None in xc:
			miss = xc.index(None)
			xc[miss] = next(problema_base[x] for x in range(vector_len) if problema_base[x] not in xc)
		
		if sum(True if x.position == xc else False for x in grupo) > 0 and vector_len > 1:
			b = random.sample(range(vector_len), 2)
			xc[b[1]], xc[b[0]] = xc[b[0]], xc[b[1]]
		
		return xc
	
	@staticmethod
	def getbestsolution(soluciones: List[object], cantidad: int = 1) -> object:
		"""

		Metodo para obtener la mejor solucion del grupo de soluciones actuales.

		:param soluciones: Grupo de soluciones al que se le obtendra la mejor respuesta basado en el fitness
		:param cantidad: Numero de soluciones a retornar
		:return: La mejor o mejores soluciones, ie. la solucion o soluciones con menor fitness

		"""
		
		sorted_fitnes = sorted(soluciones, key=attrgetter('fitness'))
		
		if cantidad == 1:
			return sorted_fitnes[0]
		else:
			return sorted_fitnes[:cantidad]
	
	@staticmethod
	def calcular_vecinos(index: int, candidato: List[Tuple[float]], visual: int, grupo: List[object]) -> List[object]:
		"""

		Metodo para calcular los vecinos dado el rango visual

		:param index: Indice del pez actual
		:param candidato: candidato actual
		:param visual: Rango visual a utilizar para el calculo de los vecinos
		:param grupo: Grupo de candidatos
		:return: vecinos, una lista con los vecinos obtenidos

		"""
		
		vecinos = []
		for j, nCandidato in enumerate(grupo):
			if j != index:
				distancia = sum([1 if A == B else 0 for A, B in zip(candidato, nCandidato.position)])
				if distancia > visual:
					vecinos.append(nCandidato)
		return vecinos


