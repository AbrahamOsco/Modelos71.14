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

#Funcion que elimina los repetidos y luego reordena las listas desde el conjunto de prendas de menor
#tiempo al de mayor tiempo para luego tomar las listas con elementos sin repetir y finalmente reordenando
#por tiempo nuevamente.
def refinamientoLista(listaSinRefinar,dicTiempos):

	#En primer lugar hay que eliminar elementos repetidos:
	listasNueva = []
	listaSinRepetidas = []
	listaAux = []
	obtenerListasSinRepetidas(listaSinRepetidas,listaSinRefinar)
	

	listasSegunTiempo = ordenarListasSegunTiempo(listaSinRepetidas,listaAux)


	numerosUsados = []
	contador = 0
	listaNuevaRe=[]

	for lista in listasSegunTiempo:
		contador = 0
		for prenda in lista:
			if(prenda not in numerosUsados ):
				numerosUsados.append(prenda)
				contador +=1
		if(contador==len(lista)):
			listaNuevaRe.append(lista)
		numerosUsados = resetearLista(numerosUsados,listaNuevaRe)


	listaFinal = ordenarListasSegunTiempo(listasSegunTiempo,listaNuevaRe)

	return listaFinal	

#Devuelve la lista con solo los numeros en la nueva lista, en la primera pasada devuelve la lista vacia
def resetearLista(numerosUsados,listaNuevaRe):
	numerosUsados= []
	if(len(listaNuevaRe)>0):
		for lista in listaNuevaRe:
			for prenda in lista:
				numerosUsados.append(prenda)
	return numerosUsados

#Recibe la lista de listas completa y la lista inicial para empezar a llenar en la nueva lista con
#los elementos que antes se encontraban ahi
def ordenarListasSegunTiempo(listaSinRepetidas,listaInicial):
	tamanioMax = 0
	listaTiemposMax=[]	
	tamanioMax = obtengoTamanioMaxLista(tamanioMax,listaSinRepetidas,listaTiemposMax)
	minTiempo = min(listaTiemposMax)
	maxtiempo = max(listaTiemposMax)
	listasNuevaTiempo= listaInicial


	for lista in listaSinRepetidas:
		if( obtenerTiempo(dicTiempos,lista) == minTiempo and len(lista)==tamanioMax and lista not in listasNuevaTiempo):
			listasNuevaTiempo.append(lista)

	for i in range(0,tamanioMax):
		for lista in listaSinRepetidas:
			if( obtenerTiempo(dicTiempos,lista) == minTiempo and  (lista not in listasNuevaTiempo) and (len(lista) ==tamanioMax-i)):
				listasNuevaTiempo.append(lista)
			elif( obtenerTiempo(dicTiempos,lista) == minTiempo+1  and (lista not in listasNuevaTiempo) and (len(lista) ==tamanioMax-i) ):
				listasNuevaTiempo.append(lista)
			elif( obtenerTiempo(dicTiempos,lista) == minTiempo+2  and (lista not in listasNuevaTiempo) and (len(lista) ==tamanioMax-i) ):
				listasNuevaTiempo.append(lista)
	return listasNuevaTiempo



#
def obtengoTamanioMaxLista(tamanioMax,listaSinRepetidas,listaTiemposMax):
	for lista in listaSinRepetidas:
		listaTiemposMax.append(obtenerTiempo(dicTiempos,lista))
		if(len(lista)>tamanioMax):
			tamanioMax = len(lista)
	return tamanioMax	

#Dada una lista vacia recibida por parametros y una lista con listas repetidas
#vamos primero a ordenar todas las listas y luego agregamos a la lista vacia las listas 
#que no se repiten
def obtenerListasSinRepetidas(listaSinRepetidas,listaSinRefinar):
	listasNueva = []
	for lista in listaSinRefinar:
		listaAux = sorted(lista)
		listasNueva.append(listaAux)
	
	for lista in listasNueva:
		if (lista not in listaSinRepetidas):
			listaSinRepetidas.append(lista)


#Dada una lista de prenda compatibles se obtendra el tiempo maximo que demoraria en lavarla 	
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
	print(listaTerminanda)
	entro = False
	prendaAgregada = 0
	for lista in listaTerminanda:
		lavados+=1
		if(prendaAgregada==0 and len(prendaUsada)>1 ):
			lavados -=1	
		prendaAgregada=0
		for prenda in lista:
			if(prenda not in prendaUsada):
				prendaAgregada+=1
				if(len(prendaUsada)<19):
					archivo.write(str(prenda) + ' ' + str(lavados) +'\n')
					prendaUsada.append(prenda)
				else:
					archivo.write(str(prenda) + ' ' + str(lavados))
	archivo.close()	


dicIncompatible,dicTiempos = leerArchivos()
dicCompatible = obtenerLavadosCompatibles(dicIncompatible)
escribirLista = escribirListaFinal(dicCompatible)
listaRefinada = refinamientoLista(escribirLista,dicTiempos)
escribirArchivo(listaRefinada)


