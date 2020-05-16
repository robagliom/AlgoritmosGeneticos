#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pick import pick
import random
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
import xlwt
from xlwt import Workbook

try:
  os.stat("resultados")
except:
  os.mkdir("resultados")

# Variables globales
long_cromosomas = 30 # Longitud de los cromosomas
cant_pi = 10 # Cantidad población inicial
pc = 0.75 # Probabilidad de crossover
pm = 0.05 # Probabilidad de mutación

r=2 #elitismo

# Función objetivo
def funcion_objetivo(x):
    return (x/((2**30)-1))**2

# Función para crear población inicial
def crear_poblacion_inicial():
    poblacion_inicial = []
    for _ in range(cant_pi):
        cromosoma = "" # Auxiliar para crear cada cromosoma
        for _ in range(long_cromosomas):
            cromosoma += str(random.randrange(2)) # Concatena random 0 o 1
        poblacion_inicial.append(cromosoma) # Agrega cromosoma a la poblacion
    return poblacion_inicial

# Función para calcular el fitness
# Argumentos: funcobj = valor de la función objetivo, poblacion = lista de cromosomas binario
def funcion_fitness(funcobj,poblacion):
    suma_fo = 0 # Acumulado
    for i in range(len(poblacion)):
        suma_fo += funcion_objetivo(int(poblacion[i],2))
    try:
        fitness = funcobj/suma_fo
    except:
        fitness = 0
    return fitness

# Exportar datos
def exportar_datos(columnas,data,cant_corr,elitismo):
    wb = Workbook()
    sheet1= wb.add_sheet('Resultados')
    bold = xlwt.easyxf('font:bold 1')
    fila = 0
    col = 0
    for c in columnas: # c es cada título en columnas (Corrida, Mínimo, Máximo, Cromosoma Máximo, Promedio)
        sheet1.write(fila,col,c,bold)
        col+=1
    fila+=1
    for d_fila in data: # d_fila es cada fila de data
        col = 0
        for d in d_fila: # d es cada celda de la fila
            sheet1.write(fila,col,d)
            col+=1
        fila+=1
    if elitismo:
        wb.save('resultados/tabla_{}_corridas_elitismo.xls'.format(cant_corr))
    else:
        wb.save('resultados/tabla_{}_corridas.xls'.format(cant_corr))
    return

def graficar_resultados(data,titulo,cant_corr,elitismo):
    #data = ["Corrida","Mínimo","Máximo","Cromosoma Máximo","Promedio"]
    plt.title(titulo)
    lista_minimos = []
    lista_maximos = []
    lista_promedios = []
    for d in data:
        lista_minimos.append(d[1])
        lista_maximos.append(d[2])
        lista_promedios.append(d[4])
    plt.plot(lista_minimos,'ro-',markersize=0.5,lw=0.5,color='red',label="Mínimos")
    plt.plot(lista_maximos,'ro-',markersize=0.5,lw=0.5,color='blue',label="Máximos")
    plt.plot(lista_promedios,'ro-',markersize=0.5,lw=0.5,color='green',label="Promedios")
    plt.grid(True)
    plt.xlabel('Número de corrida')
    plt.ylabel('Valor función objetivo')
    plt.legend()
    if elitismo:
        plt.savefig('resultados/grafica_{}_corridas_elitismo.png'.format(cant_corr))
    else:
        plt.savefig('resultados/grafica_{}_corridas.png'.format(cant_corr))
    plt.close()
    return

#Llenar ruleta
def llenar_ruleta(poblacion):
    cant_casilleros = 100 # 100% de la ruleta
    ruleta = [] # lista con casilleros --> 100%
    pos_fin = 0 # auxiliar para completar ruleta
    for i in range(len(poblacion)):
        x = int(poblacion[i],2) # Valor x (Cromosoma pasado a entero)
        valor_fo = funcion_objetivo(x) # Valor función objetivo
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

#Operador Mutación
#Argumentos
#cromosoma: el cromosoma a mutar
def mutacion(cromosoma):
    gen = random.randrange(long_cromosomas)
    cromosoma_mut = list(cromosoma) # String a Lista
    if cromosoma_mut[gen]=='0':
        cromosoma_mut[gen]='1'
    else:
        cromosoma_mut[gen]='0'
    cromosoma_mut = "".join(cromosoma_mut) # Lista a String
    return cromosoma_mut

# Operador Crossover
# Argumentos: cromosomas a cruzar
def crossover(cromosoma1,cromosoma2):
    corte = random.randrange(long_cromosomas) # Punto de corte
    nuevo_cromosoma1 = cromosoma1[:corte] + cromosoma2[corte:]
    nuevo_cromosoma2 = cromosoma2[:corte] + cromosoma1[corte:]

    return nuevo_cromosoma1, nuevo_cromosoma2

#Método de selección
#Argumentos:
#poblacion: lista de poblacion actual
def seleccion_ruleta(poblacion):
    ruleta = llenar_ruleta(poblacion)
    seleccion = []
    for i in range(len(poblacion)):
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

#Argumentos:
#cant_corridas: int cantidad de corridas
#elitistmo: boolean si hay o no elitismo
def programa_principal(cant_corridas, elitismo):
    try:
        crom_maximo_corrida = '' # cromosoma máximo de cada corrida
        cromosoma_maximo = '' # cromosoma maximo total
        maximo_total = 0
        tabla_final = [] # tabla con los datos obetenidos en cada corrida
        poblacion = crear_poblacion_inicial() # Crea población inicial
        for c in range(cant_corridas):
            suma_fo = 0
            minimo = 999999 # Número grande para la primera comparación
            maximo = 0
            fila_tabla = []
            lista_fitness = [] # para elitismo
            for i in range(cant_pi):
                cromosoma = poblacion[i]
                x = int(cromosoma,2) # Valor x (Cromosoma pasado a entero)
                valor_fo = funcion_objetivo(x) # Valor función objetivo
                valor_fit = funcion_fitness(valor_fo, poblacion) # Valor fitness
                if elitismo:
                    #para elitismo
                    lista_fitness.append([cromosoma,valor_fit])
                suma_fo += valor_fo
                if valor_fo > maximo:
                    maximo = valor_fo
                    crom_maximo_corrida = cromosoma
                if valor_fo < minimo:
                    minimo = valor_fo
            promedio = suma_fo/cant_pi
            #if crom_maximo_corrida > cromosoma_maximo:
            if maximo > maximo_total:
                maximo_total = maximo
                cromosoma_maximo = crom_maximo_corrida #cromosoma_maximo es el que se imprime en la grafica

            if elitismo:
                #Ordeno lista por la posición 1 (fitness) de mayor a menor
                lista_fitness.sort(key=lambda x:x[1], reverse=True)
                #Me quedo con los r "ere" cromosomas élit
                poblacion_elite = []
                for i in range(r):
                    poblacion_elite.append(lista_fitness[i][0])
                #Mando a selección rulea los cromosomas comunes
                poblacion_comun = []
                for i in range(r,len(poblacion)):
                    poblacion_comun.append(lista_fitness[i][0])
                poblacion = seleccion_ruleta(poblacion_comun)
                #Vuelvo a unir la población común y elite
                poblacion += poblacion_elite
            else:
                poblacion = seleccion_ruleta(poblacion) #SELECCION, CROSSOVER, MUTACION

            # Llena fila de la tabla
            fila_tabla.append(c)
            fila_tabla.append(minimo)
            fila_tabla.append(maximo)
            fila_tabla.append(crom_maximo_corrida)
            fila_tabla.append(promedio)
            tabla_final.append(fila_tabla) # Agrega fila a la tabla
        columnas_final = ["Corrida","Mínimo","Máximo","Cromosoma Máximo","Promedio"]
        exportar_datos(columnas_final,tabla_final,cant_corridas,elitismo)
        titulo = "Cromosoma que genera el máximo: {}".format(cromosoma_maximo)
        graficar_resultados(tabla_final,titulo,cant_corridas,elitismo)

        return "Algoritmo corrido con éxito, los resultados fueron guardados"
    except:
        return "Ups, algo salió mal"

def menu():
    que_hacer = 'Algoritmos genéticos'
    opciones_que_hacer = ['NORMAL', 'CON ELITISMO', 'X SALIR']
    opcion_que_hacer, index = pick(opciones_que_hacer, que_hacer)
    if opcion_que_hacer == 'NORMAL':
        elitismo = False
    elif opcion_que_hacer == 'CON ELITISMO':
        elitismo = True
    else:
        sys.exit()
    cuantas_corridas = 'Cuántas corridas va a hacer?'
    corridas = ['20','100','200', 'X VOLVER']
    cant_corr, index = pick(corridas, cuantas_corridas)
    if cant_corr == 'X VOLVER':
        menu()
    else:
        resultado=programa_principal(int(cant_corr),elitismo)
        seguir, index = pick(['SI','X SALIR'], '{}. Continuar?'.format(resultado))
        if seguir == 'SI':
            menu()
        else:
            sys.exit()

menu()
