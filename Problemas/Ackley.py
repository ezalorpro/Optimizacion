#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funcion Ackley"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from typing import *
import matplotlib.pyplot as plt
import numpy as np
import random
import collections

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


class Ackley(metaclass=OrderedClassMembers):
	
	"""Clase para definir el problema de la funcion Ackley."""
	
	def __init__(self):
		
		"""Para que los atributos de clase queden definidos en el __init__"""
		
		self.dimension = 0
		self.size_space = 0
		self.problema = 0
	
	def ini_funcionesmath(self, _, size_space: int, dimension: int, problema: str) -> List[int]:
		"""

		Para guardar las variables necesarias para el resto de funciones.
		
		:param _: None
		:param dimension: Numero de demensiones a resolver.
		:param size_space: Tamaño del espacio.
		:param problema: Nombre del problema.
		:return: Lista con len = 1 para establecer el problema como continuo.

		"""
		
		self.dimension = dimension - 1
		self.size_space = size_space
		self.problema = problema
		return [0]
	
	def crear_x(self, _) -> 'List[Tuple[float, float,...,dimension]]':
		"""

		Genera un valor real aleatorio en el rango +/- size_space/2 de dimension igual a dimension.

		:param _: None
		:return: valor real aleatorio.

		"""
		
		x = [tuple(random.sample(np.linspace(-self.size_space / 2, self.size_space / 2, 300).tolist(), self.dimension))]
		return x
	
	@staticmethod
	def calcular_fitness_ackley(x: 'List[Tuple[float, float,...,dimension]]', _) -> float:
		"""

		Genera el valor f(x) correspondiente a la funcion Ackley.

		:param x: Punto x  que contiene (x1, x2, x3,...,x_n) con n = self.dimension
		:param _: None
		:return: Ackley(x)

		"""
		
		x = np.array(*x)
		a = 20
		b = 0.2
		c = 2 * np.pi
		
		n = len(x)
		s1 = sum(x ** 2)
		s2 = sum(np.cos(c * x))
		fitness = -a * np.exp(-b * np.sqrt(s1 / n)) - np.exp(s2 / n) + a + np.exp(1)
		return fitness
	
	def imprimir_respuesta(self, _, mejor_posicion: object, cola: None = None) -> None:
		"""

		Imprime la mejor respuesta encontrada, ademas, en caso de dimension=3 (self.dimension = 2), grafica la
		superficie en 3D y el punto encontrado.

		:param _: None
		:param mejor_posicion: Mejor valor encontrado para la funcion Ackley.
		:param cola: Para determinar el mostrado de las figuras.
		:return: None

		"""
		
		print('x:', mejor_posicion.position)
		print('Mejor fitness: ', mejor_posicion.fitness)
		
		if self.dimension == 2:
			
			x = np.linspace(-self.size_space / 2, self.size_space / 2, 2000)
			y = np.linspace(-self.size_space / 2, self.size_space / 2, 2000)
			
			x, y = np.meshgrid(x, y)
			
			print('Funcion: Ackley')
			a = 20
			b = 0.2
			c = 2 * np.pi
			
			sum_sq_term = -a * np.exp(-b * np.sqrt(x * x + y * y) / 2)
			cos_term = -np.exp((np.cos(c * x) + np.cos(c * y)) / 2)
			z = a + np.exp(1) + sum_sq_term + cos_term
			
			xp = mejor_posicion.position[0][0]
			yp = mejor_posicion.position[0][1]
			
			sum_sq_term = -a * np.exp(-b * np.sqrt(xp * xp + yp * yp) / 2)
			cos_term = -np.exp((np.cos(c * xp) + np.cos(c * yp)) / 2)
			zp = a + np.exp(1) + sum_sq_term + cos_term
			
			fig = plt.figure(figsize=(10, 6))
			ax = fig.gca(projection='3d')
			
			ax.scatter(*mejor_posicion.position[0], zp, c='r', marker='o')
			
			surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
			fig.colorbar(surf, shrink=0.5, aspect=5)
			ax.view_init(elev=18, azim=38)
			ax.set_xlabel('x')
			ax.set_ylabel('y')
			ax.set_zlabel('z')
			plt.title(f"Funcion {self.problema}")
			plt.savefig("imagenes\\%s_output.png" % self.problema, bbox_inches='tight', pad_inches=0.1, format='png',
						dpi=400)
			
			if cola is None:
				plt.draw()
			else:
				plt.show()
