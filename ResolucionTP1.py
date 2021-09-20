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
	print(dicIncompatible)
	print(dicTiempos)

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
			diccionario[clave]=valor

#Creamos para resolver el modelo un diccionario con las prendas que sean compatibles entren si. 
#La idea es juntar la mayor cantidad prendas en un solo lavado. Asi se dismuye el tiempo 
def resolverModelo():
	.	



dicIncompatible,dicTiempos = leerArchivos()