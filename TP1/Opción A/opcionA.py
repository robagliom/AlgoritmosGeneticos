#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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

### Variables globales ###
long_cromosomas = 30
#Crear población inicial (vamos a elegir cantidad inicial = 4)
cant_pi = 10 #cantidad población inicial
#Cantidad de corridas
cant_corr = 200
#Probabilidades
#Crossover
pc = 0.75
#Mutación
pm = 0.05

# Función objetivo
def funcion_objetivo(x):
    return (x/((2**30)-1))**2
#Función para crear población inicial
#Parámetros: cantidad-->cantidad de cromosomas
#            longitud-->longitud de cada cromosoma
def crear_poblacion_inicial(cantidad,longitud):
    poblacion_inicial = list() #lista población inicial
    for i in range(cantidad):
        cromosoma_inicial = "" #auxiliar para crear cada cromosoma
        for i in range(longitud):
            #genero un gen aleatorio y lo agrego al cromosoma
            cromosoma_inicial += str(random.randrange(2)) #genera random: 0 o 1
        poblacion_inicial.append(cromosoma_inicial)
    return poblacion_inicial

#recibe funcobj:valor de la función objetivo, poblacion: lista de cromosomas binario
def funcion_fitness(funcobj,poblacion):
    suma_fo = 0 #suma funciones objetivo
    for i in range(cant_pi):
        suma_fo += funcion_objetivo(int(poblacion[i],2))
    try:
        fitness = funcobj/suma_fo
    except:
        fitness = 0
    return fitness

#Dibujo tabla
def exportar_datos(columnas, data,resultados=[]):
    wb = Workbook()
    sheet1= wb.add_sheet('Resultados')
    bold = xlwt.easyxf('font:bold 1')
    fila = 0
    col = 0
    for c in columnas:
        sheet1.write(fila,col,c, bold)
        col+=1
    fila+=1
    for d_fila in data:
        col = 0
        for d in d_fila:
            sheet1.write(fila,col,d)
            col+=1
        fila+=1
    wb.save('resultados/tabla_{}_corridas.xls'.format(cant_corr))

    return

def graficar_resultados(data,titulo):
    #data = ["Corrida","Mínimo","Máximo","Cromosoma Máximo","Promedio"]
    plt.title(titulo)
    lista_minimos = []
    lista_maximos = []
    lista_promedios = []
    for d in data:
        lista_minimos.append([d[0],d[1]])
        lista_maximos.append([d[0],d[2]])
        lista_promedios.append([d[0],d[4]])
    xmin,ymin = zip(*[i for i in lista_minimos])
    xmax,ymax = zip(*[i for i in lista_maximos])
    xprom,yprom = zip(*[i for i in lista_promedios])
    plt.plot(xmin,ymin,'ro-',markersize=0.5,lw=0.5,color='red',label="Mínimos")
    plt.plot(xmax,ymax,'ro-',markersize=0.5,lw=0.5,color='blue',label="Máximos")
    plt.plot(xprom,yprom,'ro-',markersize=0.5,lw=0.5,color='green',label="Promedios")
    plt.grid(True)
    plt.xlabel('Número de corrida')
    plt.ylabel('Valor función objetivo')
    plt.legend()
    plt.savefig('resultados/grafica_{}_corridas.png'.format(cant_corr))
    return

#Llenar ruleta
def llenar_ruleta(poblacion):
    cant_casilleros = 100
    ruleta = [] #lista con casilleros --> 100%
    nueva_poblacion = []
    pos_fin = 0 #auxiliar para completar ruleta
    for i in range(len(poblacion)):
        valor_fo = funcion_objetivo(int(poblacion[i],2))
        fitness_i = funcion_fitness(valor_fo,poblacion)
        cant_casilleros_i = round(fitness_i*cant_casilleros) #porcentaje de casilleros con respecto a 100
        #Lleno la ruleta con la posición del cromosoma
        for j in range(pos_fin,cant_casilleros_i+pos_fin):
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
    num_aleat = random.randrange(len(cromosoma))
    cromosoma_mut = list(cromosoma)
    if cromosoma_mut[num_aleat]=='0':
        cromosoma_mut[num_aleat]='1'
    else:
        cromosoma_mut[num_aleat]='0'
    cromosoma_mut = "".join(cromosoma_mut)
    return cromosoma_mut

#Operador Crossover
#Argumentos:
#n: número de cortes
#cromosoma1 y cromosoma2: cromosomas para hacer crossover
#Return: dos cromosomas hijos
def crossover(n,cromosoma1,cromosoma2):
    nuevo_cromosoma1 = list(cromosoma1)
    nuevo_cromosoma2 = list(cromosoma2)
    for i in range(n):
        corte = random.randrange(long_cromosomas)
        nuevo_cromosoma1[corte:]=cromosoma2[corte:]
        nuevo_cromosoma2[corte:]=cromosoma1[corte:]
    """if probabilidad_mutacion():
        nuevo_cromosoma1 = mutacion(nuevo_cromosoma1)
    else:
        nuevo_cromosoma1 = "".join(nuevo_cromosoma1)
    if probabilidad_mutacion():
        nuevo_cromosoma2 = mutacion(nuevo_cromosoma2)
    else:
        nuevo_cromosoma2 = "".join(nuevo_cromosoma2)"""
    nuevo_cromosoma1 = "".join(nuevo_cromosoma1)
    nuevo_cromosoma2 = "".join(nuevo_cromosoma2)
    return nuevo_cromosoma1,nuevo_cromosoma2

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
    for i in range(0,len(seleccion),2):
        cromosoma1 = poblacion[seleccion[i]]
        cromosoma2 = poblacion[seleccion[i+1]]
        """""if probabilidad_crossover():
            nuevo_cromosoma1,nuevo_cromosoma2 = crossover(1,cromosoma1,cromosoma2)
            nueva_poblacion.append(nuevo_cromosoma1)
            nueva_poblacion.append(nuevo_cromosoma1)
        else:
            nueva_poblacion.append(cromosoma1)
            nueva_poblacion.append(cromosoma2)"""
        if probabilidad_crossover():
            cromosoma1,cromosoma2 = crossover(1,cromosoma1,cromosoma2)
        if probabilidad_mutacion():
            cromosoma1 = mutacion(cromosoma1)
        if probabilidad_mutacion():
            cromosoma2 = mutacion(cromosoma2)
        nueva_poblacion.append(cromosoma1)
        nueva_poblacion.append(cromosoma2)
    return nueva_poblacion

#Argumentos:
#cant_pi: int cantidad de elementos (cromosomas) de la población inicial
#cant_corridas: int cantidad de corridas
def programa_principal(cant_pi, cant_corridas):
    #guardo los datos obetenidos en cada corrida
    tabla_final = []
    #Creo población inicial
    poblacion =  crear_poblacion_inicial(cant_pi,long_cromosomas)
    #seteo variable auxiliar para que no rompa
    crom_maximo_corrida = poblacion[0]
    cromosoma_maximo = crom_maximo_corrida

    for c in range(cant_corridas):
        suma_fo = 0
        promedio = 0
        minimo = 2**30 #infinito
        maximo = 0
        tabla_corrida = []
        for i in range(cant_pi):
            cromosoma = poblacion[i] #binario
            cromosoma_entero = int(poblacion[i],2) #decimal
            valor_fo = funcion_objetivo(cromosoma_entero) #valor función objetivo
            valor_fit = funcion_fitness(valor_fo, poblacion)#valor fitness
            suma_fo += valor_fo
            promedio = suma_fo/cant_pi
            if valor_fo > maximo:
                maximo = valor_fo
                crom_maximo_corrida = cromosoma
            if valor_fo < minimo:
                minimo = valor_fo
        if crom_maximo_corrida > cromosoma_maximo:
            cromosoma_maximo = crom_maximo_corrida
        poblacion = seleccion_ruleta(poblacion)
        #lleno tabla de la corrida
        tabla_corrida.append(c)
        tabla_corrida.append(minimo)
        tabla_corrida.append(maximo)
        tabla_corrida.append(crom_maximo_corrida)
        tabla_corrida.append(promedio)
        tabla_final.append(tabla_corrida)
    columnas_final = ["Corrida","Mínimo","Máximo","Cromosoma Máximo","Promedio"]
    exportar_datos(columnas_final,tabla_final)
    titulo = "Cromosoma que genera el máximo: {}".format(cromosoma_maximo)
    graficar_resultados(tabla_final,titulo)
    return

programa_principal(cant_pi,cant_corr)
