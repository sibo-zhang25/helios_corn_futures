# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 15:28:55 2026

@author: williamz

Score Evaluation functions for 2025 Helios Climate Risk Competition

"""
import pandas as pd
import numpy as np

def compute_partial_correlations(df,by=['crop_name','country_name','date_on_month']):
    ## df: must be a dataframe with non-zero rows and at least two columns 
    ## each with name starting with climate_risk and futures
    
    ## by: groupby keyword value to partition df to compute partial
    ## correlations of each group
    ## default to groupings shown in Helios sample notebook

    def _climate_futures_corr_table(df,climate_risk_columns,futures_columns):
        ## compute correlations of each climate-futures variable pair
        ## Note: dataframe must contain at least two non-null pairs
        ## to produce a non-null correlation
        
        corr_matrix = df[climate_risk_columns+futures_columns]\
                      .corr(method='pearson',min_periods=2,numeric_only=True)
        ## corr() auto drop nan values before computing
        ## number pairs must be at least two for computation
        ## according to formula
        corr_table = corr_matrix.loc[climate_risk_columns,futures_columns]\
        .rename_axis(index='climate_variable',columns='futures_variable')\
        .stack().reset_index(name='correlation')
        ## drop nan correlations in stack operation
        return corr_table.round(5)

    climate_risk_columns = [c for c in df.columns if c.startswith('climate_risk')]
    futures_columns = [c for c in df.columns if c.startswith('futures')]
    df_default = pd.DataFrame([],columns=['correlation'])
    
    if len(climate_risk_columns)==0:
        print('input dataframe must have at least one column with name starting with climate_risk')
        return df_default
    
    if len(futures_columns)==0:
        print('input dataframe must have at least one column with name starting with futures')
        return df_default
    
    if by==None:
        corr_tables = _climate_futures_corr_table(df,climate_risk_columns,futures_columns)
    else:
        try:
            corr_tables = df.groupby(by=by).apply(_climate_futures_corr_table,\
                                                  climate_risk_columns,\
                                                  futures_columns,\
                                                  include_groups=False
                                                 )
            corr_tables = corr_tables\
                          .reset_index(level=len(corr_tables.index.levels)-1,drop=True)\
                          .reset_index()
            ## compute and combine the correlation table for each group
        except KeyError:
            print('illegal by values')
            return df_default

    return corr_tables


def cfcs(df):
    """
    Calculate the Climate-Futures Correlation Score (CFCS) for leaderboard ranking.
    
    CFCS = (0.5 × Avg_Sig_Corr_Score) + (0.3 × Max_Corr_Score) + (0.2 × Sig_Count_Score)

    Input dataframe must have correlation column for computation
    """

    # Remove null correlations
    valid_corrs = df["correlation"].dropna()
    
    if len(valid_corrs) == 0:
        return {'cfcs_score': 0.0, 'error': 'No valid correlations'}
    
    # Calculate base metrics
    abs_corrs = valid_corrs.abs()
    max_abs_corr = abs_corrs.max()
    significant_corrs = abs_corrs[abs_corrs >= 0.5]
    significant_count = len(significant_corrs)
    total_count = len(valid_corrs)
    
    # Calculate component scores - ONLY average significant correlations
    if significant_count > 0:
        avg_sig_corr = significant_corrs.mean()
        avg_sig_score = min(100, avg_sig_corr * 100)  # Cap at 100 when avg sig reaches 1.0
    else:
        avg_sig_corr = 0.0
        avg_sig_score = 0.0
    
    max_corr_score = min(100, max_abs_corr * 100)  # Cap at 100 when max reaches 1.0
    sig_count_score = (significant_count / total_count) * 100  # Percentage
    
    # Composite score: Focus more on quality of significant correlations
    cfcs = (0.5 * avg_sig_score) + (0.3 * max_corr_score) + (0.2 * sig_count_score)
    scoreboard = {'cfcs_score': cfcs, 'avg_sig_score': avg_sig_score,\
                  'max_corr_score': max_corr_score,\
                  'sig_count_score': sig_count_score
                 }
    print(f'{round(sig_count_score,2)}% of all correlations are significant')
    print(f'Average significant correlation is {round(avg_sig_corr,3)}')
    print(f'highest absolute correlation found is {round(max_abs_corr,3)}')
    print(f'final CFCS score is {round(cfcs,2)}')
    return scoreboard


def sigcorr_report(df,features='climate_variable',sig_level=0.5):
    '''
        Generate a CFCS sub scores report for each feature
        with significant correlations.
        
        Input dataframe must contain a correlation column and feature columns.
    
    '''
    df = df.copy()
    df['correlation_abs'] = df.correlation.abs()
    try:
        df.loc[df['correlation_abs']<=sig_level,['correlation_abs']] = np.nan
        reportdf = df.groupby(features).agg({'correlation_abs':['mean','max','count'],\
                                       'correlation':'count'\
                                      })
        ## compute CFCS score components for each feature
    except TypeError:
        print('sig_level must be a number between 0 and 1')
        return None
    except KeyError:
        print('illegal features values')
        return None
        
    reportdf.columns = ['avg_sig_corr','max_sig_corr','sig_corr_count','total_corr_count']
    reportdf['sig_corr_ratio(%)'] = 100*reportdf['sig_corr_count']/reportdf['total_corr_count']
    reportdf = reportdf[reportdf['avg_sig_corr'].notnull()]\
               .loc[:,['avg_sig_corr','max_sig_corr','sig_corr_count','sig_corr_ratio(%)']]\
               .round(3)
    ## features without any significant correlation are not reported
    return reportdf









