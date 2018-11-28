#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Problema del agente viajero"""

from functools import lru_cache
from math import sqrt
from matplotlib import pyplot as plt
from typing import *
import math
import random
import collections
import copy

plt.rcParams["font.family"] = "Times New Roman"


class OrderedClassMembers(type):
	
	"""Meta clase para poder extraer funciones de manera ordenada"""
	
	@classmethod
	def __prepare__(mcs, name, bases):
		return collections.OrderedDict()

	def __new__(mcs, name, bases, classdict):
		classdict['__ordered__'] = [key for key in classdict.keys()
									if key not in ('__module__', '__qualname__')]
		return type.__new__(mcs, name, bases, classdict)


class TSP(metaclass=OrderedClassMembers):
	
	"""Clase para definir el problema del agente viajero."""
	
	def __init__(self):
		
		"""El unico atributo es la ciudad inicial del problema, esta ciudad sera el inicio y el final del recorrido."""
		
		self.ciudad_fija = 0
	
	def ini_tsp(self, n_ciudades: int, size_space: int, dimension: int, _) -> List[Tuple[int, int]]:
		"""
		
		Inicializa las ciudades base a resolver. La creacion de las ciudades posee dos formas, uno de manera random, una
		con forma de circunferencia + ruido, ademas, se agrega en comentarios un set de ciudades fijo para probar
		el algoritmo de manera mas consistente.
		
		:param n_ciudades: Numero de ciudades a recorrer
		:param size_space: Tamaño del espacio en el que se ubican las ciudades ig. 100x100
		:param dimension: dimension del problema (x1, x2, x3,...,x_dimension)
		:param _: None
		:return: Las ciudades generadas
		
		"""
		
		cities_base = [0]
		
		# random cities
		while len(cities_base) < n_ciudades:
			cities_base = list(set([tuple(random.sample(range(size_space), dimension)) for _ in range(n_ciudades)]))
		
		# "benchmark"
		"""
		cities_base = [(18, 55), (33, 85), (77, 30), (4, 28), (94, 0), (49, 13), (90, 61), (22, 17), (7, 56), (89, 71),
						(55, 73), (56, 35), (76, 36), (58, 75), (13, 83), (60, 59), (85, 48), (32, 41), (92, 27), (7, 93)]
		"""
		# ciudades con forma de circunferencia + "ruido"
		# cities_base = points_on_circumference(n=n_ciudades)
		
		return cities_base
	
	@staticmethod
	def crear_recorrido(cities: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
		"""
		
		Genera el recorrido a realizar
		
		:param cities: Ciudades base menos la ciudad inicial, el recorrido de crea a partir de esta.
		:return: recorrido random
		
		"""
		random.shuffle(cities)
		return cities
	
	def calcular_fitness(self, recorrido: List[Tuple[int, int]], _) -> float:
		"""
		
		Metodo para calcular el fitness, para este problema de TSP se plantea como funcion fitness la suma de distancias
		euclidianas entre cada ciudad de manera secuencial partiendo de la ciudad fija y finalizando en la misma.
		
		:param recorrido: Recorrido a seguir entre las ciudades.
		:param _: None
		:return: fitness
		
		"""

		fishcost = sum(map(self.distancia_euclidean, recorrido[:-1], recorrido[1:]))
		fishcost += self.distancia_euclidean(recorrido[-1], recorrido[0])
		return fishcost
	
	def imprimir_respuesta(self, problema_base: List[Tuple[int, int]], bestfitnes: object, cola: None = None) -> None:
		"""

		Metodo para imprimir una representacion de los resultados obtenidos

		:param problema_base: Ciudades base y por tanto, el problema a resolver
		:param bestfitnes: objeto con el mejor fitness encontrado junto con la posicion para dicho fitness
		:param cola: Para determinar el mostrado de las figuras.
		:return: None

		"""
		base = copy.deepcopy(problema_base)
		bestfitnes.position.append(bestfitnes.position[0])
		
		plt.figure(figsize=(8, 6.5))
		plt.scatter(*zip(*base))
		
		plt.title('Mejor respuesta encontrada, fitness %.3f' % bestfitnes.fitness)
		plt.plot(*zip(*bestfitnes.position))

		print('Problema: TSP')
		print('Ciudades base:' + str(base))
		print('Recorrido:' + str(bestfitnes.position))
		print('Fitness: ' + str(bestfitnes.fitness))
		plt.savefig("imagenes\\tsp_output.png", bbox_inches='tight', pad_inches=0.1, format='png')
		
		if cola is None:
			plt.draw()
		else:
			plt.show()

	@lru_cache(maxsize=None)
	def distancia_euclidean(self, punto1: Tuple[int, int], punto2: Tuple[int, int]) -> float:
		"""
		
		Metodo para el calculo de la distancia euclidiana
		
		:param punto1: se explica solo
		:param punto2: se explica solo
		:return: distancia entre el punto 1 y el punto 2
		
		"""
		
		return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(punto1, punto2)))
	
	@staticmethod
	def points_on_circumference(center=(50, 50), r=40, n=20):
		"""
		
		Metodo para general las ciudades en un patron circular
		
		:param center: Centro de la circunferencia
		:param r: Radio de la circunferencia
		:param n: Numero de puntos, o sea, numero de ciudades
		:return: ciudades generadas
		
		"""
		
		return [(random.uniform(-10, 10) + center[0] + (math.cos(2 * math.pi / n * x) * r),
				 random.uniform(-10, 10) + center[1] + (math.sin(2 * math.pi / n * x) * r)) for x in range(0, n + 1)]

