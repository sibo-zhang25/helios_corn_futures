# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 22:52:14 2025

@author: williamz

client scraper to use latitude and longitude information to find
its corresponding climate type according to the Koppen Classification system
"""
import pandas as pd
import requests
import time

geocode = pd.read_csv('./geonames_searchresults.csv',index_col=0)
marketshare = pd.read_csv('./corn_regional_market_share.csv')

dfj = marketshare.merge(geocode,how ='left',right_on=['search_name','country'],\
                        left_on=['region_name','country_name'])

climatetype = dfj.drop_duplicates(subset=marketshare.columns,keep='first',\
              inplace=False).loc[:,['region_id','latitude','longitude']]
## keep first appeared duplicates as differences in latitudes and longitudes
## are negligible


queries = []
for i in range(climatetype.shape[0]):
    row = climatetype.iloc[i]
    if row.isna().sum()==0:
        url = url = 'http://climateapi.scottpinkelman.com/api/v1/'\
                    f'location/{row.latitude}/{row.longitude}'
        r = requests.get(url)
        retvals = r.json()['return_values'][0]
        koppen = retvals['koppen_geiger_zone']
        time.sleep(5)
    else:
        koppen = None
    queries.append(koppen)
    print(f'{i+1} out of {climatetype.shape[0]} complete')
## climate type scraper 
## source: http://climateapi.scottpinkelman.com/

climatetype['koppen_zone'] = queries
climatetype.loc[:,['region_id','koppen_zone']].\
    to_csv('./corn_regional_climate_type.csv',index=False)
## output: region names together with their climate types
