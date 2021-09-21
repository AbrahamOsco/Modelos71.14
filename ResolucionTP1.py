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
#La idea es juntar la mayor cantidad prendas en un solo lavado.
def obtenerLavadosCompatibles(dicIncompatible):
	dicLavadoCompat={}
	for i in range(1,len(dicIncompatible)+1):
		dicLavadoCompat[i]=lavadosCompatiblePorPrenda(i,dicIncompatible)

	#Veo ahora en una lista los tiempos maximos de cada lista compatible
	#listaTiempoMax= []
	#listaString = dicIncompatible.values()
	
	#for lista in listaString:
	#	intList = list(map(int,lista))

	#	maximo = max(intList)
	#	listaTiempoMax.append(maximo)

	#escribirDiccionarioFInal()
	return dicLavadoCompat

	#print(listaTiempoMax)


#escribirDiccionarioFInal()

def escribirListaFinal(dicCompatible):
	dicAux = dicCompatible
	for i in range(1,len(dicIncompatible)+1):
		dicAux.get(i).insert(0,i)
	print(dicAux)
	lavados = 1
	listaFinal = []
	listaAux = dicAux.values()

	for lista in listaAux:
		listaFinal.append(lista)
		listaFinal[lavados-1] = filtrarlista(listaFinal[lavados-1],dicAux)
		lavados+=1

	print(listaFinal)
	return listaFinal

#Elimina imcompatibilidades
def filtrarlista(listaFinal,dicAux):
	listaNueva = []
	for prenda in listaFinal:
		if( len(listaNueva)==0 ):
			listaNueva.append(listaFinal[0])
		elif( len(listaNueva)>0 ):
			if( prendaCompatible(prenda,dicAux,listaNueva)):
				listaNueva.append(prenda)

	return listaNueva


def prendaCompatible(prenda,dicAux,listaNueva):
	esta = True
	for prendaAnterior in listaNueva:
		if(prenda not in list(dicAux.get(prendaAnterior)) ):
			esta = False
	return esta



#Diccionario que dado un diccionario y un valor busca si el valor es compatible con el resto de valores
def esCompatbile(dicFinal,dicCompatible,lavado,unaPrenda):
	lista =  list (dicFinal.get(lavado))
	esPrendaCompatible = True
	for prenda in lista:
		if(unaPrenda not in list(dicCompatible.get(prenda))):
			esPrendaCompatible = False
	return esPrendaCompatible




def obtengoClaveDadoElValor(dicLavados,listaIncom):
	for clave,valor in dicLavados.items():
		if(listaIncom == valor):
			return clave
	return 0


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


def escribirArchivo(listaTerminanda,dicTiempos):
	print(dicTiempos)
	print("hola")
	print(listaTerminanda)
	lavados = 0
	termino = False
	archivo = open("respuesta.txt",'w')
	prendaUsada = []


	for lista in listaTerminanda:
		lavados+=1
		for prenda in lista:
			if(prenda not in prendaUsada):
				if(lavados<16):
					archivo.write(str(prenda) + ' ' + str(lavados) +'\n')
					prendaUsada.append(prenda)
				else:
					archivo.write(str(prenda) + ' ' +str(lavados))

	archivo.close()	



dicIncompatible,dicTiempos = leerArchivos()
dicCompatible = obtenerLavadosCompatibles(dicIncompatible)
escribirLista = escribirListaFinal(dicCompatible)
escribirArchivo(escribirLista,dicTiempos)