from os import walk
import numpy as np
import pandas as pd
def aggregate(parentFileLocation, agg_report_file_name):

  UPNL = []
  TPNL = []
  SLTL = []
  NPNL = []
  DURATION = []

  f = []
  counter = 0
  for (dirpath, dirnames, filenames) in walk(parentFileLocation):
      f.extend(filenames)
      break

  for filepath in f:

    with open(f'{parentFileLocation}{filepath}', "r") as report:

      content = report.read()

      try:

        start = pd.to_datetime(content.split('start:')[1].split('\n')[0])
        end = pd.to_datetime(content.split('end:')[1].split('\n')[0])
        duration = end-start
        try:
          upnl = float(content.split('Unrealized PNL : ')[1].split('\n')[0])
        except:
          upnl = 0.0
        tpnl = float(content.split('Total PNL : ')[1].split('\n')[0])
        sltl = float(content.split('SL touch loss : ')[1].split('\n')[0])
        npnl = float(content.split('Net PNL : ')[1].split('\n')[0])

        UPNL.append(upnl)
        TPNL.append(tpnl)
        SLTL.append(sltl)
        NPNL.append(npnl)
        DURATION.append(duration)


      except:

        counter += 1

    report.close()

  sum_upnl = np.sum(np.array(UPNL))
  sum_tpnl = np.sum(np.array(TPNL))
  sum_sltl = np.sum(np.array(SLTL))
  sum_npnl = np.sum(np.array(NPNL))
  sum_dur =  np.sum(np.array(DURATION))

  with open(f'{parentFileLocation}{agg_report_file_name}','w') as agg_report:

    agg_report.write(f'\nThis Report belongs to : {agg_report_file_name}\n')
    agg_report.write(f'Overall Duration : {sum_dur}\n')
    agg_report.write(f'\n-------------------------------------------------------\n')
    agg_report.write(f'Aggregated Unrealized PNLs : {sum_upnl}\n')
    agg_report.write(f'Aggregated Total PNLs : {sum_tpnl}\n')
    agg_report.write(f'Aggregated SL Losses : {sum_sltl}\n')
    agg_report.write(f'Aggregated Net PNLs : {sum_npnl}\n')
    agg_report.write(f'-------------------------------------------------------\n\n')
    agg_report.write(f'There are {counter} files in which the trigger price has not been touched.')

    agg_report.close()
    
    
  print('Done, Go Nuts...')

aggregate("MATICUSDT234/", "MATICUSDTP_REP.txt")



