Estructura
==========

Algoritmos
----------

Los algoritmos actuales (AFSA, GA) fueron codificados con la idea principal de resolver
problemas combinatorios, no obstante, tambien son capaces de resolver problemas continuos,
en el caso del algoritmo genetico todo dependera de los operadores geneticos que se cargen
como parametros, por otro lado AFSA puede manejar problemas continuos sin ningun tipo de
condicion, cabe aclarar que este ultimo no esta optimizado para problemas continuos.

Cada algoritmo esta compuesto por una clase del mimo nombre, a su vez, cada clase requiere al menos
la definicion de un constructor ( __ini__( )) y de una funcion llamada Empezar( ) quien iniciara
el proceso de optimizacion, en cada algoritmo tambien existe una segunda clase basica que hace
de objeto solucion, sus unicos atributos son el fitness de la solucion y la solucion, se presenta
como ejemplo la clase secundaria de AFSA::
	
	class Fish:
		
		"""Clase para definir los objetos tipo pez(Fish)"""
		
		__slots__ = ('position', 'fitness')
		
		def __init__(self, p: List[Tuple[float, float]], f: float) -> None:
			self.position = p
			self.fitness = f

En orden de agregar mas algoritmos al modulo de optimizacion se recomienda estudiar los ya implementados,
sobre todo la funcion empezar( ) y las funciones de los problemas. La funcion empezar( ) se puede
estructurar de manera basica del siguiente modo::
	
	def empezar(self, queue: None = None, show_results: bool = True) -> Tuple[List[float], object, int]:
		# variables necesarias
		:
		:
		ciclo for principal:
			ciclo  for secundario:
				# funciones del algoritmo
			# imprimir % de ejecucion
			# guardado de las mejores soluciones
		:
		:
		# mostrar resultados
		# retorno de resultados con return o con cola
	

Problemas
---------

Los problemas pueden ser continuos o combinatorios, cada problema posee dos clases,
una para definir al problema cuyo nombre es igual al del archivo, y una segunda clase
que complemente a la del problema, esta segunda se encarga de crear un metodo para obtener
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

La clase principal del problema debe poseer sin exepcion las siguientes funciones:

* __init__(self)
* ini_class_name(self, numero_posiciones, size_space: int, dimension: int, problema: str)
* crear_xxxx(problema_base: List[any]) -> List[any]
* calcular_fitness(solucion: List[any], numero_posiciones: int) -> float
* imprimir_respuesta(problema_base: List[any], mejor_posicion: object, cola: None = None) -> None

El orden de las funciones debe ser el mismo que aca se presenta, cualquier otro funcion que se requiera
para el problema debera ser definida despues de las ya mencionadas. Los nombres de las funciones no son importantes
pero se recomienda utilizar la misma convencion para mantener la consistencia entre los problemas.