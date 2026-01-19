# -*- coding: utf-8 -*-
"""
Created on Sat Jan  3 13:08:57 2026

@author: williamz

function to convert latitude and longitude in degrees, minutes, and seconds 
to decimal degrees

"""
import re

def decimalDegreesConverter(Str):
    p_dir = re.compile("[N,S,W,E]{1}",re.IGNORECASE)
    p_degree = re.compile("[0-9]+(?=[°]{1})")
    p_minute = re.compile("[0-9]+(?=[′]{1})")
    p_second = re.compile("[0-9]+(?=['']{1})")
    ## using re lookahead assertion

    direction = p_dir.search(Str)[0]
    degree = int(p_degree.search(Str)[0])
    minute = int(p_minute.search(Str)[0])
    second = int(p_second.search(Str)[0])
    dd = degree+minute/60+second/3600
    if direction.lower() in ['s','w']:
        return -dd
    else:
        return dd