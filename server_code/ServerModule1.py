import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
import pandas as pd
import csv
import datetime
import random
import time
import matplotlib.pyplot as plt
import anvil.mpl_util
import string
import numpy as np

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
    app_tables.sdg.add_row(id=float(dro[0]), sdgNbr=dro[1], sdg=dro[2], sdg_dt=dro[3])

@anvil.server.callable
def upload_runto_change(data):
  # Delete all rows in the table
  app_tables.runto.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.runto.add_row(id=float(dro[0]), title_used=dro[1], end_year=float(dro[2]), yr_picks=dro[3],
                            end_rowi=float(dro[4]), title_yrs=dro[5], faint_yr=float(dro[6]), tab_color=dro[7])
#    for j in range(0,8):#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))

#id	title_used	end_year	yr_picks	end_rowi	title_years	faint_yr	tab_color
#1	Start of the Game	2025	1990, 2000, 2010, 2020	1121	1990 to 2020	2000	cyan

@anvil.server.callable
def upload_regions_change(data):
  # Delete all rows in the table
  app_tables.regions.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.regions.add_row(id=float(dro[0]), abbreviation=dro[1], name=dro[2], color=dro[3],
                            colhex=dro[4], pyidx=float(dro[5]))
#    for j in range(0,6):#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))
#id	abbreviation	name	color	colhex	pyidx
#1	us	United States	blue	#3349ff	0

@anvil.server.callable
def upload_policies_change(data):
  # Delete all rows in the table
  app_tables.policies.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.policies.add_row(id=float(dro[0]), abbreviation=dro[1], name=dro[2], tltl=float(dro[3]),
                            gl=float(dro[4]), expl=dro[5], ta=dro[6])

@anvil.server.callable
def upload_ministries_change(data):
  # Delete all rows in the table
  app_tables.ministries.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.ministries.add_row(id=float(dro[0]), ministry=dro[1], longname=dro[2])

@anvil.server.callable
def upload_game_info_change(data):
  # Delete all rows in the table
  app_tables.games_info.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.games_info.add_row(id=float(dro[0]), game_id=dro[1], started_on=dro[2], updated=dro[3],
                            closed=dro[4], next_step_p=float(dro[5]), next_step_gm=float(dro[6]), npbhp=dro[7])

@anvil.server.callable
def upload_games_change(data):
  # Delete all rows in the table
  app_tables.games.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.games.add_row(id=float(dro[0]), game_id=dro[1], reg=dro[2], wert=float(dro[3]),
                            runde=float(dro[4]), pol=dro[5], ta=dro[6])

@anvil.server.callable
def start_new_game(cid, npbhpv, next_step_gmv):
  app_tables.games_info.delete_all_rows()
  nn_str = ' '.join(npbhpv)
  jetzt = datetime.datetime.now()
  app_tables.games_info.add_row(game_id=cid , npbhp=nn_str, next_step_gm= next_step_gmv , started_on = jetzt, closed = False) 
  return True, nn_str

def get_games_info_last_row(cid):
  row = app_tables.games_info.get(game_id=cid)
#  print ('in get_games_info_last_row')
#  pp = row['game_id']
  return row
  
def make_list_from_str(npbhp):
  a = npbhp.replace("['", '')
  a = a.replace("']", '')
  a = a.replace("', '", ' ')
  return a.split(' ')
    
@anvil.server.callable
def set_up_role_assignments(game_id, npbhp, regions):
  app_tables.fr2.delete_all_rows()
#  print (game_id)
#  print (npbhp)
  reg = ['us', 'af', 'cn', 'me', 'sa', 'la', 'pa', 'ec', 'eu', 'se']
  tas = ['poverty', 'inequality', 'empowerment', 'food', 'energy', 'future']
  for i in reg:
    for j in tas:
      if i in npbhp:
#        print(i, ' ' + j + ': False')
        free = False
      else:
#        print(i, ' ' + j + ': True')
        free = True
      app_tables.fr2.add_row(free=free, gameID=game_id, region=i, ta=j)



def get_sql(table, col):
  if table == 'regions':
    names = [r[col] for r in app_tables.regions.search()]
  elif table == 'policies':
    names = [r[col] for r in app_tables.policies.search()]
  else:
    print ("ooops - need to add an elif with table name")
  return names

@anvil.server.callable
def set_up_game_db(runde, cid, npbhp):
  if runde == 1:
    app_tables.games.delete_all_rows()
  k = runde
#  print ('in set_up_game_db')
  if not npbhp == '[]':
#    print(npbhp)
    regions = get_sql('regions', 'abbreviation')
#    print(regions)
    policies = get_sql('policies', 'abbreviation')  # read policies as abbreviation
#    print(policies)
    tltl = get_sql('policies', 'tltl')  # read tltl values
#    print(tltl)
    gl = get_sql('policies', 'gl')  # read gl values
#    print(gl)
    ta = get_sql('policies', 'ta')  # read tas as list as long as policies
#    print(ta)
    for i in regions:
      gg = 0
      for j in policies:
#        print(str(k) + ' ' + i + ' ' + j)
        if i in npbhp:  # if this region is not played by human players set a random value
          mymin = tltl[gg]
          mymax = gl[gg]
          myhalf = (mymax - mymin) / 2
          wert = random.uniform(myhalf, mymax)  # random policy value biased towards GL
        else:
          wert = tltl[gg]
        app_tables.games.add_row(game_id=cid, wert=wert, pol=j, runde=k, ta=ta[gg], reg=i)
        gg += 1
  return True, regions

@anvil.server.callable
def get_latest_game():
  row = app_tables.games_info.get(closed=False, next_step_gm=1)
  return row

@anvil.server.callable
def get_roles(cid):
  roles = app_tables.fill_roles.search(game_id=cid)

@anvil.server.callable
def fill_fr2():
  app_tables.fr2.delete_all_rows()
  reg = ['us', 'af', 'cn', 'me', 'sa', 'la', 'pa', 'ec', 'eu', 'se']
  tas = ['poverty', 'inequality', 'empowerment', 'food', 'energy', 'future']
  cid = 'HSAOD-597-628'
  for i in reg:
    for j in tas:
      free_v = random.randint(0, 1)
      if free_v == 0:
        free = False
      else:
        free = True
      app_tables.fr2.add_row(free=free, gameID=cid, region=i, ta=j)

@anvil.server.callable
def get_reg_long_names(which_region):
  row = app_tables.regions.get(abbreviation=which_region)
  reg_long = row['name']
  return reg_long

@anvil.server.callable
def get_ministry_long(which_ministry):
  row = app_tables.ministries.get(mini=which_ministry)
  m_long = row['longname']
  return m_long

def get_play_25():
  pass

def get_reg_x_name_colx(region):
  row = app_tables.regions.get(abbreviation=region)
  regix = row['id']
  long = row['name']
  farbe = row['color']
  return regix, long, farbe

def get_all_vars_for_ta(ta):
  ta_cap = ta.capitalize()
  v_row = app_tables.sdg_vars.search(ta=ta_cap)
  vars = [r['vensim_name'] for r in app_tables.sdg_vars.search(ta=ta_cap)]
  return vars, v_row

def generate_mpl():
  fig = plt.figure()
  x = [1,2,3]  
  y = [2,4,1]  
  plt.plot(x, y)  
  plt.xlabel('x - axis')  
  plt.ylabel('y - axis')  
  plt.title('My first graph!')  
  fig.tight_layout(pad=15)
  return anvil.mpl_util.plot_image()

def read_ch():
  global ch
  with open(data_files['ch.npy']) as ff:
    ch = np.load(ff)
  return ch
  
def read_fcol_in_mdf():
  global fcol_in_mdf
  with open(data_files['fcol_in_mdf.json']) as ff:
    fcol_in_mdf = json.load(ff)
  return fcol_in_mdf

@anvil.server.callable
def fake_it_server(region, single_ta):
  # region as 'nn' single ta as 'poverty', etc
  fcol_in_mdf = read_fcol_in_mdf()
  my_time = time.localtime()
  my_time_formatted = time.strftime("%a %d %b %G", my_time)
  foot1 = 'mov240906 mppy GAME e4a 10reg.mdl'
  cap = foot1 + ' on ' + my_time_formatted
#  mdf = get_play_25()
#  num_rows, num_cols = mdf.shape
# drop first 10 years from 1980 to 1990 to get the spin-up wrinkles out
#  mdf = mdf[321:num_rows, :]
  regidx, long, farbe = get_reg_x_name_colx(region)
  print(region + '  ' + long)
  print('    ' + single_ta)
# get the names of all vars in the current TA / Ministry
  vars_info_l, vars_info_rows = get_all_vars_for_ta(single_ta)
  for var_row in vars_info_rows:
    var_l = var_row['vensim_name']
    print('IN fake_it_server, var_l: '+str(var_l))
    var_l = var_l.replace(" ", "_") # vensim uses underscores not whitespace in variable name
    sdg_name = var_row['sdg_nbr']
    print('IN fake_it_server, sdg_name: '+str(sdg_name))
    sdg_idx = var_row['id']
    print('IN fake_it_server, sdg_idx: '+str(sdg_idx))
    varx = var_row['id']
    print('IN fake_it_server, varx: '+str(varx))
    if varx in[18, 20, 34]: # global variable  
      idx = fcol_in_mdf[var_l] # find location of variable in mdf
    else:
      idx = fcol_in_mdf[var_l] # find location of variable in mdf
    print('IN fake_it_server, idx: ' + str(idx) + ' varl: ' + var_l)

    fig = generate_mpl()
    print(type(fig))
    full_dict = (
      {'title': 'Joe', 'subtitle': 'Latest tech report', 'fig' : fig, 'cap': 'caption'},
      {'title': 'Joe Blow', 'subtitle': 'Grandpa', 'fig' : fig,  'cap': 'caption 2'},
      {'title': 'Joe Blow jr', 'subtitle': 'Son', 'fig' : fig,  'cap': 'caption 23'},
      {'title': 'Joe Blow jr III', 'subtitle': 'Son of a b...', 'fig' : fig,  'cap': 'caption 234'},
    )
#  
#    sdg_idx = vars_info_l.iloc[i,0]
#    varx_list = vars_df.index[vars_df['modelvariable'] == var_l].tolist()
#    varx = varx_list[0] # make an integer
#    print('        ', var_l, ' ', str(varx))
#    if varx in[18, 20, 34]: # global variable
#        var_l = var_l.replace(" ", "_")
#        idx = fcol_in_mdf[var_l]
#        dfv = mdf[:, idx]
#        dfv = dfv[0:end_rowi-1]
    # Define a dictionary containing Students data
#        dfvpd = pd.DataFrame(dfv, columns=['glob'])
#        dfvpd = dfvpd * vars_df.iloc[varx, 12]
#        yr = np.arange(1990, end_yr, 0.03125)
#        dfvpd.insert(loc=0, column='yr', value=yr)
#        yr_py_int = np.int_(yr_py)
#        pvt = np.full((lx, 1), np.nan)  # placeholder for year points
#        for i in range(lx):
#            idx = max(1, yr_py_int.item(i))
#            pvt[i] = dfvpd.iloc[idx-1, 1]
#            fn = folder + region + '-' + str(varx) + '-' + single_ta + '.png'
#            plot_glob_ta_pol(dfvpd, pvt, varx, fn)
#    else: # regional variable
    # vensim uses underscores not whitespace in variable name
#        var_l = var_l.replace(" ", "_")
        # find location of variable in mdf
#        idx = fcol_in_mdf[var_l]
        # get the slice with all regional data for the variable
#        dfv = mdf[:, idx:idx + 10]
        # get the slice of rows
#        dfv = dfv[0:end_rowi - 1, :]
        # make a pd dataframe
#        dfvpd = pd.DataFrame(dfv, columns=my_lab)
        # scale
#        dfvpd = dfvpd * vars_df.iloc[varx, 12]
        # slice out the correct region column#
#        dfvpd = pd.DataFrame(dfvpd.iloc[:, regidx])
        # make a colum with correct time data
#        yr = np.arange(1990, end_yr, 0.03125)
        # put the time in slot 0
#        dfvpd.insert(loc=0, column='yr', value=yr)
        # fig = px.line(d3,x='yr',y='cn')
        # fig.show()
        # prepare the data for the years with thick dots
#        yr_py_int = np.int_(yr_py)
#        pvt = np.full((lx, 1), np.nan)  # placeholder for year points
#        for i in range(lx):
#            idx = max(1, yr_py_int.item(i))
#            pvt[i] = dfvpd.iloc[idx-1, 1]
        # prepare the correct filename
#        lfn = region + '-' + str(varx) + '-' + single_ta + '.png'
#        fn = os.path.join(cwd, folder, lfn)
        # send for plotting
#        plot_each_reg_ta_pol(dfvpd, pvt, varx, fn)
#        plot_each_reg_ta_pol2(dfvpd, pvt, varx, fn)
    fig = generate_mpl()
    print(type(fig))
    full_dict = (
     {'title': 'Joe', 'subtitle': 'Latest tech report', 'fig' : fig, 'cap': 'caption'},
     {'title': 'Joe Blow', 'subtitle': 'Grandpa', 'fig' : fig,  'cap': 'caption 2'},
     {'title': 'Joe Blow jr', 'subtitle': 'Son', 'fig' : fig,  'cap': 'caption 23'},
     {'title': 'Joe Blow jr III', 'subtitle': 'Son of a b...', 'fig' : fig,  'cap': 'caption 234'},
   )
    return full_dict

@anvil.server.callable
def load_plots(region, single_ta):
  # region as 'nn' single ta as 'poverty', etc
  my_time = time.localtime()
  my_time_formatted = time.strftime("%a %d %b %G", my_time)
  foot1 = 'mov240906 mppy GAME e4a 10reg.mdl'
  cap = foot1 + ' on ' + my_time_formatted
#  mdf = get_play_25()
#  num_rows, num_cols = mdf.shape
# drop first 10 years from 1980 to 1990 to get the spin-up wrinkles out
#  mdf = mdf[321:num_rows, :]
  regidx, long, farbe = get_reg_x_name_colx(region)
  print(region + '  ' + long)
  print('    ' + single_ta)
# get the names of all vars in the current TA / Ministry
  vars_info_l = get_all_vars_for_ta(single_ta)
  print('IN load_plots, vars_info_l')
  print(vars_info_l)
  title = 'test title ' + str(random.randint(100,999))
  sub = 'test subtile ' + str(random.randint(100,999))
  fig = 'test fig'
  return title, sub, fig, cap
#  for i in range(len(vars_info_l)):
    # name of the vensim variable
#    var_l = vars_info_l.iloc[i,3]
#    sdg_name = vars_info_l.iloc[i,1]
#    sdg_idx = vars_info_l.iloc[i,0]
#    varx_list = vars_df.index[vars_df['modelvariable'] == var_l].tolist()
#    varx = varx_list[0] # make an integer
#    print('        ', var_l, ' ', str(varx))
#    if varx in[18, 20, 34]: # global variable
#        var_l = var_l.replace(" ", "_")
#        idx = fcol_in_mdf[var_l]
#        dfv = mdf[:, idx]
#        dfv = dfv[0:end_rowi-1]
    # Define a dictionary containing Students data
#        dfvpd = pd.DataFrame(dfv, columns=['glob'])
#        dfvpd = dfvpd * vars_df.iloc[varx, 12]
#        yr = np.arange(1990, end_yr, 0.03125)
#        dfvpd.insert(loc=0, column='yr', value=yr)
#        yr_py_int = np.int_(yr_py)
#        pvt = np.full((lx, 1), np.nan)  # placeholder for year points
#        for i in range(lx):
#            idx = max(1, yr_py_int.item(i))
#            pvt[i] = dfvpd.iloc[idx-1, 1]
#            fn = folder + region + '-' + str(varx) + '-' + single_ta + '.png'
#            plot_glob_ta_pol(dfvpd, pvt, varx, fn)
#    else: # regional variable
    # vensim uses underscores not whitespace in variable name
#        var_l = var_l.replace(" ", "_")
        # find location of variable in mdf
#        idx = fcol_in_mdf[var_l]
        # get the slice with all regional data for the variable
#        dfv = mdf[:, idx:idx + 10]
        # get the slice of rows
#        dfv = dfv[0:end_rowi - 1, :]
        # make a pd dataframe
#        dfvpd = pd.DataFrame(dfv, columns=my_lab)
        # scale
#        dfvpd = dfvpd * vars_df.iloc[varx, 12]
        # slice out the correct region column#
#        dfvpd = pd.DataFrame(dfvpd.iloc[:, regidx])
        # make a colum with correct time data
#        yr = np.arange(1990, end_yr, 0.03125)
        # put the time in slot 0
#        dfvpd.insert(loc=0, column='yr', value=yr)
        # fig = px.line(d3,x='yr',y='cn')
        # fig.show()
        # prepare the data for the years with thick dots
#        yr_py_int = np.int_(yr_py)
#        pvt = np.full((lx, 1), np.nan)  # placeholder for year points
#        for i in range(lx):
#            idx = max(1, yr_py_int.item(i))
#            pvt[i] = dfvpd.iloc[idx-1, 1]
        # prepare the correct filename
#        lfn = region + '-' + str(varx) + '-' + single_ta + '.png'
#        fn = os.path.join(cwd, folder, lfn)
        # send for plotting
#        plot_each_reg_ta_pol(dfvpd, pvt, varx, fn)
#        plot_each_reg_ta_pol2(dfvpd, pvt, varx, fn)

  pass
