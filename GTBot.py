import pandas as pd
import numpy as np
from time import sleep
import matplotlib.pyplot as plt

from hurst import compute_Hc
try:
	import configparser
except ImportError:
	import ConfigParser as configparser

class GTBOT:

    def __init__(self, df, signals, cfg_file):

        self.df = df
        self.signals = signals
        self.grid = {}
        self.pending_orders = {}
        self.open_positions = {}
        self.position_size = {}
        self.completed_orders = []
        self.memory = []
        self.cfg_file = cfg_file

    def set_parameters(self):

        config = configparser.RawConfigParser()
        config.read(self.cfg_file)
        
        self.asset = config.get("market", "asset")
        name_one = str(self.signals[1]).split(" ")[0]
        name_two = str(self.signals[2]).split(" ")[0]

        self.f = open(f"{self.asset}_{name_one}_{name_two}.txt","w+")
        self.initial_margin= float(config.get("market", "InitialMargin"))
        self.f.write(f"initial margin:{self.initial_margin}\n")

        self.leverage= int(config.get("market", "Leverage"))
        self.f.write(f"leverage:{self.leverage}\n")

        self.fee_coef = float(config.get("market","fee_coef"))
        self.f.write(f"fee_coef:{self.fee_coef}\n")

        self.market_fee_coef = float(config.get("market","market_fee_coef"))
        self.f.write(f"market_fee_coef:{self.market_fee_coef}\n")

        self.adjust_coef = float(config.get("market","adjust_coef"))
        self.f.write(f"adjust_coef:{self.adjust_coef}\n")

        self.minQTY = float(config.get("market","minQTY"))
        self.f.write(f"minQTY:{self.minQTY}\n")

        self.type = config.get("grid", "grid_type")
        self.f.write(f"type:{self.type}\n")

        self.strategy = config.get("grid", "strategy")
        self.f.write(f"strategy:{self.strategy}\n")

        self.start = self.signals[1]
        self.end = self.signals[2]
        self.df = self.df[(self.df.time>=self.start) & (self.df.time<=self.end)]
        self.df.index = range(0, len(self.df))

        self.lower = self.signals[3] #float(config.get("grid", "lower"))
        self.f.write(f"lower:{self.lower}\n")

        self.upper = self.signals[4] #float(config.get("grid", "upper"))
        self.f.write(f"upper:{self.upper}\n")

        self.SLD = self.signals[5] #float(config.get("grid","SLD"))
        self.f.write(f"SLD:{self.SLD}\n")

        self.SLU = self.signals[6] #float(config.get("grid","SLU"))
        self.f.write(f"SLU:{self.SLU}\n")

        self.trigger = self.signals[7] #float(config.get("grid","trigger"))
        self.f.write(f"trigger:{self.trigger}\n")
        
        self.level = self.signals[8] #int(config.get("grid", "grid_level"))
        self.f.write(f"level:{self.level}\n")
        

        self.f.write(f"---------------------------------------------------\n")
        
        


        if self.leverage > 125:

          print("Maximum leverage available is 125")

          exit()

        if self.level > 149 or self.level < 2:

          print("Level is not in range")

          exit()

        if self.type == "A":

          sum = (self.lower + self.upper) * (self.level + 1) * 0.5

        elif type == "G":

          q = (self.upper / self.lower) ** (1/level)

          sum = (self.lower * (q ** (self.level + 1) - 1)) / (q-1)

        else:

          print("Invalid Input...")

          exit()
        
        self.min_initial_margin = (self.minQTY * sum) / (self.leverage * self.adjust_coef) 

        self.candidateQTY = ((self.adjust_coef * self.initial_margin * self.leverage) / sum)

        QTY = int(self.candidateQTY / self.minQTY) * self.minQTY
        

        # print(min_initial_margin, candidateQTY, QTY, sum)

        if self.initial_margin < self.min_initial_margin:

          print(f"Minimum initial margin required is {self.min_initial_margin}")

          exit()

        else:

          self.qty = QTY

        if self.trigger != 0.0:

          first_trigger_touch = self.df[(self.df.price>=self.trigger) & (self.df.price.shift(1)<self.trigger)].index.min()
          self.df = self.df.iloc[first_trigger_touch-1:,:]

        else:
          

          self.trigger = self.df.loc[self.df.index[0],'price']

        self.f.write(f"start:{self.df.loc[self.df.index[0],'time']}\n")
        self.f.write(f"end:{self.df.loc[self.df.index[-1],'time']}\n")


    def setting(self):

        self.grid['lower'] = self.lower

        if self.type == "A":
            
            price_difference = (self.upper - self.lower) / self.level
            
            for gr in range(self.level-1):

                self.grid[f"grid_{gr+1}"] = self.lower + (gr+1)*price_difference 

        elif self.type == "G":

            price_difference = (self.upper/self.lower) ** (1/self.level)

            for gr in range(self.level - 1):

                self.grid[f"grid_{gr+1}"] = self.lower * (price_difference**(gr+1))

        else:

            print("Invalid Input...")
            exit()

        self.grid['upper'] = self.upper
        

    def grid_labeling(self):

        if self.strategy == "S":

            for k in self.grid.keys():

                self.pending_orders[k] = "S"
                self.position_size[k] = self.grid[k] * self.qty
                self.open_positions[k] = []

        elif self.strategy == "L":
            
            for k in self.grid.keys():

                self.pending_orders[k] = "L"
                self.position_size[k] = self.grid[k] * self.qty
                self.open_positions[k] = []

        elif self.strategy == "N":

            for k in self.grid.keys():

                if self.grid[k] <= self.trigger:

                    self.pending_orders[k] = "L"
                    self.position_size[k] = self.grid[k] * self.qty
                    self.open_positions[k] = []

                else:

                    self.pending_orders[k] = "S"
                    self.position_size[k] = self.grid[k] * self.qty
                    self.open_positions[k] = []

        else:

            print("Invalid Input...")
            exit()
        #print(self.grid)
    
    def updating(self, grid):

        #print(self.pending_orders)

        for g in self.pending_orders.keys():

            if self.grid[g] < self.grid[grid]: self.pending_orders[g] = "L"
            elif self.grid[g] == self.grid[grid]: self.pending_orders[g] = " "
            else: self.pending_orders[g] = "S"
        #print(self.pending_orders)
        print('\n')

    def terminate(self, price_index, manual = False):

      if  manual:

        print("Manually terminated...")
        #CODE ...
        return False

      elif (self.df.price[price_index] <= self.SLD):

        loss = 0

        for el in self.memory:

          grid = el[0]

          loss += (self.grid[grid] - self.SLD) * self.qty + self.position_size[grid] * self.market_fee_coef

        print("SLD has been touched...")

        self.total_pnl(loss)

        return False

      elif (self.df.price[price_index] >= self.SLU): 
        print(self.df.price[price_index], self.df.time[price_index])

        loss = 0

        for el in self.memory:

          grid = el[0]

          loss += (self.SLU - self.grid[grid]) * self.qty + self.position_size[grid] * self.market_fee_coef

        print("SLU has been touched...")

        self.total_pnl(loss)

        return False

      else:

        return True

    def execution_check(self):

      recent_position = self.memory[-1]
      
      for idx in range(len(self.memory) - 2, -1, -1):

        pre_position = self.memory[idx]

        if recent_position[1] != pre_position[1]:

          self.completed_orders.append([pre_position[0], pre_position[1]])

          self.PNL(recent_position[0], pre_position[0], pre_position[1])

          self.open_positions[pre_position[0]].remove((pre_position[1], pre_position[2]))

          self.open_positions[recent_position[0]].remove((recent_position[1], recent_position[2]))

          self.memory.remove(pre_position)

          self.memory.remove(recent_position)

          break

    def PNL(self, fg, sg, type):

      if type == "S":

        pnl = (self.grid[sg] - self.grid[fg]) * self.qty - (self.position_size[sg] * self.fee_coef + self.position_size[fg] * self.fee_coef)

      else:

        pnl = (self.grid[fg] - self.grid[sg]) * self.qty - (self.position_size[sg] * self.fee_coef + self.position_size[fg] * self.fee_coef)

      self.completed_orders[-1].append(pnl)

    def total_pnl(self, loss, check = False):
      

      grids_sum = 0
      
      
      for x in self.completed_orders: 

        grids_sum += x[-1]
          
        
      aux_grids_sum = grids_sum
      
      if loss == 0 and check:

        grids_sum += self.upnl

        print(f"Unrealized PNL : {self.upnl}")
        self.f.write(f"---------------------------------------------------\n")
        self.f.write(f"Unrealized PNL : {self.upnl}\n")

      print(f"Total PNL : {aux_grids_sum}")
      self.f.write(f"Total PNL : {aux_grids_sum}\n")

      print(f"SL touch loss : {loss}")
      self.f.write(f"SL touch loss : {loss}\n")

      print(f"Net PNL : {grids_sum - loss}")
      self.f.write(f"Net PNL : {grids_sum - loss}\n")

      

    def unrealized_pnl(self):

      self.upnl = 0

      for gr in self.open_positions.keys():

        if len(self.open_positions[gr]) > 0:

          if self.grid[gr] >= self.df.loc[self.df.index[-1],'price']:

            if self.open_positions[gr][0][0] == "L":

              sign=-1
            else:

              sign=+1
              
            self.upnl += (sign * abs(self.grid[gr] - self.df.loc[self.df.index[-1],'price'])) * self.qty

          else:

            if self.open_positions[gr][0][0] == "L":
              sign=+1

            else:

              sign=-1

            self.upnl += (sign * abs(self.grid[gr] - self.df.loc[self.df.index[-1],'price'])) * self.qty

    def body(self):
        
        self.f.write(f"grids' prices:{self.grid}\n\n\n\n")


        self.counters = {"S" : 0, "L" : 0}
        
        for i in self.df.index[1:]:

          counter = 0

          result = self.terminate(i)

          if not result:break
             
          for g in self.grid.keys():

              if (self.df.loc[i-1, "price"] < self.grid[g] and self.df.loc[i, "price"] >= self.grid[g]) or (self.df.loc[i-1, "price"] > self.grid[g] and self.df.loc[i, "price"] <= self.grid[g]):
              
                  if self.pending_orders[g] != " " and counter == 0:
                  
                    print(self.df.loc[i, "time"])
                    print(self.grid[g])
                    self.f.write(f"triggered grid's price:{self.grid[g]}\n")
                    self.f.write(f"triggered grid's price:{self.df.loc[i, 'time']}\n")

                    counter +=1

                    self.counters[self.pending_orders[g]] += 1

                    self.open_positions[g].append((self.pending_orders[g], self.counters[self.pending_orders[g]]))
                    
                    self.memory.append((g,self.pending_orders[g], self.counters[self.pending_orders[g]]))

                    print(self.memory)

                    self.f.write(f"memory:{self.memory}\n")
                    self.f.write(f"---------------------------------------------------\n")
                    
                    self.execution_check()

                    self.updating(g)

        if result: 

          self.unrealized_pnl()

          self.total_pnl(0, True)
        self.f.write(f"completed orders:{self.completed_orders}\n")
        self.f.close()

          

    def forward(self):

      self.set_parameters()
      self.setting()
      self.grid_labeling()
      print(self.grid)
      print(f"qty:{self.qty}")
      self.body()
