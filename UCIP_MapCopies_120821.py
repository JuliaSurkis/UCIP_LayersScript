# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:21:55 2021

@author: jsurkis
"""

from IPython.display import display
import arcgis
from arcgis.gis import GIS
from arcgis.mapping import WebMap
import os
import json
import getpass
import arcpy

# connect to your GIS
portal_url = arcpy.GetActivePortalURL()
print(portal_url)

user = getpass.getpass(prompt='    Enter arcgis.com username:\n')
pw = getpass.getpass(prompt='    Enter arcgis.com password:\n')
arcpy.SignInToPortal(portal_url, user, pw)

gis = GIS(portal_url, user, pw)

#Find web map to be copied
webmap_search = gis.content.search(query = 'title:UCIP_Map_120221_Final', item_type="Web_Map", sort_field='numViews', sort_order='desc', max_items=9999)

map_item = webmap_search[0]

#Show layer information to make sure we are referencing appropriate map layer
#webmapJSON = map_item.get_data()
#for layer in webmapJSON['operationalLayers']:
    
#    display(layer)
    
    
web_map_dict = map_item.get_data(try_json=True)

# Just Counties:
# counties = gis.content.get('5d55fd5a8ad34448a32b2b5e34ce9ab9').layers[0].query()

# Counties and municipalities:
counties = gis.content.get('6e5e56892ecb4be5990467419f69d248').layers[0].query()
spat_ref = counties.spatial_reference

#Loop through each county/muni and create map with same properties for each
for index, county in enumerate(counties):
    county_name = counties.features[index].attributes['NAME']
    print(county_name) 
    title = "UCIP_" + county_name + "_120621_Final"
    
    #Find and add properties from master map to each jurisdictions map
    web_map_properties = {'title': title,
                         'type':'Web Map',
                         'snippet':'This web map copied from template',
                         'tags':'ArcGIS Python API PC Test',
                         'text':json.dumps(web_map_dict)}

    web_map_item = gis.content.add(web_map_properties)
    
    ucipMap = WebMap(web_map_item)
    
    #Find and add relevant View layer and rename 
    layer_search = gis.content.search(query = "UCIP__" + county_name + "_View")
    
    layer = layer_search[0]
    
    print(layer)
    
    ucipMap.add_layer(layer, options={'title': county_name + "View"})
    
    # Check if view layer was added
    print(ucipMap.layers[0])