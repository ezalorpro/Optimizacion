#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Clase para utilizar como un modulo de optimizacion, los problemas se deben definir en la carpeta Problemas, cada
problema debera tener definida dos clases, una generica para poder extraer las funciones del problema en orden y una
clase que define al problema, el nombre del archivo debera ser igual al nombre de la clase que define al problema, esta
segunda condicion tambien es necesaria para el caso de los algoritmos, los cuales se deben definir en la carpeta
Algoritmos y mantener una estructura aproximada a los algoritmos ya definidos.

Algoritmos:

	- 'AFSA'
	- 'GA'
	
	*Nota 1: En la carpeta config_files se pueden modificar los parametros para cada algoritmo, en la misma carpeta
	se pueden encontrar ejemplos para cada algoritmo.
	
	*Nota 2: A la hora de cargar los parametros del GA, se deben escoger los operadores geneticos adecuadamente segun
	el tipo de problema, i.e., si el problema es combinatorio o si es continuo.
	
	Ejemplos:
	
		Para problemas combinatorios:
			ga_operators=('proportional_selection','ordered_crossover','swap_mutation','elitism')
		
		Para problemas continuos:
			ga_operators=('proportional_selection','heuristic_crossover','continuous_mutation','elitism')
	
Problemas:
	
	Combinatorios:
	
		- 'TSP' -> Travelling salesman problem
		- 'Nqns' -> N queens
	
		*Nota 3: vector_len debe ser > 1, pues indica el numero de ciudades o reinas.
	
	Continuos:
	
		- 'Ackley' -> Funcion Ackley
		- 'Rosenbrock' -> Funcion Rosenbrock
		- 'Rastrigin' -> Funcion Rastrigin
		
		*Nota 4: Para dimension=3, se graficá la superficie en 3D, se recomienda un size_space bajo no mayor de 30 para
		apreciar mejor la grafica.

"""

import importlib
import numpy as np
from typing import *
from matplotlib import pyplot as plt


class Optimizar:
	
	"""Clase para definir al 'modulo' Optimizar"""
	
	def __init__(self):
		self.conteo = 0
	
	@staticmethod
	def set_problem(elproblema: str, vector_len: int, size_space: int, dimension: int) -> Any:
		"""
		
		Funcion para establecer el problema base y las funciones asociadas a la clase de dicho problema.
		
		:param elproblema: Nombre de la clase que define al problema.
		:param vector_len: Tamaño del problema combinatorio ig. numero de ciudades para TSP.
		:param size_space: Espacio del problema, para ciertos problemas puede que no se use.
		:param dimension:  Dimension del problema, i.g., 2 para TSP
		:return: Diccionario con el problema base y las funciones de la clase del problema
		
		"""
		
		module_a = importlib.import_module('Problemas.' + elproblema)
		instance_a = getattr(module_a, elproblema)()
		class_functions = instance_a.__ordered__
		problema_base = getattr(instance_a, class_functions[2])(vector_len, size_space, dimension, elproblema)
		list_functions = [getattr(instance_a, name) for name in class_functions[3:6]]
		
		return dict(problema=problema_base, funciones=list_functions)
	
	@staticmethod
	def set_algorithm(class_object: str) -> Tuple[Callable, str]:
		"""
		
		Funcion para establecer el algoritmo a utilizar, esta funcion puede ser llamada varias veces para instanciar
		varios algoritmos.
		
		:param class_object: Nombre de la clase que define al algoritmo.
		:return: Un Callable del algoritmo escogido, i.g., AFSA.AFSA, ademas, retorna le nombre del algoritmo.
		
		"""
		
		module_a = importlib.import_module('Algoritmos.' + class_object)
		instance_a = getattr(module_a, class_object)
		
		return instance_a, class_object
	
	@staticmethod
	def set_parameters(archivo: str = None) -> Dict[str, float]:
		"""
		
		Funcion extraer los parametros de un archivo de texto.
			
			Formato:
				
				param1=value1
				param2=value2
				param3=value3
		
		:param archivo: Nombre del archivo que contiene los parametros del algoritmo
		:return: Diccionario con los parametros del algoritmo
		
		"""
		
		try:
			param = {}
			with open('config_files\\' + archivo) as f:
				for line in f:
					(key, val) = line.split('=')
					param[key] = val
			
			return param
		
		except FileNotFoundError:
			print('El archivo de parametros no existe...')
			quit()
	
	def procesar(self, fitness_data: List[float], best_finded: object, metrica: int, algoritmo: str) -> None:
		"""
		
		Funcion de uso opcional, se utiliza para graficar la evolucion del fitness, especialmente util para comparar
		varios algoritmos, ver ejemplo en Ejecucion_multiple.py
		
		:param fitness_data: Lista con la evolucion del fitness.
		:param best_finded: Objeto con la mejor solucion encontrada, actualmente sin uso.
		:param metrica: Unidad metrica para el eje de las X, actualmente iteraciones * poblacion.
		:param algoritmo: Nombre del algoritmo para la leyenda.
		:return: None
		
		"""
		
		self.conteo += 1
		vtiempo = np.linspace(0, metrica, len(fitness_data))
		plt.figure(30)
		plt.plot(vtiempo, fitness_data, linestyle='-', linewidth=1, label=algoritmo + str(self.conteo))
