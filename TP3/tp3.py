#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from pick import pick
import random
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
#Manejo de excel
import xlwt
from xlwt import Workbook
from xlrd import open_workbook

import mapas

try:
  os.stat("resultados")
except:
  os.mkdir("resultados")

# Variables globales
dict_ciudades = {
                1:'Cdad. de Bs. As.',
                2:'Córdoba',
                3:'Corrientes',
                4:'Formosa',
                5:'La Plata',
                6:'La Rioja',
                7:'Mendoza',
                8:'Neuquén',
                9:'Paraná',
                10:'Posadas',
                11:'Rawson',
                12:'Resistencia',
                13:'Río Galleqos',
                14:'S.F.d.V.d. Catamarca',
                15:'S.M. de Tucumán',
                16:'S.S. de Jujuy',
                17:'Salta',
                18:'San Juan',
                19:'San Luis',
                20:'Santa Fe',
                21:'Santa Rosa',
                22:'Sgo. Del Estero',
                23:'Ushuaia',
                24:'Viedma',
}
#for i in range(len(dict_ciudades)): print(i,dict_ciudades.get(i+1))

 #Traemos excel con datos a memoria
url_excel = "Datos/TablaCapitales.xlsx"
excel = open_workbook(url_excel)
hoja = excel.sheet_by_name('Distancias')

#Recibe el indice de la ciudad
#Devuelve lista de tuplas (int: indice_ciudad,int: distancia)
def buscar_distancia_excel(indice_ciudad):
    for i in range(1,25):
        indice_ciudad_excel = hoja.cell_value(rowx=i, colx=0)
        if indice_ciudad == indice_ciudad_excel:
            distancias = []
            for j in range(1,25):
                valor_celda = hoja.cell_value(rowx=i,colx=j)
                distancias.append((j,int(valor_celda)))
            break
    return distancias

def distancia_entre_ciudades(indice_ciudad_1,indice_ciudad_2):
    return int(hoja.cell_value(rowx=indice_ciudad_1,colx=indice_ciudad_2))

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

def buscar_ruta(ciudad_origen=None):
    #Seteo lista para mantener ciudades visitadas
    lista_ciudades_visitadas = []
    for i in range(len(dict_ciudades)): 
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
            distancias_ciudad_origen = buscar_distancia_excel(prox_ciudad)
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
        distancia_total += distancia_entre_ciudades(prox_ciudad,ciudad_origen)
        #Agrego la ciudad de origen al final de ciudades visitadas
        ciudades_visitadas.append(ciudad_origen)
    dibujar_mapa(ciudades_visitadas,distancia_total)
    return "Distancia total recorrida: {}\nOrden de visitas: {}".format(distancia_total,ciudades_visitadas)

def recorrido_min_alg_genet():
    print('Algoritmos genéticos')
    return "resultado"

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
            for i in range(len(dict_ciudades)): 
                op_submenu_1.append(dict_ciudades.get(i+1))
            op_submenu_1.append('X VOLVER')
            op_submenu_1, index_submenu_1 = pick(op_submenu_1,submenu_1)
            if op_submenu_1 == 'X VOLVER':
                #volver
                menu()
            else:
                #Ciudad = index_submenu_1
                resultado=buscar_ruta(index_submenu_1+1)
                seguir, _ = pick(['SI','X SALIR'], '{}. Continuar?'.format(resultado))
                if seguir == 'SI':
                    menu()
                else:
                    sys.exit()
        elif index_submenu==1:
            resultado=buscar_ruta()
            seguir, _ = pick(['SI','X SALIR'], '{}. Continuar?'.format(resultado))
            if seguir == 'SI':
                menu()
            else:
                sys.exit()
        else:
            menu()
    elif index_menu_principal == 1:
        #Buscar recorrido mínimo con algoritmos genéticos
        resultado=recorrido_min_alg_genet()
        seguir, _ = pick(['SI','X SALIR'], '{}. Continuar?'.format(resultado))
        if seguir == 'SI':
            menu()
        else:
            sys.exit()
    else:
        #Salir
        sys.exit()

menu()