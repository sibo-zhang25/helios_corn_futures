# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 16:15:30 2026

@author: williamz
"""
import pandas as pd

geocode = pd.read_csv('./geonames_searchresults.csv',index_col=0)
marketshare = pd.read_csv('./corn_regional_market_share.csv')

dfj = marketshare.merge(geocode,how ='left',right_on=['search_name','country'],\
                        left_on=['region_name','country_name'])

dfj.drop_duplicates(subset=marketshare.columns,keep='first',\
              inplace=True)
dfj['hemisphere'] = dfj.latitude.transform(lambda x: 'S' if x<0 else \
                       ('N_1' if x<=23.43591 else 'N_2'))

dfj.loc[:,['region_id','hemisphere']].to_csv('./corn_regional_hemisphere.csv',\
                                             index=False)