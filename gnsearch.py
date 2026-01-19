# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 16:42:36 2025

@author: williamz
"""
'''
A function to retrieve first fifty queries from
GeoNames database with location name and country code.

Note that:
- country code should follow ISO 3166-1 alpha-2 format.
- featureClass should be a one Letter string in the 
  encoding dictionary below.

GeoNames database official website:    
https://www.geonames.org/

'''

'''
featureClass encoding dictionary:
A: country, state, region,...
H: stream, lake, ...
L: parks,area, ...
P: city, village,...
R: road, railroad
S: spot, building, farm
T: mountain,hill,rock,...
U: undersea
V: forest,heath,...
'''
import requests
import pandas as pd
from bs4 import BeautifulSoup

def GNSearch(search_name,country_code='',featureClass = ''):
    
    if (isinstance(search_name,str) is False) or \
       (isinstance(country_code,str) is False):
           print('parameters must all be of string type')
           return None

    q = search_name.replace(' ','+')
    url = f"https://www.geonames.org/advanced-search.html?q={q}"\
          f"&country={country_code}&featureClass={featureClass}&startRow=0"
    ## note this only return first fifty results.
    ## To add more results, increment startRow parameter
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'lxml')
    
    invalidCountryCode = soup.find('div',class_="formTemplateClass")
    if invalidCountryCode is not None:
        msg = invalidCountryCode.string.replace('\n',' ')+country_code
        print(msg)
        return None

    table = soup.find('div',id='search').form.next_sibling.next_sibling
    if table is None:
        print(f'We have found no places with the name {search_name}.')
        return None
    
    trs = table.select('tr')
    rows = trs[2:-1]
    queries = []
    for row in rows:
        cells  = row.select('td')
        try:
            index = cells[0].small.string
        except AttributeError:
            index = ''
            print('cannot find index in:\n'+str(cells[0]))
        
        try:
            name = cells[1].a.string
        except AttributeError:
            name = ''
            print('cannot find name in:\n'+str(cells[1]))
        
        try:
            country = cells[2].a.string
        except AttributeError:
            country = ''
            print('cannot find country in:\n'+str(cells[2]))
        
        try:
            feature_class = cells[3].contents[0]
        except AttributeError:
            feature_class = ''
            print('cannot find feature class in:\n'+str(cells[3]))
        
        try:
            lat = cells[4].string
        except AttributeError:
            lat = ''
            print('cannot find latitude in:\n'+str(cells[4]))  
        
        try:
            long = cells[5].string 
        except AttributeError:
            long = ''
            print('cannot find longitutde in:\n'+str(cells[5]))        
        
        queries.append([index,name,search_name,country,feature_class,lat,long])
        
    result = pd.DataFrame(queries,columns=['index','name','search_name',\
                                           'country','feature_class','lat',\
                                           'long']).set_index('index')
    return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    