import pandas as pd
import numpy as np
def concatenate_(locs:list, filename):

  df = pd.read_csv(locs[0])

  for i in range(1, len(locs)):

    df_new = pd.read_csv(locs[i ])

    df = pd.concat([df, df_new])

  df = df[['time', 'price']]
  df.index = np.array(range(len(df)))

  df.to_csv(filename)
  
  
locations = ['MATICUSDT-1h-2021-02.csv', 'MATICUSDT-1h-2021-03.csv', 'MATICUSDT-1h-2021-04.csv', 'MATICUSDT-1h-2021-05.csv','MATICUSDT-1h-2021-06.csv','MATICUSDT-1h-2021-07.csv']

filename = "SixmonthsCandles1h.csv"

concatenate_(locations, filename)

