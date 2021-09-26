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
			agregarDiccionario(linea[0],dicIncompatible, int (linea[1]), int (linea[2]) )   
		if(linea[0] =='n'):
			agregarDiccionario(linea[0],dicTiempos,int (linea[1]),int( linea[2]))
		linea = archivo.readline()

	return dicIncompatible,dicTiempos

#Funcion auxiliar que rellena los diccionarios, para el primer diccionario 
#dada una clave se crea una lista con las prendas incompatibles se destiñen
#Para el segundo diccionario dada la prenda(clave) le corresponde el tiempo de lavado (valor)

def agregarDiccionario(id,diccionario,clave,valor,):
	if(id=='e'):
		if( clave in diccionario): 
				diccionario.get(clave).append( valor )
		else:
			listaAux=[]
			listaAux.append( valor )
			diccionario[clave]=listaAux
	if(id=='n'):
		if( clave in diccionario): 		#el tiempo de cada prenda es solo un valor, por lo tanto no necesitamos una lista
				diccionario.get(clave).append(valor)
		else:
			diccionario[ clave ]= valor


#Dado un valor obtengo la clave del diccionario
def obtengoClaveDadoElValor(unDiccionario,listaIncom):
	for clave,valor in unDiccionario.items():
		if(listaIncom == valor):
			return int (clave)
	return 0


#Dado un diccionario de tiempos se devolvera la prenda que mas tarda en lavarse individualmente	
def prendaQueMasTardaEnLavar(dicTiempos):
	listaAux = []
	maxActual = 0
	prenda = 0;
	for tiempo in dicTiempos.values():
		if(tiempo>maxActual):
			maxActual=tiempo;
			prenda = obtengoClaveDadoElValor(dicTiempos,maxActual);

	valorMax = maxActual;
	dicTiempos.pop(prenda);
	return prenda


#Buscamos en los valores del dicIncompatible si la prenda no esta agregamos la clave a una lista.
def buscarPrendasCompatibles(dicIncompatible,prenda):
	listaCompatibles=[]
	for lista in dicIncompatible.values():
		if(prenda not in lista):
			listaCompatibles.append(obtengoClaveDadoElValor(dicIncompatible,lista) )
	return listaCompatibles


#Filtrar las prendas que solo con compatibles entre si en una lista de prestas ademas elimina
#las prendas que ya se uso anteriormente.
def filtrarCompatiblesEntreSi(listaComp,dicIncompatible,prendasUsadas):
	listaComptEntreSi = []
	for prenda in listaComp:
		if(prenda in prendasUsadas):
			listaComp.remove(prenda)
	for prenda in listaComp:
		if( prendaCompatibleEnListaPrendas(prenda,listaComptEntreSi,dicIncompatible)):
			listaComptEntreSi.append(prenda)
	return listaComptEntreSi

#Funcion auxiliar dado una prenda especifica vemos si es compatible para estar 
#en el mismo lavado que las prendas de la lista.
def prendaCompatibleEnListaPrendas(prendaEspecifica,listaPrendas,dicIncompatible):
	esCompatible = True
	#print(prendaespecifica)
	j = 0
	for prenda in listaPrendas:
		if(prendaEspecifica in dicIncompatible[prenda]):
			esCompatible = False
	return esCompatible

#Agrega la prenda usada a una lista de prendas adema retorna un booleano que nos
#indica si debemos agregar la lista de prendas o no.
def agregarPrendasUsadas(prendasUsadas,listaCompSI):
	noSeAgregaNada = False
	listaPrendasAgregar = []
	cantidadPrendasrepetidas=0
	if(len(listaCompSI)<=1):
		return True,listaPrendasAgregar

	for prenda in listaCompSI:
		if(prenda in prendasUsadas):
			cantidadPrendasrepetidas+=1
		else:
			listaPrendasAgregar.append(prenda)
			prendasUsadas.append(prenda)

	if(cantidadPrendasrepetidas==len(listaCompSI)):
		noSeAgregaNada = True
	return noSeAgregaNada,listaPrendasAgregar

#Devuelve un diccionaria cuya clave es el lavado y el valor es una 
#lista de prendas.
def asignarLavados(dicTiempos,dicIncompatible):
	lavado={}
	PrendasCompatible =[]
	prendasUsadas=[]
	j=1
	while(len(dicTiempos)>0):
		prenda =  prendaQueMasTardaEnLavar(dicTiempos)
		listaComp = buscarPrendasCompatibles(dicIncompatible,prenda)
		listaCompSI =filtrarCompatiblesEntreSi(listaComp,dicIncompatible,prendasUsadas)	 
		NoSeAgrega,listaPrendas = agregarPrendasUsadas(prendasUsadas,listaCompSI)
		if( NoSeAgrega == False):
			lavado[j]=listaPrendas;
			j+=1
	return lavado
#Escribe el archivo "respuestas.txt" el diccionario de lavados con el formato pedido.
def escribirArchivo(DicLavado):
	archivo = open("respuestas.txt","w")
	for lavado,listaPrendas in DicLavado.items():
		for prenda in listaPrendas:
			if(lavado<len(DicLavado)):
				archivo.write(str(prenda) + " " + str(lavado)+"\n")
			else:
				archivo.write(str(prenda) + " " + str(lavado))
	archivo.close()


def main():
	dicIncompatible,dicTiempos = leerArchivos()
	lavado = asignarLavados(dicTiempos,dicIncompatible);
	escribirArchivo(lavado)

main()




