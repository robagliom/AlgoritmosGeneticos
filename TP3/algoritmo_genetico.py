#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
#Elitismo
r=2

def buscar_ruta():
    ciudades_visitadas = []
    distancia_total = 0
    return ciudades_visitadas,distancia_total