#Lee los archivos y devuelve dos diccionarios uno para las prendas incompatibles
#Y otro diccionario para el tiempo que demora cada prenda 
class Prenda:

	def __init__(self,nroPrenda):
		self.nro = nroPrenda
		self.tiempoLavado = 0
		self.prendasIncomp = []
		self.EstaEnUnlavado = False

	def definirTiempo(self,unTiempo):
		self.tiempoLavado=unTiempo

	def addIncompatibilidad(self,prendaIncompatible):
		if prendaIncompatible not in self.prendasIncomp:
			self.prendasIncomp.append(prendaIncompatible)
	
	def imprimirPrenda(self):
		print(self.nro,end=':')
		print(len(self.prendasIncomp),end='\n')
		#print((self.prendasIncomp),end='')
		#print(self.tiempoLavado,end='\t \n')

	def getPrendasIncomp(self):
		return self.prendasIncomp

	def estaEnListaIncomp(self,prenda):
		return (prenda in self.prendasIncomp)
	
	def getNro(self):
		return self.nro
	
	#Se usa para definir como se compara en el sorted
	def __gt__(self,prenda):
		return ( len(self.prendasIncomp) > (len(prenda.prendasIncomp) ))

	def cantidadIncom(self):
		return len(self.prendasIncomp)

	def getTiempo(self):
		return self.tiempoLavado

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

	def imprimirLavado(self):
		print(self.nroLavado,end=':')
		for prenda in self.prendas:
			prenda.imprimirPrenda()

	def getListaPrendas(self):
		return self.prendas

	def getNroLavado(self):
		return self.nroLavado

def leerArchivos():
	archivo = open("ConsignaTP1.py","r")
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


def listaPrendasConMasIncomp(listaIncomp):
	listCantiIncomp = (sorted(listaIncomp,reverse=True))
	i = 0
	for prenda in listCantiIncomp:
		if(i<len(listCantiIncomp)-1):
			if(listCantiIncomp[i].cantidadIncom() == listCantiIncomp[i+1].cantidadIncom() ):
				if(listCantiIncomp[i].getTiempo() < listCantiIncomp[i+1].getTiempo() ):
					backup = listCantiIncomp[i]
					listCantiIncomp[i]=listCantiIncomp[i+1]
					listCantiIncomp[i+1]=backup
		i += 1
	return listCantiIncomp


def asignarLavados(listaIncomp,listCantiIncomp):
	nroLavado = 1
	prendasLavadas = []
	listaLavados = []
	seLavoLaPrenda = False

	while(len(prendasLavadas)<len(listaIncomp)):
		if( len(prendasLavadas)==0 ):#Realizamos el primer lavado para que tenga sentido recorrer la lista de lavados
			listaLavados.append(Lavado(nroLavado)) 
			prenda = listCantiIncomp[0]
			listaLavados[0].agregarPrendaAlLavado(prenda)
			prendasLavadas.append(prenda)
			nroLavado += 1
		else:
			for prenda in listCantiIncomp:
				for lavado in listaLavados:
					if(lavado.sePuedeAgregarPrenda(prenda) and prenda not in prendasLavadas):
						lavado.agregarPrendaAlLavado(prenda)
						prendasLavadas.append(prenda)
						seLavoLaPrenda = True
				if(not seLavoLaPrenda and prenda not in prendasLavadas ):
					listaLavados.append( Lavado(nroLavado))
					listaLavados[nroLavado-1].agregarPrendaAlLavado(prenda)
					prendasLavadas.append(prenda)
					nroLavado += 1
				seLavoLaPrenda = False
	return listaLavados

def escribirArchivo(listaLavados):
	archivo = open("respuestas2.txt","w")
	for lavado in listaLavados:
		for prenda in lavado.getListaPrendas():
				if(lavado.getNroLavado() < len(listaLavados) ):
					archivo.write(str(prenda.getNro()) + " " + str(lavado.getNroLavado() )+"\n")
				else:
					archivo.write(str(prenda.getNro()) + " " + str(lavado.getNroLavado() ))
	archivo.close()

def main():
	listaIncomp = leerArchivos()
	listaCantiIncomp =  listaPrendasConMasIncomp(listaIncomp)
	listaLavados = asignarLavados(listaIncomp,listaCantiIncomp)
	escribirArchivo(listaLavados)

	#print(len(listaLavados))
	#for lavado in listaLavados:
	#	lavado.imprimirLavado()

main()