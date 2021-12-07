#Lee los archivos y devuelve dos diccionarios uno para las prendas incompatibles
#Y otro diccionario para el tiempo que demora cada prenda 
import time
class Prenda:

	def __init__(self,nroPrenda):
		self.nro = nroPrenda
		self.tiempoLavado = 0
		self.prendasIncomp = []
		self.estaLavada = False

	def definirTiempo(self,unTiempo):
		self.tiempoLavado=unTiempo

	def addIncompatibilidad(self,prendaIncompatible):
		if prendaIncompatible not in self.prendasIncomp:
			self.prendasIncomp.append(prendaIncompatible)
		
	def getPrendasIncomp(self):
		return self.prendasIncomp

	def getNro(self):
		return self.nro

	def cantidadIncom(self):
		return len(self.prendasIncomp)

	def getTiempo(self):
		return self.tiempoLavado
	
	def lavarPrenda(self):
		self.estaLavada = True

	def prendaLavada(self):
		return self.estaLavada

class Lavado:

	def __init__(self,nroDeLavado):
		self.nroLavado=nroDeLavado
		self.prendas = []

	def agregarPrendaAlLavado(self,unaPrenda):
		if(unaPrenda not in (self.prendas) and self.sePuedeAgregarPrenda(unaPrenda) ):
			self.prendas.append(unaPrenda)

	def sePuedeAgregarPrenda(self,unaPrenda):
		for prenda in self.prendas:
			if(unaPrenda.getNro() in prenda.getPrendasIncomp()):
				return False
		return True

	def getListaPrendas(self):
		return self.prendas

	def getNroLavado(self):
		return self.nroLavado

	def estaNroPrendaEnLavado(self,nro):
		for prenda in self.prendas:
			if(prenda.getNro() == nro):
				return True
		return False

def leerArchivos():
	archivo = open("tercer_problema.txt","r")
	linea = archivo.readline()
	listaIncomp = []	
	while(linea!=""):
		linea= (linea.strip()).split()
		if(linea[0] == 'p'):
			inicializarLista(linea,listaIncomp)
		if(linea[0] == 'e'):						
			agregarIncomp(listaIncomp,int (linea[1]), int (linea[2]) )   
		elif(linea[0] =='n'):
			listaIncomp[int (linea[1])-1].definirTiempo( int (linea[2])  )
		linea = archivo.readline()

	return listaIncomp

def agregarIncomp(listaIncomp,valor1,valor2,):
	#Agregamos en ambos sentidos la incompatibilidad de la prenda
	listaIncomp[valor1-1].addIncompatibilidad(valor2)
	listaIncomp[valor2-1].addIncompatibilidad(valor1)

def inicializarLista(linea,listaIncomp):
	cantidadPrendas = int (linea[2]) #Esto si . 
	for i in range(1,cantidadPrendas+1):
		listaIncomp.append( Prenda(i))

#Obtenemos una lista con las prendas con mayor cantidad de incompatibilidades
#Es decir seria una lista con las prendas (vertices) de mayor grado.
#Grado de un vertice definición: Es la cantidad de aristas que inciden en el . 
#Paso 1: Ordenar los vértices en orden decreciente de grados.
def listaPrendasConMasIncomp(listaIncomp):
	listaOrden = sorted(listaIncomp,key=lambda p:p.cantidadIncom() ,reverse=True)
	return listaOrden

#Dado una prendaEspecifica (vertice) vamos a obtener la cantidad de colores(lavados) usados
#en los vecinos de esta prendaEspecifica (vertice).Esto es la definicion de grado de color de un vertice.
def obtenerGradoColor(prendaEsp,lavados):
	nroLavadosVecinos = []
	for prenda in prendaEsp.getPrendasIncomp():
		for lavado in lavados:
			if(lavado.getNroLavado() not in nroLavadosVecinos and lavado.estaNroPrendaEnLavado(prenda) ):
				nroLavadosVecinos.append(lavado.getNroLavado())
				
	return len(nroLavadosVecinos)

def obtenerGradoColorMax(listaPrendas,lavados):
	gradoColorMax = 0
	contador = 1
	prendasSiguientes = []  #el grado de color se puede repetir, tomaremos la prenda que mas tarda en lavar.
	for prenda in listaPrendas:
		gradoActual = obtenerGradoColor(prenda,lavados)
		if(gradoActual>gradoColorMax):
			gradoColorMax = gradoActual
			prendasSiguientes.clear() #Limpio toda la lista porque encontre un grado de color mucho mas grande.
			prendasSiguientes.append(prenda)
		elif(gradoActual == gradoColorMax):   #Paso 3.1: Si hay varios, elegimos el de grado máximo, asi dice el algoritmo nosotros solo lo 
			prendasSiguientes.append(prenda)  #agruparemos en una lista para luego ordenarlos por  el que tenga mayor tiempo .		

	prendasOrd = sorted(prendasSiguientes,key=lambda p:p.getTiempo(), reverse=True )
	return prendasOrd[0]

def asignarLavados(listCantiIncomp):
	nroLavado = 1
	lavados = []
	#Paso 2: Coloreamos un vértice de grado máximo con el color(lavado) 1.
	prendaIni = listCantiIncomp[0]
	lavados.append(Lavado(nroLavado))
	lavados[0].agregarPrendaAlLavado(prendaIni)
	prendaIni.lavarPrenda()
	nroLavado +=1
	listCantiIncomp.pop(0)

	while( len(listCantiIncomp) > 0 ):
		#Paso 3.0: Seleccionamos un vértice, aún sin colorear, con grado de color máximo. 	
		prendaSgt = obtenerGradoColorMax(listCantiIncomp,lavados)
		for lavado in lavados: #Paso 4: Colorear(asignar Lavado) el vértice (prenda) seleccionado en el paso 3 con el menor color(lavado) posible.
			if(lavado.sePuedeAgregarPrenda(prendaSgt) and  not prendaSgt.prendaLavada() ):
				lavado.agregarPrendaAlLavado(prendaSgt)
				prendaSgt.lavarPrenda()
				listCantiIncomp.remove(prendaSgt)
		if( not prendaSgt.prendaLavada() ):
			lavadoActual = Lavado(nroLavado)
			lavadoActual.agregarPrendaAlLavado(prendaSgt)
			lavados.append(lavadoActual)
			prendaSgt.lavarPrenda()
			nroLavado +=1
			listCantiIncomp.remove(prendaSgt)
		print(len(listCantiIncomp))
		#Paso 5: Si todos los vértices se han coloreado, FIN. En caso contrario, volver al paso 3.	
	return lavados

def escribirArchivo(listaLavados):
	archivo = open("respuestasTP3Inicial.txt","w")
	for lavado in listaLavados:
		for prenda in lavado.getListaPrendas():
			archivo.write(str(prenda.getNro()) + " " + str(lavado.getNroLavado() )+"\n")
	archivo.close()

def main():
	inicio = time.time()
	listaIncomp = leerArchivos()
	listaCantiIncomp =  listaPrendasConMasIncomp(listaIncomp)
	listaLavados = asignarLavados(listaCantiIncomp)
	escribirArchivo(listaLavados)
	fin = time.time()
	print(fin-inicio)
main()

