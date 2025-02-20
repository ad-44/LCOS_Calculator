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

"""
raw_2014 = rawprices['2014'].iloc[:-24]
raw_2014 = raw_2014.astype('float')
raw_2014 = raw_2014.fillna(0)

raw_2015 = rawprices['2015'].iloc[:-24]
raw_2015 = raw_2015.astype('float')
raw_2015 = raw_2015.fillna(0)

raw_2016 = rawprices['2016']
raw_2016 = raw_2016.astype('float')
raw_2016 = raw_2016.fillna(0)

raw_2017 = rawprices['2017'].iloc[:-24]
raw_2017 = raw_2017.astype('float')
raw_2017 = raw_2017.fillna(0)

raw_2018 = rawprices['2018'].iloc[:-24]
raw_2018 = raw_2018.astype('float')
raw_2018 = raw_2018.fillna(0)

raw_2019 = rawprices['2019'].iloc[:-24]
raw_2019 = raw_2019.astype('float')
raw_2019 = raw_2019.fillna(0)

raw_2020 = rawprices['2020']
raw_2020 = raw_2020.astype('float')
raw_2020 = raw_2020.fillna(0)

raw_2021 = rawprices['2021'].iloc[:-24]
raw_2021 = raw_2021.astype('float')
raw_2021 = raw_2021.fillna(0)

raw_2022 = rawprices['2022'].iloc[:-24]
raw_2022 = raw_2022.astype('float')
raw_2022 = raw_2022.fillna(0)

raw_2023 = rawprices['2023'].iloc[:-24]
raw_2023 = raw_2023.astype('float')
raw_2023 = raw_2023.fillna(0)
"""

"""
 if spot_year != None:
     index_hours = pd.date_range(spot_year+"-01-01",spot_year+"-12-31",freq='h').tolist()
     if spot_year == '2014':
         spot_data = raw_2014
     elif spot_year == '2015':
         spot_data = raw_2015
     elif spot_year == '2016':
         spot_data = raw_2016
     elif spot_year == '2017':
         spot_data = raw_2017
     elif spot_year == '2018':
         spot_data = raw_2018
     elif spot_year == '2019':
         spot_data = raw_2019
     elif spot_year == '2020':
         spot_data = raw_2020
     elif spot_year == '2021':
         spot_data = raw_2021
     elif spot_year == '2022':
         spot_data = raw_2022
     elif spot_year == '2023':
         spot_data = raw_2023
 else:
     pass
"""