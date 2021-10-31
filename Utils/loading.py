import numpy as np
import pandas as pd

def loading(locs, tick=True):

  for i in range(len(locs)):

    df = pd.read_csv(locs[i])

    data = pd.DataFrame(None)

    aux = 1 if tick else 0
  
    data['time'] = pd.to_datetime(df.iloc[:,aux], unit='ms')
    data['price'] = df.iloc[:,4]

    data.to_csv(locs[i])


locations = ['MATICUSDT-1h-2021-02.csv', 'MATICUSDT-1h-2021-03.csv', 'MATICUSDT-1h-2021-04.csv', 'MATICUSDT-1h-2021-05.csv','MATICUSDT-1h-2021-06.csv','MATICUSDT-1h-2021-07.csv'] 
loading(locations, False)
  

