#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Manejo de excel
import xlwt
from xlwt import Workbook
from xlrd import open_workbook

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