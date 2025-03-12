#%% Imports
import pandas as pd

#%% Data base creation
url_spot = (r'https://raw.githubusercontent.com/ad-44/LCOS_Calculator/main/bdd/spotprice.csv')

rawprices = pd.read_csv(url_spot, sep=';', header=0, index_col=0)
rawprices.index = range(0,8784)
rawprices = rawprices.astype('float')
rawprices = rawprices.fillna(0)

url_gm = (r'https://raw.githubusercontent.com/ad-44/LCOS_Calculator/main/bdd/GM_data.csv')

rawGM = pd.read_csv(url_gm, sep=';', header=0, index_col=0)
rawGM = rawGM.fillna(0)
