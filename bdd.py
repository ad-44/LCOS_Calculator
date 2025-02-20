#%% Imports
import pandas as pd
import request

url = "https://github.com/ad-44/LCOS_Calculator/blob/main/bdd/spotprice.csv"
resp = requests.get(url)

#%% Data base creation
rawprices = pd.read_csv(resp,sep=';',header=0,index_col=0)
rawprices.index = range(0,8784)
rawprices = rawprices.astype('float')
rawprices = rawprices.fillna(0)
