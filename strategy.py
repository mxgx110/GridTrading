import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

from hurst import compute_Hc
try:
	import configparser
except ImportError:
	import ConfigParser as configparser

class strategy:

  def __init__(self, df_candles):

    self.df_candles = df_candles

  def hurst_exp(self ,N):

    hurst = []

    for _ in range(N):

      hurst.append(1)
  
    for i in range(len(self.df_candles)-N):


      ymin = np.min(self.df_candles.loc[self.df_candles.index[i]:self.df_candles.index[i+N],'price'])
      
      ymax = np.max(self.df_candles.loc[self.df_candles.index[i]:self.df_candles.index[i+N],'price'])


      yscl = ymax - ymin

      lngth = 0

      if N < 2 or ymin == ymax:

        lngth = 1

      else:

        lngth = 0.0

        dx2 = 1.0 / (N * N)

        for j in range(1, N):

          dy = (self.df_candles.price[i + j] - self.df_candles.price[i + j - 1]) / yscl

          lngth = lngth + np.sqrt(dx2 + (dy * dy))

      FDI = 1 + (np.log(lngth) + np.log(2)) / np.log(2*N)
      HURST = 2 - FDI
      hurst.append(HURST)

    self.df_candles['hurst'] = hurst
    self.df_candles.dropna(inplace=True)
    self.df_candles.index = range(0, len(self.df_candles))
    

  def events(self, threshold:float = 0.5)->list:

    signals = []
    in_event = False

    for i in range(1, len(self.df_candles)-1):

      if self.df_candles.hurst[i-1]>threshold and self.df_candles.hurst[i]<=threshold and (not in_event):

        start = self.df_candles.time[i]

        in_event = True

      elif self.df_candles.hurst[i-1]<threshold and self.df_candles.hurst[i]>=threshold and in_event:

        end = self.df_candles.time[i]
        
        signals.append([None, start, end, None, None, None, None, None, None])
        in_event = False

      else:

        pass

    return np.array(signals)

  def SGN(self):

    self.hurst_exp(30)
    self.signals = self.events(0.5)
    self.lookback = self.events(0.55)[:,1]


    for (co,st) in enumerate(self.signals[:,1]):
    
      try:

        pot = self.lookback[self.lookback < st].max()
        self.signals[co][0] = pot
        
      except:
       
        print("What a chance!!! The first hurst cross under takes place so soon that there is no earlier time to calculate parameteres...")

    return self.signals
