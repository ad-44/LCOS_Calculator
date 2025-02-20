#%% Imports
import pandas as pd

#%% Data base creation
url = (r'https://raw.githubusercontent.com/ad-44/LCOS_Calculator/main/bdd/spotprice.csv')

rawprices = pd.read_csv(url,sep=';',header=0,index_col=0)
rawprices.index = range(0,8784)
rawprices = rawprices.astype('float')
rawprices = rawprices.fillna(0)
