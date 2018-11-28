#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Algoritmo de escuela de peces artificiales (AFSA). Se puede utilizar por medio de la clase Optimizar, para mas detalles
estudiar el ejemplo Ejecucion_simple.py o Ejecucion_multiple.py
	
	*Nota 1: El AFSA se modifico ligeramente para el caso de los problemas continuos dado que esta planteado para
	problemas combinatorios, si se quiere un mejor desempeño para estos casos, se recomienda plantear el AFSA para
	problemas continuos.

"""

from typing import *
from funciones_generales import General
import copy
import random
import time


class Fish:
	
	"""Clase para definir los objetos tipo pez(Fish)"""
	
	__slots__ = ('position', 'fitness')
	
	def __init__(self, p: List[Tuple[float, float]], f: float) -> None:
		self.position = p
		self.fitness = f


class AFSA(General):
	
	"""Clase base de la escuela de peces artificiales, incluye los movimientos necesarios para el algoritmo."""
	
	def __init__(self,
				 maxiteration: str = 5000,
				 visual: str = 4,
				 crowfactor: str = 0.83,
				 n_fish: str = 10,
				 step: str = 1,
				 try_numbers: str = 10,
				 problema: List[Tuple[int, int]] = None,
				 funciones: List[Callable] = None) -> None:
		"""
		
		:param maxiteration: Maximas iteraciones a realizar.
		:param visual: Rango visual de los peces.
		:param crowfactor: Factor de congestion.
		:param n_fish: Numero de peces.
		:param step: Cantidad de swaps a realizar por move_behavior_modificado()
		:param try_numbers: Numero de intentos de obtener una mejor posicion con prey_behavior()
		:param problema: Problema base a resolver.
		:param funciones: lista de funciones correspondiente al problema a resolver.
		:return: None
		
		"""
		
		self.Maxiteration = int(maxiteration)
		self.visual = float(visual)
		self.crowfactor = float(crowfactor)
		self.n_fish = int(n_fish)
		self.step = int(step)
		self.try_numbers = int(try_numbers)
		self.tipo_de_problema = problema
		self.NC = 0
		self.GroupFish = []
		
		self.crear_vector, self.calcular_fitness, self.imprimir_respuesta = funciones
		
		self.problema_base = problema
		
		for num in range(self.n_fish):
			vector = self.crear_vector(self.problema_base)
			fit = self.calcular_fitness(vector, len(vector))
			fish_ini = Fish(copy.copy(vector), copy.copy(fit))
			self.GroupFish.append(fish_ini)
			
		self.vector_len = len(self.problema_base)
		
	def empezar(self, queue: None = None, show_results: bool = True) -> Tuple[List[float], Fish, int]:
		"""
		
		Empieza el proceso de optimizacion, hace el llamado para guardar el mejor pez despues de cada iteracion y llama
		a la funcion de imprimir respuesta.
		
		:param queue: Variable de multiproceso (cola), se utiliza para devolver informacion al thread principal.
		:param show_results: Bandera para escoger el llamado a imprimir_respuesta().
		:returns: Lista con la evolucion del fitness, objeto Fish con la mejor solucion encontrada, numero de
		operaciones realizadas (iteraciones * n_fish).
		
		"""
		
		start = time.time()
		mejor_fish = []
		fitness_evolution = []
		interval = self.Maxiteration*0.2/100
		count = 0
		for iteration in range(self.Maxiteration):
			for index, fish in enumerate(self.GroupFish):
				_ = self.follow_behavior(index, fish)
			
			mejor_fish.append(copy.deepcopy(self.getbestsolution(self.GroupFish)))
			
			if count > interval:
				count = 0
				print(f'{(iteration/self.Maxiteration)*100:.2f} %')
				fitness_evolution.append(self.getbestsolution(mejor_fish).fitness)
			count += 1
			
		end = time.time()
		tiempo = end - start
		print("\nTiempo transcurrido: %.3f" % tiempo)
		
		if show_results:
			self.imprimir_respuesta(self.problema_base, self.getbestsolution(mejor_fish), queue)
		
		operaciones = self.Maxiteration * self.n_fish
		if queue is not None:
			paquete = [fitness_evolution, copy.deepcopy(self.getbestsolution(mejor_fish)), operaciones]
			queue.put(paquete)
		
		return fitness_evolution, copy.deepcopy(self.getbestsolution(mejor_fish)), operaciones
	
	def follow_behavior(self, index: int, fish: Fish) -> int:
		"""
		
		Se obtiene el mejor pez dentro de los vecinos del pez actual, se asigna su posicion en caso de que el fitness
		sea mejor y que no haya mucha congestion.
		
		:param index: Indice del pez actual
		:param fish: Pez actual
		:return: 0, con fines de acabar la funcion
		
		"""
		
		self.vecinos = self.calcular_vecinos(index, fish.position, self.visual, self.GroupFish)
		
		try:
			best_vecino = self.getbestsolution(self.vecinos)
			if len(self.vecinos)/self.n_fish < self.crowfactor and best_vecino.fitness < fish.fitness:
				self.GroupFish[index].position = copy.copy(best_vecino.position)
				self.GroupFish[index].fitness = self.calcular_fitness(self.GroupFish[index].position, self.vector_len)
				self.NC += 1
				return 0
			
			elif int(self.visual*(1-(self.NC/self.Maxiteration))) > 0:
				visual2 = int(self.visual*(1-(self.NC/self.Maxiteration)))
				_ = self.prey_behavior(index, fish, visual2)
			else:
				_ = self.swarm_behavior(index, fish)
				return 0
			
		except IndexError:
			_ = self.move_behavior_modificado(index, fish)
			return 0
		
	def prey_behavior(self, index: int, fish: Fish, visual: int) -> int:
		"""
		
		Se escoge de manera random un pez vecino, si su fitness es mejor, la posicion del pez actual se reemplaza con la
		de dicho pez, este proceso se repite try_numbers veces.
		
		:param index: Indice del pez actual
		:param fish: Pez actual
		:param visual: Rango visual del pez actual
		:return: 0, con fines de acabar la funcion
		
		"""
		
		self.vecinos = self.calcular_vecinos(index, fish.position, visual, self.GroupFish)
		
		try:
			for intentos in range(self.try_numbers):
				maybe = random.choice(self.vecinos)
				if maybe.fitness < fish.fitness:
					self.GroupFish[index].position = copy.copy(maybe.position)
					self.GroupFish[index].fitness = self.calcular_fitness(self.GroupFish[index].position, self.vector_len)
					self.NC += 1
					return 0
			
			self.GroupFish[index].position = copy.copy(maybe.position)
			self.GroupFish[index].fitness = self.calcular_fitness(self.GroupFish[index].position, self.vector_len)
			_ = self.swarm_behavior(index, fish)
			return 0
		
		except ValueError:
			_ = self.move_behavior_modificado(index, fish)
			return 0
		
	def swarm_behavior(self, index: int, fish: Fish) -> int:
		"""
		
		Se calcula el centroide entre los vecinos, al pez actual se le asigna la posicion dada por el centroide si el
		fitness en dicha posicion es mejor y si la posicion no esta muy congestionada.
		
		:param index: Indice del pez actual
		:param fish: Pez actual
		:return: 0, con fines de acabar la funcion
		
		"""
		
		if len(self.vecinos)/self.n_fish < self.crowfactor:
			
			xc = self.calcular_centroide(self.GroupFish)
			
			if self.calcular_fitness(xc, self.vector_len) < fish.fitness:
				self.GroupFish[index].position = copy.copy(xc)
				self.GroupFish[index].fitness = self.calcular_fitness(self.GroupFish[index].position, self.vector_len)
				self.NC += 1
				return 0
			else:
				_ = self.move_behavior_modificado(index, fish)
				return 0
		else:
			_ = self.move_behavior_modificado(index, fish)
			return 0
	
	def move_behavior_modificado(self, index: int, fish: Fish) -> int:
		"""
		
		Se modifico el move_behavior() original propuesto por Yun Cai (2010) el cual consistia en obtener una posicion
		random y sustituir la posicion del pez actual si dicha posicion generaba un mejor fitness.
		
		Dado que en las pruebas este metodo no genero buenos resultados se opto por realizar un numero step de swaps
		entre posiciones random, el mejor valor conseguido para step fue de 1 y 2, para mayores valores de step, se tiende
		a generar una respuesta parecida al move_behavior() original, dado que se termina obteniendo una posicion random
		
		Por otro lado, se agrego una version alterna en caso de que el problema a resolver sea de tipo continuo.
		
		:param index: Indice del pez actual
		:param fish: Pez actual
		:return: 0, con fines de acabar la funcion
		
		"""
		if self.vector_len == 1:
			best = copy.copy(self.getbestsolution(self.GroupFish))
			random_move = []
			
			for value in best.position[0]:
				best = value + random.uniform(-1, 1)*(self.Maxiteration - self.NC)/self.Maxiteration
				
				random_move.append(best)
			
			self.GroupFish[index].position = copy.copy([tuple(random_move)])
			self.GroupFish[index].fitness = self.calcular_fitness(self.GroupFish[index].position, self.vector_len)
			self.NC += 1
			
			return 0
		
		random_x = fish.position
		
		for swaps in range(self.step):
			b = random.sample(range(self.vector_len), 2)
			random_x[b[1]], random_x[b[0]] = random_x[b[0]], random_x[b[1]]
		
		self.GroupFish[index].position = copy.copy(random_x)
		self.GroupFish[index].fitness = self.calcular_fitness(self.GroupFish[index].position, self.vector_len)
		self.NC += 1
		
		return 0
