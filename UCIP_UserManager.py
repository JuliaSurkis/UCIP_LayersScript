# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 14:50:09 2021

@author: jsurkis
"""

from arcgis.gis import GIS
from arcgis.gis import ContentManager
from arcgis.features import FeatureLayerCollection
import arcgis
# import os, sys
# import time
import getpass
# import requests
# import random
import arcpy

# Set variables, get AGOL username and password
portal_url = arcpy.GetActivePortalURL()
print(portal_url)

user = getpass.getpass(prompt='    Enter arcgis.com username:\n')
pw = getpass.getpass(prompt='    Enter arcgis.com password:\n')
arcpy.SignInToPortal(portal_url, user, pw)

my_agol = GIS(portal_url, user, pw)

del pw

#get layer with jurisdiction polygons
counties_munis = my_agol.content.get('c29faaea33da4cb680bf4a0e6a676732').layers[0].query()

#loop through each jurisdiction to create a group and add users for each
for index, county in enumerate(counties_munis):
    county_name = counties_munis.features[index].attributes['NAME']
    print(county_name)
    group_name = county_name + "_Group"
    create_group = my_agol.groups.create(title=group_name,
                                    tags = 'UCIP, Critical Infrastructure, Utah, Emergency Management',
                                    description = 'Group for access to critical infrastructure within ' + county_name,
                                    access = 'org',
                                    is_invitation_only = 'True')
    create_group
    
    #Make sure jurisdiction layer is accessible to the group
    layer_search = my_agol.content.search(query = "UCIP__" + county_name + "_View")
    layer = layer_search[0]
    layer.share(groups = create_group)
    
    #Make sure the jurisdiction map is accessible to the group
    mapname = "UCIP_" + county_name + "120621_Final"
    map_search = my_agol.content.search(query = 'title:'"UCIP_" + county_name + "_120621_Final")
    map_result = map_search[0]
    map_result.share(groups = create_group)
    
    #Add assessors by looping through assessor table and checking that their jurisdiction mathces
    #the jurisdiction for the group that was just created. If it does match, either create or 
    #add the user based on their email.
    assessor_table = ****
    for index, i in enumerate(assessors):
        admin_email = assessor_table.features[index].attributes['email']
        admin_firstname = assessor_name.features[index].attributes['firstname']
        admin_lastname = assessor_name.features[index].attributes['lastname']
        admin_jurisdiction = assessor_name.features[index].attributes['jurisdiction']
        if admin_jurisdiction == county_name:
            if my_agol.users.search(query = 'email=admin_email') is None:
                new_user = my_agol.users.create(username = admin_firstname+adminlastname, password = 'Password123', firstname = admin_firstname,
                                lastname = admin_lastname, email = admin_email, provider = 'enterprise',usertype = 'editor')
                new_user
                username = new_user[username]
                create_group.add_users(username)
            else: 
                create_group.add_users(my_agol.users.search(query = 'email=admin_email')[username])
        else:
            continue
