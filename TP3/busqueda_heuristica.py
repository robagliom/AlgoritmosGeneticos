#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datos
import excel

#Funcion que actualiza lista de ciudades visitadas
def actualizar_ciudades_visitadas(lista,indice_ciudad):
    lista_actualizada = []
    for i in lista:
        if i[0] == indice_ciudad:
            lista_actualizada.append((i[0],True))
        else:
            lista_actualizada.append(i)
    return lista_actualizada

#Devuelve la ciudad que está a menor distancia
def proxima_ciudad(lista_distancias, ciudades_visitadas):
    #ordeno por menor distancia
    lista_distancias = sorted(lista_distancias, key=lambda x: x[1])
    for i in lista_distancias:
        visitada = list(filter(lambda x: x[0]==i[0] and x[1]==False,ciudades_visitadas))
        if len(visitada) == 1:
            return i
    #elegir la menor de lista_distancias y que no esté en ciudades_visitadas
    return

#Devuelve true si quedan ciudades, false si ya se recorrieron todas
def quedan_ciudades_por_visitar(lista):
    ciudades_no_visitadas = list(filter(lambda x: x[1]==False,lista))
    if len(ciudades_no_visitadas) > 0:
        return True
    return False

def buscar_ruta(ciudad_origen):
    #Seteo lista para mantener ciudades visitadas
    lista_ciudades_visitadas = []
    for i in range(len(datos.dict_ciudades)): 
            lista_ciudades_visitadas.append((i+1,False))
    #Mantengo orden de visitas
    ciudades_visitadas = [ciudad_origen]
    #Si eligió ciudad de origen
    if ciudad_origen:
        #Pongo en true ciudad de origen para no visitarla
        lista_ciudades_visitadas = actualizar_ciudades_visitadas(lista_ciudades_visitadas,ciudad_origen)
        distancia_total = 0
        prox_ciudad = ciudad_origen
        while quedan_ciudades_por_visitar(lista_ciudades_visitadas):
            #Busco distancias desde la ciudad elegida
            distancias_ciudad_origen = excel.buscar_distancia_excel(prox_ciudad)
            #Ciudad de menor a mayor por la distancia
            tupla_prox_ciudad = proxima_ciudad(distancias_ciudad_origen,lista_ciudades_visitadas)
            #Índice próxima ciudad
            prox_ciudad = tupla_prox_ciudad[0]
            #Actualizo distancia recorrida
            distancia_total += int(tupla_prox_ciudad[1])
            #Actualizo ciudades visitadas
            lista_ciudades_visitadas = actualizar_ciudades_visitadas(lista_ciudades_visitadas,prox_ciudad)
            #Actualizo lista orden
            ciudades_visitadas.append(prox_ciudad)
        #Agrego la distanca de la última ciudad a la de origen
        distancia_total += excel.distancia_entre_ciudades(prox_ciudad,ciudad_origen)
        #Agrego la ciudad de origen al final de ciudades visitadas
        ciudades_visitadas.append(ciudad_origen)
    return ciudades_visitadas,distancia_total