#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
#Imports TP3
import excel

#Variables globales
#Cantidad de corridas
cantidad_corridas = 200
#Cantidad de cromosomas de la población
tamano_poblacion = 50
#Cromosomas: permutaciones de 24 números naturales del 1 al 24 donde cada gen es una ciudad.
longitud_cromosomas = 24
#Probabilidad de crossover
pc = 0.75 
#Probabilidad de mutación
pm = 0.05 
#Elitismo: cantidad de cromosomas
r=4

#Crear población inicial
def crear_poblacion_inicial():
    poblacion_inicial = []
    for _ in range(tamano_poblacion):
        #random.sample(a,b) crea lista de números aleatorios
        #a: rango de los números, b: cantidad de números
        cromosoma = random.sample(range(1,longitud_cromosomas+1), longitud_cromosomas)
        poblacion_inicial.append(cromosoma)
    return poblacion_inicial

#Función objetivo: suma de las distancias
#x: cromosoma
def funcion_objetivo(x):
    valor_fo = 0
    for i in range(1,len(x)-1):
        valor_fo += excel.distancia_entre_ciudades(x[i],x[i+1])
    #Agrego distancia de la última ciudad a la ciudad origen
    valor_fo += excel.distancia_entre_ciudades(x[-1],x[0])
    return valor_fo

#Función fitness
#Argumentos: funcobj = valor de la función objetivo del cromosoma, poblacion = lista de cromosomas
def funcion_fitness(funcobj,poblacion):
    #Acumulado funciones objetivo
    acum_fo = 0
    for i in range(len(poblacion)):
        acum_fo += funcion_objetivo(poblacion[i])
    try:
        #Fitness: diferencia entre la suma de todas las FO y la FO del cromosoma, dividido la suma
        #Para dar mayor fitness a las FO más bajas (menor distancia)
        fitness = (acum_fo - funcobj)/acum_fo
    except:
        fitness = 0
    return fitness

#Función que llena la ruleta
def llenar_ruleta(poblacion):
    cant_casilleros = 100 # 100% de la ruleta
    ruleta = [] # lista con casilleros --> 100%
    pos_fin = 0 # auxiliar para completar ruleta
    for i in range(len(poblacion)):
        x = poblacion[i] # Valor cromosoma posición i
        valor_fo = funcion_objetivo(x) # Valor función objetivo cromosoma
        fitness_i = funcion_fitness(valor_fo,poblacion) # Valor función fitness
        cant_casilleros_i = round(fitness_i*cant_casilleros) # Porcentaje de casilleros con respecto a 100
        #Lleno la ruleta con la posición del cromosoma
        for _ in range(pos_fin,pos_fin+cant_casilleros_i):
            ruleta.append(i)
        pos_fin += cant_casilleros_i
    return ruleta

def probabilidad_crossover():
    num_aleat = random.random()
    if num_aleat <= pc:
        return True
    return False

def probabilidad_mutacion():
    num_aleat = random.random()
    if num_aleat <= pm:
        return True
    return False

#Mutación
def mutacion(cromosoma):
    #elegimos dos posiciones al azar
    gen1 = random.randrange(longitud_cromosomas)
    gen2 = random.randrange(longitud_cromosomas)
    #intercambiamos genes:
    valor1 = cromosoma[gen2]
    valor2 = cromosoma[gen1]
    cromosoma[gen1] = valor1 #lo que esta en la posicion gen2 pasa a la posición gen1
    cromosoma[gen2] = valor2 #lo que esta en la posicion gen1 pasa a la posición gen2
    return cromosoma

#Crossover cíclico
def crossover(cromosoma1,cromosoma2):
    #inicializamos los dos cromosomas nuevos como lista de ceros
    nuevo_cromosoma1 = [0 for i in range(longitud_cromosomas)]
    nuevo_cromosoma2 = [0 for i in range(longitud_cromosomas)]
    #formamos el primer hijo:
    pos = 0 #inicializamos la posición para asignar al cromosoma nuevo
    while not cromosoma1[pos] in nuevo_cromosoma1: #si lo que esta en esa posición ya lo agregamos al nuevo, corta el while
        nuevo_cromosoma1[pos] = cromosoma1[pos]
        pos = cromosoma1.index(cromosoma2[pos])
    for i in range(len(nuevo_cromosoma1)): #por cada cero que quedó le asignamos lo que esta en esa posicion en el 2do padre
        if nuevo_cromosoma1[i] == 0:
            nuevo_cromosoma1[i] = cromosoma2[i]
    #formamos el segundo hijo:
    pos = 0
    while not cromosoma2[pos] in nuevo_cromosoma2: #si lo que esta en esa posición ya lo agregamos al nuevo, corta el while
        nuevo_cromosoma2[pos] = cromosoma2[pos]
        pos = cromosoma2.index(cromosoma1[pos])
    for i in range(len(nuevo_cromosoma2)): #por cada cero que quedó le asignamos lo que esta en esa posicion en el 1er padre
        if nuevo_cromosoma2[i] == 0:
            nuevo_cromosoma2[i] = cromosoma1[i]
    return nuevo_cromosoma1, nuevo_cromosoma2    

#Método de selección
def seleccion_ruleta(poblacion,elitismo):
    ruleta = llenar_ruleta(poblacion)
    seleccion = []
    if elitismo:
        cant = int(len(poblacion)-r)
    else:
        cant = len(poblacion)    
    for i in range(cant):
        #Saco un random de la ruleta
        num = random.randrange(len(ruleta))
        seleccion.append(ruleta[num])
    nueva_poblacion = []
    #Tomamos de a pares
    for i in range(0,len(seleccion),2): #para ir saltando de a 2
        cromosoma1 = poblacion[seleccion[i]]
        cromosoma2 = poblacion[seleccion[i+1]]
        if probabilidad_crossover():
            cromosoma1,cromosoma2 = crossover(cromosoma1,cromosoma2)
        if probabilidad_mutacion():
            cromosoma1 = mutacion(cromosoma1)
        if probabilidad_mutacion():
            cromosoma2 = mutacion(cromosoma2)
        nueva_poblacion.append(cromosoma1)
        nueva_poblacion.append(cromosoma2)
    return nueva_poblacion

def buscar_ruta(elitismo=False):
    crom_minimo_corrida = [] # cromosoma mínima distancia de cada corrida
    ciudades_visitadas = [] # cromosoma mínima distancia total
    distancia_total = 99999999 # Número grande para la primera comparación
    poblacion = crear_poblacion_inicial() # Crea población inicial
    for _ in range(cantidad_corridas):
        minimo = 99999999 # Número grande para la primera comparación
        lista_fitness = [] # para elitismo
        for i in range(tamano_poblacion):
            cromosoma = poblacion[i]
            valor_fo = funcion_objetivo(cromosoma) # Valor función objetivo
            valor_fit = funcion_fitness(valor_fo, poblacion) # Valor fitness
            if elitismo:
                #para elitismo
                lista_fitness.append([cromosoma,valor_fit])
            if valor_fo < minimo:
                minimo = valor_fo
                crom_minimo_corrida = cromosoma        

        if minimo < distancia_total:
            distancia_total = minimo
            ciudades_visitadas = crom_minimo_corrida #cromosoma_minimo es el que se imprime en la grafica

        if elitismo:
            #Ordeno lista por la posición 1 (fitness) de mayor a menor
            lista_fitness.sort(key=lambda x:x[1], reverse=True)
            #Me quedo con los r "ere" cromosomas élit
            poblacion_elite = []
            for i in range(r):
                poblacion_elite.append(lista_fitness[i][0])
            poblacion = seleccion_ruleta(poblacion,elitismo)
            #Vuelvo a unir la población común y elite
            poblacion += poblacion_elite
        else:
            poblacion = seleccion_ruleta(poblacion,elitismo) #SELECCION, CROSSOVER, MUTACION
        
    #Agrego la ciudad de origen al final de ciudades visitadas para graficar
    ciudades_visitadas.append(ciudades_visitadas[0])
    return ciudades_visitadas,distancia_total