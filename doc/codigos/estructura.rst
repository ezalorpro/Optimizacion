Estructura del modulo
=====================
Optimizar
---------

Es el núcleo del módulo, se encarga de gestionar a los algoritmos y a los problemas, es la clase
con la que el usuario interactuara para resolver los problemas, posee 3 funciones básicas:

* set_problem
* set_algorithm
* set_parameters

Los nombres de las funciones son un indicativo de su uso, set_problem se encargará de instanciar
un objeto de la clase del problema y retornar las funciones necesarias del mismo, set_algorithm, instanciara
un objeto de la clase del algoritmo y retornara el objeto para ser inicializado con sus respectivos
parámetros, estos parámetros se pueden leer de un archivo de texto usando la función set_parameters,
se presenta como ejemplo el formato para el archivo de configuración del AFSA::
	
	maxiteration=1000
	visual=4
	crowfactor=0.83
	n_fish=10
	step=1
	try_numbers=10

Adicionalmente se pretende agregar funciones para el post procesado de los resultados, actualmente
la única función de este estilo es procesar( ), la cual grafica el fitness vs métrica utilizando los valores
que retorna la función empezar( ) de cada algoritmo o aquellos que se guardan en una cola.
 
Algoritmos
----------

Los algoritmos actuales (AFSA, GA) fueron codificados con la idea principal de resolver
problemas combinatorios, no obstante, también son capaces de resolver problemas continuos,
en el caso del algoritmo genético todo dependerá de los operadores genéticos que se carguen
como parámetros, por otro lado, AFSA puede manejar problemas continuos sin ningún tipo de
condición, cabe aclarar que este último no está optimizado para problemas continuos.

Cada algoritmo está compuesto por una clase del mimo nombre, a su vez, cada clase requiere al menos
la definición de un constructor ( __ini__( )) y de una función llamada Empezar( ) quien iniciara
el proceso de optimización, en cada algoritmo también existe una segunda clase básica que hace
de objeto solución, sus únicos atributos son el fitness de la solución y la solución, se presenta
como ejemplo la clase secundaria de AFSA::

	
	class Fish:
		
		"""Clase para definir los objetos tipo pez(Fish)"""
		
		__slots__ = ('position', 'fitness')
		
		def __init__(self, p: List[Tuple[float, float]], f: float) -> None:
			self.position = p
			self.fitness = f

En orden de agregar más algoritmos al módulo de optimización se recomienda estudiar los ya implementados,
sobre todo la función empezar( ) y las funciones de los problemas. La función empezar( ) se puede
estructurar de manera básica del siguiente modo::
	
	def empezar(self, queue: None = None, show_results: bool = True) -> Tuple[List[float], object, int]:
		# variables necesarias
		:
		:
		ciclo for principal:
			ciclo  for secundario:
				# funciones del algoritmo
			# imprimir % de ejecucion
			# guardado de las mejores soluciones y de la evolucion del fitness
		:
		:
		# mostrar resultados
		
		if queue is not None:
			paquete = [fitness_evolution, copy.deepcopy(self.getbestsolution(best_solutions)), metrica]
			queue.put(paquete)
		
		return fitness_evolution, copy.deepcopy(self.getbestsolution(best_solutions)), metrica

Por otro lado, cuando se defina el constructor se debe tomar en cuenta que este deberá poder aceptar todos los parámetros
necesarios del algoritmo, adicionalmente deberá aceptar las funciones del problema y el problema base, en este constructor
se inicializarán las variables de la clase que deberían corresponder con los parámetros recibidos, todos los parámetros
recibidos estarán en formato string, por tanto, se deben transformar al tipo de variable que se requiera, es decir, int,
float, list, etc. Una estructura básica para el constructor es la siguiente::
	
	def __init__(self,
			parametros,
			problema: List[Tuple[float]] = None,
			funciones: List[Callable] = None) -> None:
		
		# Repetir para cada parametro
		# self.parametro = necessary_type(parametro)
		
		self.GroupObject_secundary_class = [] 
		
		self.crear_vector, self.calcular_fitness, self.imprimir_respuesta = funciones
		
		self.problema_base = problema
		
		for num in range(self.num_objects):
			vector = self.crear_vector(self.problema_base)
			fit = self.calcular_fitness(vector, len(vector))
			Object_ini = Object_secundary_class(copy.copy(vector), copy.copy(fit))
			self.GroupObject_secundary_class.append(Object_ini)
		
		self.vector_len = len(self.problema_base)

El primer segmento del código debería crear los atributos de la clase usando los parámetros recibidos,
se debe crear una lista que almacenara los objetos de la clase secundaria i.g., objetos de la clase Fish para AFSA,
se deben asignar las funciones del problema a atributos de la clase, con esto, se hará el llamado a las funciones
de manera general, lo siguiente es la creación de la población inicial, este paso es requerido por todos
los algoritmos (hasta donde conozco), por último, debemos crear el atributo self.vector_len quien nos indicara
el tamaño del problema a resolver.

Problemas
---------

Los problemas pueden ser continuos o combinatorios, cada problema posee dos clases,
una para definir al problema cuyo nombre es igual al del archivo, y una segunda clase
que complemente a la del problema, esta segunda se encarga de crear un método para obtener
las funciones de la clase principal de manera ordenada, esto con el fin de ser utilizado
por el modulo Optimizar::
	
	class OrderedClassMembers(type):
		@classmethod
		def __prepare__(self, name, bases):
			return collections.OrderedDict()
		
		def __new__(self, name, bases, classdict):
			classdict['__ordered__'] = [key for key in classdict.keys()
								if key not in ('__module__', '__qualname__')]
			return type.__new__(self, name, bases, classdict)

La clase principal del problema debe poseer sin excepción las siguientes funciones:

* __init__(self)
* ini_class_name(self, numero_posiciones, size_space: int, dimension: int, problema: str)
* crear_xxxx(problema_base: List[any]) -> List[any]
* calcular_fitness(solucion: List[any], numero_posiciones: int) -> float
* imprimir_respuesta(problema_base: List[any], mejor_posicion: object, cola: None = None) -> None

El orden de las funciones debe ser el mismo que acá se presenta, cualquiera otra función que se requiera
para el problema deberá ser definida después de las ya mencionadas. Los nombres de las funciones no son importantes
pero se recomienda utilizar la misma convención para mantener la consistencia entre los problemas.


__init__
^^^^^^^^

Se utiliza para crear atributos de la clase, por ahora este constructor no acepta ningún parámetro, pero
se tiene en mente expandir todos los constructores de todos los problemas para aceptar *args and **kwargs
con el fin de agregar flexibilidad a la definición de problemas.


ini_class_name
^^^^^^^^^^^^^^

Esta función creará el problema base a resolver, class_name se debe reemplazar con el nombre del problema deberá
retornar una lista conteniendo una representación del problema, normalmente esta lista contiene una serie tuples,
este es el caso incluso para problemas continuos, donde el retorno es una lista con un tuple de largo uno i.e., [(float,)].
Requiere de 4 parámetros, incluso si no se van a usar, en caso de no ser necesarios se pueden definir
usando _, __ , ___ y _____ para dejar claro que no son necesarios.


crear_xxxx
^^^^^^^^^^

Función crear la población inicial o un nuevo candidato, la idea es que devuelva una solución generada de manera random
del problema base, xxxx se debe sustituir con un nombre representativo del problema.


calcular_fitness
^^^^^^^^^^^^^^^^

Función para calcular el fitness correspondiente al problema, es posiblemente la función principal de la clase, se
recomienda optimizar lo mejor posible esta función, pues en muchos casos se requieren múltiples cálculos del fitness,
bien sea por requerimientos del algoritmo o de forma general para ir guardando las mejores soluciones, al igual que con
el constructor, se tiene la intensión de expandir sus parámetros con el uso de *args y **kwargs para mayor flexibilidad.


imprimir_respuesta
^^^^^^^^^^^^^^^^^^

Una función simple para mostrar los resultados obtenidos, en caso de generar algunas grafica con matplotlib, se recomienda
usar plt.draw, se invita al lector a revisar los problemas ya definidos para observar como condicionar a esta función para
que el problema pueda ser resuelto en múltiples ejecuciones tanto en secuencia como en paralelo con multiprocessing.
