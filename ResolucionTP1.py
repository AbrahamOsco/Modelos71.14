#Lee los archivos y devuelve dos diccionarios uno para las prendas incompatibles
#Y otro diccionario para el tiempo que demora cada prenda 
import numpy as np
import pulp

def leerArchivos():
	archivo = open("ConsignaTP1.py","r")
	valores = []
	linea = archivo.readline()
	dicIncompatible={}
	dicTiempos = {}
	
	while(linea!=""):
		linea= (linea.strip()).split()
		if(linea[0] == 'p'):
			inicializarDiccionarios(linea,dicIncompatible,dicTiempos)
		elif(linea[0] == 'e'):
			agregarDiccionario(linea[0],dicIncompatible, int (linea[1]), int (linea[2]) )   
		elif(linea[0] =='n'):
			agregarDiccionario(linea[0],dicTiempos,int (linea[1]),int( linea[2]))
		linea = archivo.readline()

	return dicIncompatible,dicTiempos

def agregarDiccionario(id,diccionario,clave,valor,):
	if(id=='e'):
		diccionario.get(clave).append(valor)
	if(id=='n'):
		diccionario[clave] = valor

#Funcion auxiliar para inicializar los diccionarios.
def inicializarDiccionarios(linea,dicIncompatible,dicTiempos):
	cantidadPrendas = int (linea[2]) #Esto si . 
	for i in range(1,cantidadPrendas+1):
		dicIncompatible[i]=[]
		dicTiempos[i]=0

#Dado un valor obtengo la clave del diccionario
def obtengoClaveDadoElValor(unDiccionario,listaIncom):
	for clave,valor in unDiccionario.items():
		if(listaIncom == valor):
			return int (clave) 
	return 0

def prendaQueMasTardaEnLavar(dicTiempos): 
	listaAux = []
	max_actual = max(dicTiempos.values() )
	prenda = obtengoClaveDadoElValor(dicTiempos,max_actual)
	dicTiempos.pop(prenda);
	return prenda 

def buscarPrendasCompatibles(dicIncompatible,prenda):
	listaCompatibles=[]
	for prendaI in dicIncompatible.keys():
		if(prendaI not in dicIncompatible[prenda] and prenda not in dicIncompatible[prendaI] ):
			listaCompatibles.append(prendaI)
	return listaCompatibles

def filtrarCompatiblesEntreSi(listaComp,dicIncompatible):
	listaComptEntreSi = []
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

def escribirArchivo(DicLavado):
	archivo = open("respuestas2.txt","w")
	for lavado,listaPrendas in DicLavado.items():
		for prenda in listaPrendas:
			if(lavado<len(DicLavado)):
				archivo.write(str(prenda) + " " + str(lavado)+"\n")
			else:
				archivo.write(str(prenda) + " " + str(lavado))
	archivo.close()

def obtenerDicCompatibles(dicIncompatible):
	dicCompatibles= {}
	listaSinInncompEntreSi = []
	for prenda in dicIncompatible.keys():
		listaSinInncompEntreSi = buscarPrendasCompatibles(dicIncompatible,prenda)
		dicCompatibles[prenda] = filtrarCompatiblesEntreSi(listaSinInncompEntreSi,dicIncompatible)
	return dicCompatibles

def añadirRestricciones(dicCompatibles,prob,visitaPrendaVAR,ListPrendasVAR,dicTiempos):
	sumaAux = 0
	aux = 1
	for ListasPrendas in dicCompatibles.values():
		for prendas in ListasPrendas:
			sumaAux += ListPrendasVAR[prendas-1]
		prob +=sumaAux == visitaPrendaVAR[aux-1]
		#prenda = prendaQueMasTardaEnLavar(dicTiempos)
		#prob += visitaPrendaVAR[prenda-1] == 1  #Asigno 1 a la variable de la prenda que mas tarda en lavar				
		sumaAux =0
		aux +=1

def asignarLavado(dicCompatibles,prendasSeleccionadas):
	dicNuevo = {}
	lavado = 1
	listaLavado = []
	prendasLavadas = []
	for prendaSelec in prendasSeleccionadas:
		for prenda in dicCompatibles[prendaSelec]:
			if(prenda not in prendasLavadas):
				prendasLavadas.append(prenda)
				listaLavado.append(prenda)
		if(len(listaLavado)>0):
			dicNuevo[lavado]=listaLavado
			listaLavado=[]
			lavado+=1

	return dicNuevo,len(prendasLavadas)		



def main():
	dicIncompatible,dicTiempos = leerArchivos()
	dic = obtenerDicCompatibles(dicIncompatible)
	VisitoListaPrendas = []
	tope = len(dic)
	PrendasVisitadas = []
	#Se uso pulp para intentar resolver el problema. 
	prob = pulp.LpProblem("prendasl",pulp.LpMaximize) #Queremos maximizar
	
	for i in range(0,tope):
		VisitoListaPrendas.append('y'+str(i+1))	
	#y_i : Se visito la lista de la prenda compatibles de la prenda i 
	#y: es una lista que cotiene las 385 posibles listas para visitar
	y = [ pulp.LpVariable(i,lowBound=0,cat='Binary') for i in VisitoListaPrendas ] 
	


	for i in range(0,tope):
		PrendasVisitadas.append('v'+str(i+1))
	#v_i: Se visito (lavo) la prenda i 
	v = [ pulp.LpVariable(i,lowBound=0,cat='Binary') for i in PrendasVisitadas ]

	z = 0 #Funcion Objetivo
	for i in range(0,385):
		z += v[i]*1
	prob += z 
	añadirRestricciones(dic,prob,v,y,dicTiempos)

	status = prob.solve() #Se resuelve el modelo 
	lista = []
	#Lo siguiente es para ver que variables toman valor 1 
	for i in prob.variables():
		if (i.varValue==1.0):
			lista.append(i)
		#print(i,i.varValue) #Vemos que variables toman valor 1

	listasVisitadas = list (lista)
	listaVisitadasPrendas =[]
	#Nos interesa las listas que visitamos
	for elemento in listasVisitadas:
		nuevo = (str (elemento))
		if ('y' in nuevo):
			agregar = nuevo.replace('y','')
			listaVisitadasPrendas.append(int (agregar))

	dicLavados,cantPrendasLavadas = asignarLavado(dic,listaVisitadasPrendas)
	print(dicLavados,cantPrendasLavadas)

main()