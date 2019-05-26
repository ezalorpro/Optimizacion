#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Algoritmo Genetico. Se puede utilizar por medio de la clase Optimizar, para mas detalles estudiar el ejemplo
Ejecucion_simple.py o Ejecucion_multiple.py.
	
	*Nota 1: A la hora de cargar los parametros del GA, se deben escoger los operadores geneticos adecuadamente segun
	el tipo de problema, i.e., si el problema es combinatorio o si es continuo.
	
	Ejemplos:
	
		Para problemas combinatorios:
			ga_operators=('proportional_selection','ordered_crossover','swap_mutation','elitism')
		
		Para problemas continuos:
			ga_operators=('proportional_selection','heuristic_crossover','continuous_mutation','elitism')

"""

import ast
import copy
import random
from tqdm import tqdm
from typing import *
from funciones_generales import General


class Chromosome:
	
	"""Clase para definir los objetos tipo cromosoma(Chromosome)"""
	
	__slots__ = ('position', 'fitness')
	
	def __init__(self, p: List[Tuple[int, int]], f: float) -> None:
		self.position = p
		self.fitness = f


class GA(General):
	
	"""Clase base del Algoritmo Genetico, incluye los operadores geneticos necesarios para el algoritmo."""
	
	def __init__(self,
				 maxgenerations: str = 1000,
				 poppulation_size: str = 100,
				 mutation_rate: str = 0.01,
				 selection_rate: str = 0.5,
				 ga_operators: str = ('proportional_selection', 'ordered_crossover', 'swap_mutation', 'elitism'),
				 problema: List[Tuple[int, int]] = None,
				 funciones: List[Callable] = None) -> None:
		"""
		
		:param maxgenerations: Cantidad maxima de generaciones
		:param poppulation_size: Numero de candidatos, i.e., numero de cromosomas
		:param mutation_rate: Porcentaje relativo de mutaciones a realizar por cada posicion en el genoma del cromosoma.
		:param selection_rate: Porcentaje relativo de padres a escoger del total de candidatos.
		:param ga_operators: Lista de operadores geneticos.
		:param problema: Problema base a resolver.
		:param funciones: lista de funciones correspondiente al problema a resolver.
		:return: None
		
		"""
		
		self.problema_base = problema
		self.vector_len = len(self.problema_base)
		self.Maxiteration = int(maxgenerations)
		self.mutation_rate = float(mutation_rate)
		self.selection_rate = float(selection_rate)
		self.population_size = int(poppulation_size)
		self.GA_operators = [getattr(self, name) for name in ast.literal_eval(ga_operators)]
		self.GroupChromosomes = []
		self.crear_vector, self.calcular_fitness, self.imprimir_respuesta = funciones
		self.NC = 0
		
		for num in range(self.population_size):
			vector = self.crear_vector(self.problema_base)
			fit = self.calcular_fitness(vector, len(vector))
			fish_ini = Chromosome(copy.copy(vector), copy.copy(fit))
			self.GroupChromosomes.append(fish_ini)
		
	def empezar(self, queue: None = None, show_results: bool = True, position: int = 0) -> Tuple[List[float], Chromosome, int]:
		"""
		
		Empieza el proceso de optimizacion, hace el llamado para guardar el mejor cromosoma despues de cada iteracion y
		llama a la funcion de imprimir respuesta.
		
		:param queue: Variable de multiproceso (cola), se utiliza para devolver informacion al thread principal.
		:param show_results: Bandera para escoger el llamado a imprimir_respuesta().
		:returns: Lista con la evolucion del fitness, objeto Chromosome con la mejor solucion encontrada, numero de
		operaciones realizadas (iteraciones * population_size).
		
		"""
		
		best_chromosome = []
		fitness_evolution = []
		interval = self.Maxiteration * 0.2 / 100
		count = 0
		
		for iteration in tqdm(range(self.Maxiteration), position=position):
			couples = []
			childs = []
			parents = []
			max_value = sum(chromosome.fitness for chromosome in self.GroupChromosomes)

			# Seleccion de Padres
			for _ in range(int(self.population_size*self.selection_rate)):
				
				couples.append(self.GA_operators[0](self.GroupChromosomes, max_value))
				couples.append(self.GA_operators[0](self.GroupChromosomes, max_value))
				parents.append(couples)
				couples = []
			
			# Crossover y mutation
			for couples in parents:
				child1, child2 = self.GA_operators[1](couples[0], couples[1])
				child1 = self.GA_operators[2](child1, self.mutation_rate)
				child2 = self.GA_operators[2](child2, self.mutation_rate)
				
				childs.append(copy.copy(child1))
				childs.append(copy.copy(child2))
			
			# reduccion de la poblacion por elitismo	
			self.GroupChromosomes = self.GA_operators[3](self.GroupChromosomes + childs)
			
			# self.GroupChromosomes = copy.deepcopy(new_generation)
			best_chromosome.append(copy.deepcopy(self.getbestsolution(self.GroupChromosomes)))
			
			if count > interval:
				count = 0
				fitness_evolution.append(self.getbestsolution(best_chromosome).fitness)
			
			count += 1
			self.NC += 1
		
		if show_results:
			self.imprimir_respuesta(self.problema_base, self.getbestsolution(best_chromosome), queue)
		
		operaciones = self.Maxiteration * self.population_size
		if queue is not None:
			paquete = [fitness_evolution, copy.deepcopy(self.getbestsolution(best_chromosome)), operaciones]
			queue.put(paquete)
		
		return fitness_evolution, copy.deepcopy(self.getbestsolution(best_chromosome)), operaciones
	
	@staticmethod
	def proportional_selection(chromosomes: List[Chromosome], max_value: float) -> Chromosome:
		"""
		
		Funcion para seleccionar los padres, los padres con un mejor fitness tienen una probabilidad mayor de ser
		escogidos.
		
		:param chromosomes: Lista de cromosomas correspondiente a la generacion actual.
		:param max_value: sumatoria total de fitness de la generacion actual.
		:return: Padre seleccionado.
		
		"""
		
		pick = random.uniform(0, max_value)
		current = 0
		for chromosome in chromosomes:
			current += chromosome.fitness
			if current >= pick:
				return chromosome
		
	def ordered_crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
		"""
		
		Funcion para generar los hijos, quienes seran los candidatos a formar la siguiente generacion. El proceso consta
		de tomar dos puntos de cortes en el padre y la madre, la informacion rodeada de dichos cortes se preserva para
		para los hijos, y el resto se rellena de manera secuencial con la data faltante, si el corte es tomado del padre,
		el resto de la data se rellena con informacion de la madre, y viceversa.
			
			Ejemplo:						cuts	=	[2, 5)
											padre	1 2 |3 4 5| 6 7
											madre	5 6 |7 4 3| 2 1
											-----------------------
													x x |3 4 5| x x
													x x |7 4 3| x x
											-----------------------
											child1	6 7 |3 4 5| 2 1
											child2	1 2 |7 4 3| 5 6
											
		
		:param parent1: Cromosoma correspondiente al padre.
		:param parent2: Cromosoma correspondiente a la madre.
		:return: Cromosomas correspondientes a los hijos generados.
		
		"""
		
		cuts = random.sample(range(len(parent1.position)), 2)
		first_cut = min(*cuts)
		second_cut = max(*cuts)
		
		child1_part = [item for item in parent1.position[first_cut: second_cut]]
		child1 = [item for item in parent2.position if item not in child1_part]
		child1[first_cut:first_cut] = child1_part
		
		child2_part = [item for item in parent2.position[first_cut: second_cut]]
		child2 = [item for item in parent1.position if item not in child2_part]
		child2[first_cut:first_cut] = child2_part
		
		parent1.position = child1
		parent2.position = child2
		parent1.fitness = self.calcular_fitness(parent1.position, self.vector_len)
		parent2.fitness = self.calcular_fitness(parent2.position, self.vector_len)
		
		return parent1, parent2
	
	def swap_mutation(self, individuo: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
		"""
		
		Funcion para realizar mutacion por medio de un swap, dicho swap se ejecuta para cada posicion del genoma, si
		se cumple la probabilidad de que suceda dada por el mutation_rate.
		
		:param individuo: Cromosoma que posiblemente mutará.
		:param mutation_rate: Porcentaje relativo de mutaciones a realizar por cada posicion en el genoma del cromosoma.
		:return: Cromosoma mutado.
		
		"""
		
		for gen_index in range(len(individuo.position)):
			if random.random() < mutation_rate:
				swap_index = random.sample(range(len(individuo.position)), 1)
				individuo.position[swap_index[0]], individuo.position[gen_index] = \
					individuo.position[gen_index], individuo.position[swap_index[0]]
		
				individuo.fitness = self.calcular_fitness(individuo.position, self.vector_len)
		
		return individuo
	
	def elitism(self, old_generation: List[Chromosome]) -> List[Chromosome]:
		"""
		
		Funcion para reducir la poblacion basado en el principio de elitismo, donde solo los cromosomas con mejor fitness
		sobreviven. EL tamaño de la poblacion luego del crossover se reduce a al tamaño de la poblacion antes del crossover.
		
		:param old_generation: Generation anterior + hijos generados del crossover
		:return: Nueva generacion de un tamaño igual a population_size
		
		"""
		
		new_generation = self.getbestsolution(old_generation, self.population_size)
		return new_generation

	def heuristic_crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
		"""
		
		Funcion para calcular el crossover en el caso de problemas continuos. Se selecciona una posicion random dentro
		de la dimension del problema, luego, se modifica dicha posicion para el padre y para la madre tomando informacion
		de ambos y utilizando un factor beta que tomara valores entre 0 y 1.
			
			Formula:
												Padre					Madre
										P(N1, N2, N3,..., Nn) y M(N1, N2, N3,..., Nn)
							
											Ni_pnew = Ni_p - beta*(Ni_p - Ni_m)
											Ni_mnew = Ni_m + beta*(Ni_p - Ni_m)
											
							Con Ni como la posicion a modificar con i € Naturales y 0 <= i < dimension
							
		
		:param parent1: Cromosoma correspondiente al padre.
		:param parent2: Cromosoma correspondiente a la madre.
		:return: Cromosomas correspondientes a los hijos generados.
		
		"""
		
		if len(parent1.position[0]) != 1:
			i = random.sample(range(len(parent1.position[0])), 2)
		else:
			i = [0, 0]
		
		beta = random.random()
		
		new_value1 = parent1.position[0][i[0]] - beta*(parent1.position[0][i[0]] - parent2.position[0][i[0]])
		new_value2 = parent2.position[0][i[1]] + beta*(parent1.position[0][i[1]] - parent2.position[0][i[1]])
		
		parent1.position[0] = list(parent1.position[0])
		parent1.position[0][i[0]] = new_value1
		parent1.position[0] = tuple(parent1.position[0])
		
		parent2.position[0] = list(parent2.position[0])
		parent2.position[0][i[1]] = new_value2
		parent2.position[0] = tuple(parent2.position[0])
		
		parent1.fitness = self.calcular_fitness(parent1.position, self.vector_len)
		parent2.fitness = self.calcular_fitness(parent2.position, self.vector_len)
		
		return parent1, parent2
	
	def continuous_mutation(self, individuo: Chromosome, mutation_rate: float = 0.01) -> Chromosome:
		"""
		
		Funcion para realizar mutacion agregando un valor random entre -1 y 1 si se cumple la probabilidad de que suceda
		dicha mutacion dado por el mutation_rate. Esta mutacion solo puede suceder a una posicion del genoma.
		
		:param individuo: Cromosoma que posiblemente mutará.
		:param mutation_rate: Porcentaje relativo de mutaciones a realizar para una posicion en el genoma del cromosoma.
		:return: Cromosoma mutado.
		
		"""
		
		if random.random() < mutation_rate:
			mutation_index = random.sample(range(len(individuo.position[0])), 1)[0]
			individuo.position[0] = list(individuo.position[0])
			individuo.position[0][mutation_index] = individuo.position[0][mutation_index] + random.uniform(-1, 1)
			
			individuo.position[0] = tuple(individuo.position[0])
			individuo.fitness = self.calcular_fitness(individuo.position, self.vector_len)
		return individuo
