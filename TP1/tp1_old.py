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

### Variables globales ###
long_cromosomas = 30
#Crear población inicial (vamos a elegir cantidad inicial = 4)
cant_pi = 10 #cantidad población inicial
#Probabilidades
#Crossover
pc = 0.75
#Mutación
pm = 0.05
#elitismo
r=2

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
    for i in range(len(poblacion)):
        suma_fo += funcion_objetivo(int(poblacion[i],2))
    try:
        fitness = funcobj/suma_fo
    except:
        fitness = 0
    return fitness

#Dibujo tabla
def exportar_datos(columnas, data,cant_corr,elitismo):
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
    if elitismo:
        plt.savefig('resultados/grafica_{}_corridas_elitismo.png'.format(cant_corr))
    else:
        plt.savefig('resultados/grafica_{}_corridas.png'.format(cant_corr))
    plt.close()
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
#elitistmo: boolean si hay o no elitismo
def programa_principal(cant_pi, cant_corridas, elitismo):
    try:
        #guardo los datos obetenidos en cada corrida
        tabla_final = []
        #Creo población inicial
        poblacion =  crear_poblacion_inicial(cant_pi,long_cromosomas)
        #seteo variable auxiliar para que no rompa
        crom_maximo_corrida = poblacion[0]
        cromosoma_maximo = crom_maximo_corrida

        for c in range(cant_corridas):
            suma_fo = 0
            minimo = 2**30 #infinito
            maximo = 0
            tabla_corrida = []
            #para elitismo
            lista_fitness = []
            for i in range(len(poblacion)):
                cromosoma = poblacion[i] #binario
                cromosoma_entero = int(poblacion[i],2) #decimal
                valor_fo = funcion_objetivo(cromosoma_entero) #valor función objetivo
                valor_fit = funcion_fitness(valor_fo, poblacion)#valor fitness
                if elitismo:
                    #para elitismo
                    lista_fitness.append([cromosoma,valor_fit])
                suma_fo += valor_fo
                if valor_fo > maximo:
                    maximo = valor_fo
                    crom_maximo_corrida = cromosoma
                if valor_fo < minimo:
                    minimo = valor_fo
            promedio = suma_fo/len(poblacion)
            if crom_maximo_corrida > cromosoma_maximo:
                cromosoma_maximo = crom_maximo_corrida

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
                poblacion = seleccion_ruleta(poblacion)
            #lleno tabla de la corrida
            tabla_corrida.append(c)
            tabla_corrida.append(minimo)
            tabla_corrida.append(maximo)
            tabla_corrida.append(crom_maximo_corrida)
            tabla_corrida.append(promedio)
            tabla_final.append(tabla_corrida)
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
        resultado=programa_principal(cant_pi,int(cant_corr),elitismo)
        seguir, index = pick(['SI','X SALIR'], '{}. Continuar?'.format(resultado))
        if seguir == 'SI':
            menu()
        else:
            sys.exit()

menu()
