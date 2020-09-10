#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Manejo de mapa
import folium

def crear_mapa(lista):
    #Mapa
    m = folium.Map(
                    #Argentina
                    location=[-34.9964963,-64.9672817],
                    zoom_start=4            
        )
    #Agrego marcadores
    ciudad_origen = lista[0]
    localizaciones = []
    for i in lista:
        localizacion = tuple(dict_geo_ciudades.get(i)[0])
        nombre_ciudad = str(dict_geo_ciudades.get(i)[1])
        if i == ciudad_origen:
            folium.Marker(localizacion,popup=nombre_ciudad,icon=folium.Icon(color='green',icon_color='green')).add_to(m)
        else:
            folium.Marker(localizacion,popup=nombre_ciudad).add_to(m)
        localizaciones.append(localizacion)
    #Agrego líneas
    folium.PolyLine(localizaciones, color="red", weight=2.5, opacity=1).add_to(m)

    url_mapa = "resultados/mapa.html"
    m.save(url_mapa)
    return url_mapa

#Geolocalizaciones
dict_geo_ciudades = {
                1:[[-34.6075682,-58.4370894],'Cdad. de Bs. As.'],
                2:[[-31.4173391,-64.183319],'Córdoba'],
                3:[[-28.5912315,-57.9394658],'Corrientes'],
                4:[[-24.5955306,-60.4289718],'Formosa'],
                5:[[-34.9206797,-57.9537638],'La Plata'],
                6:[[-29.4069066,-66.8498038],'La Rioja'],
                7:[[-34.7871961,-68.4380712],'Mendoza'],
                8:[[-38.3695057,-69.832275],'Neuquén'],
                9:[[-31.7330145,-60.5298511],'Paraná'],
                10:[[-27.3664824,-55.894295],'Posadas'],
                11:[[-43.2991348,-65.1056655],'Rawson'],
                12:[[-27.4511235,-58.9865196],'Resistencia'],
                13:[[-51.6232352,-69.1090848],'Río Galleqos'],
                14:[[-27.1910825,-67.105374],'S.F.d.V.d. Catamarca'],
                15:[[-26.5643582,-64.882397],'S.M. de Tucumán'],
                16:[[-23.3161458,-65.7595288],'S.S. de Jujuy'],
                17:[[-25.1076701,-64.3494964],'Salta'],
                18:[[-30.7054363,-69.1988222],'San Juan'],
                19:[[-33.2762202,-65.9515546],'San Luis'],
                20:[[-30.3154739,-61.1645076],'Santa Fe'],
                21:[[-36.6203925,-64.2906107],'Santa Rosa'],
                22:[[-27.6431016,-63.5408542],'Sgo. Del Estero'],
                23:[[-54.8069332,-68.3073246],'Ushuaia'],
                24:[[-40.8084274,-62.994722],'Viedma']
}    