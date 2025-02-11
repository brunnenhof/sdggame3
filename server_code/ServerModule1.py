import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
import pandas as pd
import csv

@anvil.server.callable
def upload_sdg_var_change(data):
  # Delete all rows in the table
  app_tables.sdg_vars.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    d = data[i]
    d = d.replace('\"', '')
    dro = d.split(',')
    for j in range(0,13):
      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))
    
    app_tables.sdg_vars.add_row(sdg_nbr=float(dro[0]), sdg=dro[1], indicator=dro[2], vensim_name=dro[3], green=float(dro[4]), red=float(dro[5]),
                              lowerbetter=float(dro[6]), ymin=float(dro[7]),ymax=float(dro[8]),subtitle=dro[9],ta=dro[10],pct=float(dro[11]), id=float(dro[12]))

def clean_csv(d):
    d = d.replace('\"', '')
    return d.split(',')
  
@anvil.server.callable
def upload_sdg_change(data):
  # Delete all rows in the table
  app_tables.sdg.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    for j in range(0,4):
      app_tables.sdg.add_row(id=float(dro[0]), sdgNbr=dro[1], sdg=dro[2], sdg_dt=dro[3])
#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))

@anvil.server.callable
def upload_runto_change(data):
  # Delete all rows in the table
  app_tables.runto.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    for j in range(0,8):
      app_tables.runto.add_row(id=float(dro[0]), title_used=dro[1], end_year=float(dro[2]), yr_picks=dro[3],
                            end_rowi=float(dro[4]), title_years=dro[5], faint_yr=float(dro[6]), tab_color=dro[7])
#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))

#id	title_used	end_year	yr_picks	end_rowi	title_years	faint_yr	tab_color
#1	Start of the Game	2025	1990, 2000, 2010, 2020	1121	1990 to 2020	2000	cyan


    