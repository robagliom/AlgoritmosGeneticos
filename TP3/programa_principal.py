#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pick import pick

#Mapas
import mapas
#Búsqueda heurística
import busqueda_heuristica
#Algorítmo genético
import algoritmo_genetico
#Diccionarios
import datos
#Excel
import excel

try:
  os.stat("resultados")
except:
  os.mkdir("resultados")

def buscar_ruta(ciudad_origen=None):
    #Si eligió ciudad de origen
    if ciudad_origen:
        ciudades_visitadas,distancia_total = busqueda_heuristica.buscar_ruta(ciudad_origen)
    #Si no se elige ciudad hay que devolver la ruta mínima
    else:
        distancia_total = 999999 #seteo número grande
        ciudades_visitadas = []
        for c in datos.dict_ciudades:
            lista_ciudades_visitadas,distancia = busqueda_heuristica.buscar_ruta(c)
            if distancia < distancia_total:
                distancia_total = distancia
                ciudades_visitadas = lista_ciudades_visitadas
    #dibujar mapa resultados
    dibujar_mapa(ciudades_visitadas,distancia_total)
    return #"Distancia total recorrida: {}\nOrden de visitas: {}".format(distancia_total,ciudades_visitadas)

def recorrido_min_alg_genet(elitismo=False):
    #dibujar mapa resultados
    ciudades_visitadas,distancia_total = algoritmo_genetico.buscar_ruta(elitismo)
    dibujar_mapa(ciudades_visitadas,distancia_total)
    return

#Recibe lista ordenada con los índices de las ciudades
def dibujar_mapa(lista_ciudades,distancia_total):
    #Creo mapa
    url_mapa = mapas.crear_mapa(lista_ciudades,distancia_total)
    import webbrowser
    return webbrowser.open(url_mapa, new=2, autoraise=True)

def menu():
    menu_principal = 'El problema del viajante'
    op_menu_principal = [
        'Buscar recorrido mínimo con método: desde cada ciudad ir a la ciudad más cercana no visitada', 
        'Buscar recorrido mínimo con algoritmos genéticos', 
        'X SALIR'
    ]
    _, index_menu_principal = pick(op_menu_principal, menu_principal)
    if index_menu_principal == 0:
        submenu = 'Buscar recorrido mínimo con método: desde cada ciudad ir a la ciudad más cercana no visitada'
        op_submenu = [
            'Ingresar ciudad de origen',
            'Calcular recorrido mínimo',
            'X VOLVER'
        ]
        _, index_submenu = pick(op_submenu,submenu)
        if index_submenu == 0:
            submenu_1 = 'Eliga ciudad de origen'
            op_submenu_1 =[]
            #Agrego lista de ciudades al submenú
            for i in range(len(datos.dict_ciudades)): 
                op_submenu_1.append(datos.dict_ciudades.get(i+1))
            op_submenu_1.append('X VOLVER')
            op_submenu_1, index_submenu_1 = pick(op_submenu_1,submenu_1)
            if op_submenu_1 == 'X VOLVER':
                #volver
                menu()
            else:
                #Ciudad = index_submenu_1
                buscar_ruta(index_submenu_1+1)
                seguir, _ = pick(['SI','X SALIR'], 'Continuar?')
                if seguir == 'SI':
                    menu()
                else:
                    sys.exit()
        elif index_submenu==1:
            buscar_ruta()
            seguir, _ = pick(['SI','X SALIR'], 'Continuar?')
            if seguir == 'SI':
                menu()
            else:
                sys.exit()
        else:
            menu()
    elif index_menu_principal == 1:
        submenu = 'Buscar recorrido mínimo con algoritos genéticos'
        op_submenu = ['Sin elitismo', 'Con elitismo', 'X VOLVER']
        _, index_submenu = pick(op_submenu,submenu)
        if index_submenu == 0:
            recorrido_min_alg_genet()
        elif index_submenu == 1:
            recorrido_min_alg_genet(True)
        else:
            #volver
            menu()
        seguir, _ = pick(['SI','X SALIR'], 'Continuar?')
        if seguir == 'SI':
            menu()
        else:
            sys.exit()
    else:
        #Salir
        sys.exit()

menu()