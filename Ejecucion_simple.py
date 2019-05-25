#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Uso basico del modulo Optimizar"""

from funciones_generales import General
import matplotlib.pyplot as plt
import Optimizar

optimizador = Optimizar.Optimizar()
Problema = optimizador.set_problem('TSP', vector_len=20, size_space=50, dimension=2)
instanciador, a_name = optimizador.set_algorithm(class_object='AFSA')
Parametros = optimizador.set_parameters('standar_AFSA.txt')

# Forma compacta
Resultado = instanciador(**Parametros, **Problema).empezar(show_results=True)
optimizador.procesar(*Resultado, a_name)

# Mas explicito
# Algoritmo = instanciador(**Parametros, **Problema)
# fitness_evolution, objeto, metrica = Algoritmo.empezar(show_results=True)
# optimizador.procesar(fitness_data=fitness_evolution, best_finded=objeto, metrica=metrica, algoritmo=a_name)

# Para correr varias veces
# best_solution = []
# for _ in range(5):   # Numero de ejecuciones secuenciales
# 	Resultado = instanciador(**Parametros, **Problema).empezar(show_results=True)
# 	optimizador.procesar(*Resultado, a_name)
# 	best_solution.append(Resultado[1])

# best_solution = General.getbestsolution(best_solution)
# print(f'\nMejor solucion: {best_solution.position}\ncon fitness de : {best_solution.fitness}')

plt.xlabel('iteraciones * poblacion')
plt.ylabel('fitness')
plt.title('fitness vs iteraciones * poblacion')
plt.legend()
plt.grid()
plt.savefig("imagenes\\fitnessgraph.png", bbox_inches='tight', pad_inches=0.1, format='png')
plt.show()
