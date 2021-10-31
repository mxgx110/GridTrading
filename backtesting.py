import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

from hurst import compute_Hc
try:
	import configparser
except ImportError:
	import ConfigParser as configparser


def backtest(tickfilelocation, candlesfilelocation, cfgfile):


  load_df = pd.read_csv(tickfilelocation)
  df_tick  = pd.DataFrame(None)
  df_tick ['time'] = load_df.iloc[:,-2]
  df_tick ['price'] = load_df.iloc[:,-1]


  load_df = pd.read_csv(candlesfilelocation)
  df = pd.DataFrame(None)
  df ['time'] = load_df.iloc[:,-2]
  df ['price'] = load_df.iloc[:,-1]



  strg = strategy(df)
  signals = strg.SGN()
 

  aut = automatic_param(df_tick, signals)
  completed_signals = aut.params(0.03)
  print(completed_signals)
  
  for i in range(len(completed_signals)):
  
    try:

      bot = GTBOT(df_tick, completed_signals[i],cfgfile)

      bot.forward()

      sleep(5)
      
    except:
    
      pass
    
"""
tick =  "PATH TO TICK DATA.csv"
candles = "PATH TO CANDLES DATA CORRESPONDING TO PROVIDED TICK DATA.csv"
cfg = "PATH TO CONFIGE FILE.cfg"

backtest(tickfilelocation=tick, candlesfilelocation=candles, cfgfile=cfg)
"""

