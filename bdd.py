# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:43:34 2025

@author: debille-a-1
"""
#%% Imports
import pandas as pd

#%% Data base creation

rawprices = pd.read_csv(r'bdd\spotprice.csv',sep=';',header=0,index_col=0)
rawprices.index = range(0,8784)
rawprices = rawprices.astype('float')
rawprices = rawprices.fillna(0)
