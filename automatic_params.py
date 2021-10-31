import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

from hurst import compute_Hc
try:
	import configparser
except ImportError:
	import ConfigParser as configparser

class automatic_param:

  def __init__(self, df_ticks, signals):
    
    self.df_ticks = df_ticks
    self.signals = signals

  def params(self, first_grid_perc):

    for (no, sg) in enumerate(self.signals[:,0:2]):
    
      if sg[0] != None:

        interval = self.df_ticks[(self.df_ticks.time>=sg[0]) & (self.df_ticks.time<=sg[1])]
      
        #print(sg[0],"\n",sg[1],"\n",interval)


        mean = np.mean(interval.price)
        std = np.std(interval.price)

        lower = mean - 3.5*std
        upper = mean + 3.5*std

      

        body = (upper-lower)/lower

        sld = lower * (1 - body/2)
        slu = upper * (1 + body/2)

        firstGrid_and_lower_distance = lower * first_grid_perc

        grid_numbers = max(6, int((upper-lower) / firstGrid_and_lower_distance))
        coeff = 0.2
        trigger = (lower + upper)/2 - coeff * (upper - lower)/grid_numbers

        self.signals[no][3] = lower
        self.signals[no][4] = upper
        self.signals[no][5] = sld
        self.signals[no][6] = slu
        self.signals[no][7] = trigger
        self.signals[no][8] = grid_numbers

    return self.signals
