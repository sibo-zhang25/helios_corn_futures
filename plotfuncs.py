# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 20:24:19 2025

@author: williamz
"""
from matplotlib import pyplot as plt

def barplots(data,seperator,x,y):
    '''
    parameters: 
    data:pandas Dataframe instance 
    seperator:str,column name in data used to seperate plots
    x: str, column name in data that gives height of each plot
    y: str, column name in data that gives categories of each plot
    '''
    seps = data[seperator].unique()
    gridsize = _gridsizefinder(seps.size)
    ## an algo to auto-set number of rows
    ## and columns in the figure 
    nrows = gridsize[0]
    ncols = gridsize[1]
    width = ncols*6.4
    height = (nrows+1)*4.8
    ## default figsize is (6.4,4.8) according to Matplotlib doc
    
    fig,axs = plt.subplots(nrows,ncols,\
                           figsize=(width,height))
    
    count = 0
    for i in range(nrows):
        for j in range(ncols):
            ax = axs[i,j]
            name = seps[count]
            subdata = data[data[seperator]==name]
            ax.barh(y = subdata[y],width=subdata[x],color='orange');
            ## minimize colour variety to maintain clarity
            ## favor horizontal over vertical barchart due to 
            ## reading habits
            ax.legend(labels = [name]);
            
            ax.set_frame_on(False)
            ax.tick_params(axis='y',length=0)
            ## eliminiate unnecessary lines per Knaflic's ideas
        
            count+=1
            if count==seps.size:
                break
            else:
                continue
        if count==seps.size:
            break
        else:
            continue
        
def _gridsizefinder(n):
    ## find all integer factor pairs of n
    factorpairs=[]
    for i in range(2,int(n/2)):
        if n%i==0:
            factorpairs.append((i,int(n/i)))
        else:
            continue
    ## if n is a prime number, try n+1
    ## this will happen once because n+1
    ## is an even number if n is prime
    if len(factorpairs)==0:
        return _gridsizefinder(n+1)
    elif len(factorpairs)>1:
        ## find the pair with minimal abs difference
        diff = []
        for pair in factorpairs:
            diff.append(abs(pair[0]-pair[1]))
        return factorpairs[diff.index(min(diff))]
    else:
        return factorpairs  

    