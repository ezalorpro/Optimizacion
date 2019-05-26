from multiprocessing import Queue, Process
from matplotlib import pyplot as plt
from Optimizar import Optimizar


if __name__ == '__main__':
	
	# Instanciacion de un Optimizador
	optimizador = Optimizar()
	
	# Definicion del problema
	Problema1 = optimizador.set_problem('TSP', vector_len=20, size_space=100, dimension=2)
	
	# Se establecen los algoritmos a usar
	instanciador1, a_name1 = optimizador.set_algorithm(class_object='AFSA')
	instanciador2, a_name2 = optimizador.set_algorithm(class_object='GA')
	
	# Primera opcion para cargar parametros al algoritmo: usando un archivo
	Parametros1 = optimizador.set_parameters('standar_AFSA.txt')
	Parametros2 = optimizador.set_parameters('standar_GA.txt')
	
	# Opcion alternativa para cargar parametros: creando el diccionario directamente
	Parametros3 = {
		'maxiteration': 1000,
		'visual': 4,
		'crowfactor': 0.83,
		'n_fish': 10,
		'step': 1,
		'try_numbers': 10,
	}
	
	# Colas
	q1 = Queue()
	q2 = Queue()
	
	# Se instancian ambos algoritmos enviando los parametros y el problema haciendo un unpack de los diccionarios
	ejecutar1 = instanciador1(**Parametros1, **Problema1)
	ejecutar2 = instanciador2(**Parametros2, **Problema1)
	
	# Se define la ejecucion de los procesos para ambos algoritmos enviando la cola para retornar informacion
	p1 = Process(target=ejecutar1.empezar, kwargs=dict(queue=q1, show_results=False, position=0))
	p2 = Process(target=ejecutar2.empezar, kwargs=dict(queue=q2, show_results=False, position=1))
	
	# Se inician los procesos
	p1.start()
	p2.start()
	
	# Cuando cada algoritmo termine, se obtienen los datos de la cola y se procesan
	optimizador.procesar(*q1.get(), a_name1)
	optimizador.procesar(*q2.get(), a_name2)
	
	p1.join()
	p2.join()
	
	# Opciones para la grafica creada con optimizador.procesar()
	plt.xlabel('iteraciones * poblacion')
	plt.ylabel('fitness')
	plt.title('fitness vs iteraciones * poblacion')
	plt.legend()
	plt.grid()
	plt.savefig("imagenes\\fitnessgraph.png", bbox_inches='tight', pad_inches=0.1, format='png')
	plt.show()
