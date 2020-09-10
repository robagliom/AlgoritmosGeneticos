#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Manejo de mapa
import folium
#Datos
import datos

def crear_mapa(lista,distancia_total):
    #Mapa
    m = folium.Map(
                    #Argentina
                    location=[-34.9964963,-64.9672817],
                    zoom_start=4            
        )
    #Agrego marcadores
    ciudad_origen = lista[0]
    localizaciones = []
    ciudades = []
    for i in lista:
        localizacion = tuple(datos.dict_geo_ciudades.get(i)[0])
        nombre_ciudad = str(datos.dict_geo_ciudades.get(i)[1])
        ciudades.append(nombre_ciudad)
        if i == ciudad_origen:
            folium.Marker(localizacion,popup=nombre_ciudad,icon=folium.Icon(color='green',icon_color='green')).add_to(m)
        else:
            folium.Marker(localizacion,popup=nombre_ciudad).add_to(m)
        localizaciones.append(localizacion)
    #Agrego líneas
    folium.PolyLine(localizaciones, color="red", weight=2.5, opacity=1).add_to(m)

    #Agrego text   
    title_html = '''
                    <h3 align="center" style="font-size:16px"><b>Distancia total recorrida: {} km</b></h3>
                    <p align="justify"><b>Recorrido:</b> {}</p>
                '''.format(distancia_total,ciudades)

    m.get_root().html.add_child(folium.Element(title_html))

    url_mapa = "resultados/mapa.html"
    m.save(url_mapa)
    return url_mapa