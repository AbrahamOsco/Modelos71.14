#Enunciado
#Una lavandería tiene que lavar prendas, algunas pueden ir juntas y otras no (destiñen).
#El tiempo de cada lavado es el tiempo que lleva lavar la prenda más sucia de ese lavado.


#Lee los archivos y devuelve dos diccionarios uno para las prendas incompatibles
#Y otro diccionario para el tiempo que demora cada prenda 
def leerArchivos():
	archivo = open("ConsignaTP1.py","r"); #w,r,a(add, agregar)
	valores = []
	linea = archivo.readline()
	dicIncompatible={}
	dicTiempos = {}
	while(linea!=""):
		linea= (linea.strip()).split()
		if(linea[0] == 'e'):
			agregarDiccionario(linea[0],dicIncompatible,linea[1],linea[2])   
		if(linea[0] =='n'):
			agregarDiccionario(linea[0],dicTiempos,linea[1],linea[2])
		linea = archivo.readline()

	return dicIncompatible,dicTiempos

#Funcion auxiliar que rellena los diccionarios, para el primer diccionario 
#dada una clave se crea una lista con las prendas incompatibles se destiñen
#Para el segundo diccionario dada la prenda(clave) le corresponde el tiempo de lavado (valor)

def agregarDiccionario(id,diccionario,clave,valor,):
	if(id=='e'):
		if( clave in diccionario): 
				diccionario.get(clave).append(valor)
		else:
			listaAux=[]
			listaAux.append(valor)
			diccionario[clave]=listaAux
	if(id=='n'):
		if( clave in diccionario): 		#el tiempo de cada prenda es solo un valor, por lo tanto no necesitamos una lista
				diccionario.get(clave).append(valor)
		else:
			diccionario[int (clave)]= int (valor)

#Creamos para resolver el modelo un diccionario con las prendas que sean compatibles entren si. 
def obtenerLavadosCompatibles(dicIncompatible):
	dicLavadoCompat={}
	for i in range(1,len(dicIncompatible)+1):
		dicLavadoCompat[i]=lavadosCompatiblePorPrenda(i,dicIncompatible)
	return dicLavadoCompat

#Escribo la lista que tendra las prendas compatibles entre si() agrego los casos triviales por ej
#la prend 1 es compatible consigo mismo,de forma analogca con las demas.
def escribirListaFinal(dicCompatible):
	dicAux = dicCompatible
	for i in range(1,len(dicCompatible)+1):
		dicAux.get(i).insert(0,i)

	prenda = 1
	listaFinal = []
	listaAux = dicAux.values()

	for lista in listaAux:
		listaFinal.append(lista)
		listaFinal[prenda-1] = filtrarlista(listaFinal[prenda-1],dicAux)
		prenda+=1


	return listaFinal

#Funcion auxiliar que dada una lista recorre los elementos 
#devolviendo una lista nueva solo los elementos que son compatibles entre si.  
def filtrarlista(listaFinal,dicAux):
	listaNueva = []
	for prenda in listaFinal:
		if( len(listaNueva)==0 ):
			listaNueva.append(listaFinal[0])
		elif( len(listaNueva)>0 ):
			if( prendaCompatible(prenda,dicAux,listaNueva)):
				listaNueva.append(prenda)

	return listaNueva

#Funcion auxiliar que dada una prenda nos dice que si esta es compatible con las prendas
#anteriormente guardadas en la lista nueva.
def prendaCompatible(prenda,dicAux,listaNueva):
	esta = True
	for prendaAnterior in listaNueva:
		if(prenda not in list(dicAux.get(prendaAnterior)) ):
			esta = False
	return esta



#Dado un valor antes de agregar verifica si es compatible con las demas prendas
#En caso de que no sea no sea compatible retornara false
def esCompatbile(dicFinal,dicCompatible,lavado,unaPrenda):
	lista =  list (dicFinal.get(lavado))
	esPrendaCompatible = True
	for prenda in lista:
		if(unaPrenda not in list(dicCompatible.get(prenda))):
			esPrendaCompatible = False
	return esPrendaCompatible



#Dado un valor obtengo la clave del diccionario
def obtengoClaveDadoElValor(dicLavados,listaIncom):
	for clave,valor in dicLavados.items():
		if(listaIncom == valor):
			return clave
	return 0

#Funcion auxiliar para obtener los lavados compatibles por prenda
def lavadosCompatiblePorPrenda(prendaEspecifica,dicLavados):
	listaAux = []
	listaIncom= list(dicLavados.values())
	#Es necesario castear el numero que ingresamos como entero a string pues al buscar los elementos en la lista estos 
	#son de tipo string.
	prendaString = str (prendaEspecifica)
	
	#Observacion al castear la lista el resultado de (dicLavados.values()) obtenemos una lista de listas entonces recorremos
	#con un for la lista y buscamos, si no esta la prenda especifica entonces es compatible esa prenda con la prenda especifica.
	for lista in listaIncom:
		if( (prendaString not in lista)):
			clave = obtengoClaveDadoElValor(dicLavados,lista)
			if(clave!=prendaString):
				listaAux.append( int(clave))

	return listaAux			


def refinamientoLista(listaSinRefinar,dicTiempos):

	#En primer lugar hay que eliminar elementos repetidos:
	listasNueva = []
	listaSinRepetidas = []
	for lista in listaSinRefinar:
		listaAux = sorted(lista)
		listasNueva.append(listaAux)
	
	for lista in listasNueva:
		if (lista not in listaSinRepetidas):
			listaSinRepetidas.append(lista)
	print("Lista con refinada con todas las prendas compatibles entre si ")
	print(listaSinRepetidas)
	i = 0
	listaTiemposMax=[]			
	tamanioMax = len(listaSinRepetidas[0])
	for lista in listaSinRepetidas:
		listaTiemposMax.append(obtenerTiempo(dicTiempos,lista))
		if(len(lista)>tamanioMax):
			tamanioMax = len(lista)
	i+=1
	minTiempo = min(listaTiemposMax)
	maxTiempo = max(listaTiemposMax)
	diferencia = maxTiempo-minTiempo
	
	listasNuevaTiempo=[]

	for lista in listaSinRepetidas:
		if( obtenerTiempo(dicTiempos,lista) == minTiempo and len(lista)==tamanioMax):
			listasNuevaTiempo.append(lista)
	for lista in listaSinRepetidas:
		if(lista not in listasNuevaTiempo):
			listasNuevaTiempo.append(lista)

	print(listasNuevaTiempo)
	return listasNuevaTiempo


	
def obtenerTiempo(dicTiempos,lista):
	listaAux = []
	for prenda in lista:
		listaAux.append(dicTiempos.get(prenda))

	valorMax = max(listaAux)
	return valorMax

#Funcion donde se escribe el archivo
def escribirArchivo(listaTerminanda):


	lavados = 0
	archivo = open("respuesta.txt",'w')
	prendaUsada = []
	#print(listaTerminanda)
	
	for lista in listaTerminanda:
		lavados+=1
		intento = 0
		for prenda in lista:
			intento=intento+1
			if(prenda not in prendaUsada):
				if(lavados<15):
					archivo.write(str(prenda) + ' ' + str(lavados) +'\n')
					prendaUsada.append(prenda)
				elif(lavados>14):
					print("hola")
					archivo.write(str(prenda) + ' ' +str(lavados-1))
			
	archivo.close()	



dicIncompatible,dicTiempos = leerArchivos()
dicCompatible = obtenerLavadosCompatibles(dicIncompatible)
escribirLista = escribirListaFinal(dicCompatible)
listaRefinada = refinamientoLista(escribirLista,dicTiempos)
escribirArchivo(listaRefinada)