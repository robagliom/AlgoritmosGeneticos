#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pick import pick
#Librería que genera combinaciones
import itertools

####################
#Variables globales#
####################
#Volumen máximo mochila en cm3
Vmax = 4200
#Lista de objetos posibles
#Tupla: (volumen objeto i en cm3, valor objeto i en $)
objetos = [[150,20],[325,40],[600,50],[805,36],[430,25],[1200,64],[770,54],[60,18],[930,46],[353,28]]

#####################
#Búsqueda exhaustiva#
#####################
#Queremos Máximizar Valor $
def maximo_valor_posible(lista_objetos):
    valor_acum = 0
    vol_acum = 0
    for objeto in lista_objetos:
        vol_acum += objeto[0]
        if vol_acum <= Vmax:
            valor_acum += objeto[1]
        else:
            #supera volumen máximo
            return 0,0
    return valor_acum,vol_acum

def generar_combinaciones(lista_objetos):
    #itertools.combinations(iterable,r): combina de a r elemenos de iterable
    lista_combinaciones = []
    for i in range(1,len(lista_objetos)+1):
        #tomo de a i elementos
        lista_combinaciones.append(itertools.combinations(lista_objetos,i))
    return lista_combinaciones

def busqueda_exhaustiva():
    valor_max = 0
    vol_acum_max = 0
    lista_solucion_max = []
    combinaciones_posibles = generar_combinaciones(objetos)
    for combinacion_i in combinaciones_posibles:
        for lista_i in combinacion_i:
            valor_max_i,vol_acum_i = maximo_valor_posible(lista_i)
            if valor_max_i > valor_max:
                valor_max = valor_max_i
                vol_acum_max = vol_acum_i
                lista_solucion_max = lista_i
    return valor_max,vol_acum_max,lista_solucion_max

##################
#Algoritmo Greedy#
##################
def proporcion_objeto(objeto):
    return objeto[1]/objeto[0]

def algoritmo_greedy():
    valor = 0
    vol_acum = 0
    lista_solucion = []
    lista_objetos = objetos
    for obj in lista_objetos:
        prop_obj = proporcion_objeto(obj)
        #agrego las proporciones a cada objeto
        obj.append(prop_obj)
    #ordeno la lista de objetos de mayor a menor según la proporción
    lista_objetos.sort(key=lambda x:x[2], reverse=True)
    for ob in lista_objetos:
        vol_aux = vol_acum + ob[0]
        if vol_aux <= Vmax:
            vol_acum += ob[0]
            valor += ob[1]
            lista_solucion.append(ob[0:2])
        else:
            pass
    return valor,vol_acum,lista_solucion

####################
#Programa Principal#
####################
def programa_principal(busqueda):
    if busqueda=="exhaustiva":
        valor_max,vol_acum_max,lista_solucion_max=busqueda_exhaustiva()
    elif busqueda=="greedy":
        valor_max,vol_acum_max,lista_solucion_max=algoritmo_greedy()
    else:
        return
    print("Valor máximo $",valor_max)
    print("Volumen máximo cm3",vol_acum_max)
    print("Objetos elegidos",lista_solucion_max)

    return valor_max,vol_acum_max,lista_solucion_max

######
#Menú#
######
def menu():
    que_hacer = 'Problema de la Mochila'
    opciones_que_hacer = ['1) Búsqueda Exhaustiva','2) Algoritmo Greedy', 'X SALIR']
    opcion_que_hacer, index = pick(opciones_que_hacer, que_hacer)
    if opcion_que_hacer == '1) Búsqueda Exhaustiva':
        programa_principal("exhaustiva")
    elif opcion_que_hacer == '2) Algoritmo Greedy':
        programa_principal("greedy")
    else:
        sys.exit()

menu()
