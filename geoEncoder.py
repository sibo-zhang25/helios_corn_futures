# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 20:16:15 2025

@author: williamz
client file to use GNSearch to scrape geo location information
for each region in the corn_regional_market_share file 
"""
import pandas as pd
from gnsearch import GNSearch
from decimalDegreesConverter import decimalDegreesConverter as ddc

marketshare = pd.read_csv('./corn_regional_market_share.csv')
## input: names of region in interest

queries = list(marketshare.groupby(['region_name','country_code']).count().index)
result = pd.DataFrame([])
for query in queries:
    region_name = query[0]
    country_code = query[1]
    df = GNSearch(region_name,country_code=country_code)
    ## use GNSearch function to query results from GeoNames database
    result = pd.concat([result,df],axis=0,ignore_index=True)
## EU is not a valid country_code

result['latitude']  = result.lat.map(lambda x: ddc(x))
result['longitude']  = result.long.map(lambda x: ddc(x))
## convert string lat and long values to decimal degrees

result.reset_index(drop=True).to_csv('./geonames_searchresults.csv')
## output: regional names with their corresponding geo location information








