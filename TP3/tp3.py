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

def buscar_ruta(ciudad=None):
    print("Ciudad", ciudad, dict_ciudades.get(ciudad))
    return "resultado"

def recorrido_min_alg_genet():
    print('Algoritmos genéticos')
    return "resultado"

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
            op_submenu_1 =[
                'X VOLVER'
            ]
            #Agrego lista de ciudades al submenú
            for i in range(len(dict_ciudades)): 
                op_submenu_1.append(dict_ciudades.get(i+1))

            _, index_submenu_1 = pick(op_submenu_1,submenu_1)
            if index_submenu_1 == 0:
                #volver
                menu()
            else:
                #Ciudad = index_submenu_1
                resultado=buscar_ruta(index_submenu_1)
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