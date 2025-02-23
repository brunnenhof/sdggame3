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
import pickle

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
  long = row['name']
  farbe = row['color']
  return long, farbe

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

def read_mdf25():
  global mdf
  with open(data_files['mdf25.json']) as ff:
    mdf_read = json.load(ff)
    mdf = np.array(mdf_read)
  return mdf

def pickOLD(ys, x, y):
  o = []
  for i in range(0, len(ys)):
    y_in_range = ys[i]
    idx = np.where(x == y_in_range)[0]
    lo = y[idx]
    o.append(lo[0])
  return o

def pick(ys, x, y):
    o = []
    ys_len = len(ys)
    ys_cnt = 0
    ys_check = ys[ys_cnt]
    for i in range(0, len(x)):
        if ys_check == x[i]:
            o.append(y[i])
            ys_cnt += 1
            if ys_cnt == ys_len:
                ys_check = 1952
            else:
                ys_check = ys[ys_cnt]
        else:
            o.append(np.nan)
    return o

  
def make_pngOLD(df, row, pyidx, end_yr):
  fig = plt.figure()
  x = df[:, 0]
  y = df[:, 1]  
  data_max = y.max() * 1.1
  data_min = y.min()
  plot_max = row['ymax']
  plot_min = row['ymin']
  ymin = min(data_min, plot_min)
  ymax = max(data_max, plot_max)
  if ymin > 0:
    ymin = 0
  if ymax < 0:
    ymax = 0
  if int(row['id']) in [26, 4]:  # Labour share of GDP | life expectancy
    ymin = plot_min # red min
  if int(row['id']) in [25,31]: # population | Nitrogen use
    ymax = data_max
  dt = 1 / 32  # = 0.03125
  abc = app_tables.regions.get(pyidx=pyidx)
  my_colhex = abc['colhex']
  my_lab = abc['name']
  plt.plot(x, y, color=my_colhex, linewidth=2.5, label=my_lab)
  # now plot the thick dots
  # get the year picks
  runto_row = app_tables.runto.get(end_year=end_yr)
  yr_picks_str = runto_row['yr_picks']
  yps = yr_picks_str.replace("'", "")
  yr_picks = yps.split(' ')
  yps_int = []
  for i in range(0,len(yr_picks)):
    yps_int.append(int(yr_picks[i]))
  print ('IN make_png yr_picks: ')
  pvt_len = len(yr_picks)
  ys = pick(yps_int, x, y)
  plt.scatter(yr_picks, ys, color = my_colhex, s=66, alpha=0.5)
  if int(row['lowerbetter']) == 1:
    grn_min = row['ymin'] # 8
    grn_max = row['green'] # vars_df.iloc[varx, 4]
    red_min = row['red'] #vars_df.iloc[varx, 5]
    if int(row['id']) == 16: # Emissions per person
      red_max = max(data_max, 8)
      ymax = red_max
    else:
      red_max = row['ymax'] # vars_df.iloc[varx, 9]
    if red_max < ymax:
      red_max = ymax
    yel_min = grn_max
    yel_max = red_min
  else:
    red_min = row['ymin'] # vars_df.iloc[varx, 8]
    if int(row['id']) == 9: # Access to electricity
      if red_min > ymin:
        ymin = red_min
    red_max = row['red'] # vars_df.iloc[varx, 5]
    grn_min = row['green'] #vars_df.iloc[varx, 4]
    grn_max = row['ymax'] #vars_df.iloc[varx, 9]
    yel_min = red_max
    yel_max = grn_min

    plt.ylim(ymin, ymax)
    xmin = 1990
    xmax = end_yr
    if not int(row['id']) == 25: # population
        opa = 0.075
        plt.fill_betweenx(y=[grn_min, grn_max], x1=xmin, x2=xmax, color='green', alpha=opa)
        plt.fill_betweenx(y=[red_min, red_max], x1=xmin, x2=xmax, color='red', alpha=opa)
        plt.fill_betweenx(y=[yel_min, yel_max], x1=xmin, x2=xmax, color='yellow', alpha=opa)

#    plt.figtext(0.88, 0.035, 'ug ' + cap, ha='right', fontsize=8)
    plt.grid(color='gainsboro', linestyle='-', linewidth=.5)
        # leg = plt.legend()
        # leg.get_frame().set_alpha(.8)
    plt.box(False)

#  plt.plot(x, y)  
#  plt.xlabel('Years')  
#  plt.ylabel('')  
#  fig.tight_layout(pad=15)
  return anvil.mpl_util.plot_image()

#    plt.xticks(yr_points)
#    plt.subplots_adjust(top=0.83, bottom=0.15)

def make_png(df, row, pyidx, end_yr, my_title):
    fig, ax = plt.subplots()
    pct = row['pct']
    x = df[:, 0]
    y = df[:, 1] * pct
    data_max = y.max() * 1.1
    data_min = y.min()
    plot_max = row['ymax']
    plot_min = row['ymin']
    ymin = min(data_min, plot_min)
    ymax = max(data_max, plot_max)
    if ymin > 0:
        ymin = 0
    if ymax < 0:
        ymax = 0
    if int(row['id']) in [27, 5]:  # Labour share of GDP | life expectancy
        ymin = plot_min  # red min
    if int(row['id']) in [26, 32]:  # population | Nitrogen use
        ymax = data_max
    if int(row['id']) in [21]:  # pH  |
        ymin = plot_min
        ymax = plot_max

    dt = 1 / 32  # = 0.03125
    abc = app_tables.regions.get(pyidx=pyidx)
#    sql = ("SELECT * FROM regions WHERE pyidx = %s")
#    conn = connect()
#    with conn.cursor() as cur:
#        cur.execute(sql, [pyidx])
#        abc = cur.fetchone()
    my_colhex = abc['colhex']
    my_lab = abc['name']
    plt.plot(x, y, color=my_colhex, linewidth=2.5, label=my_lab)
#    plt.title(my_title)
#    plt.show()
    # now plot the thick dots
    # get the year picks
    runto_row = app_tables.runto.get(end_year=end_yr)
#    sql = ("SELECT * FROM runto WHERE end_year = %s")
#    conn = connect()
#    with conn.cursor() as cur:
#        cur.execute(sql, [end_yr])
#        runto_row = cur.fetchone()
    yr_picks_str = runto_row['yr_picks']
    yps = yr_picks_str.replace("'", "")
    yr_picks = yps.split(' ')
    yps_int = []
    for i in range(0, len(yr_picks)):
        yps_int.append(int(yr_picks[i]))
#    print('IN make_png yr_picks: ')
    pvt_len = len(yr_picks)
    ys = pick(yps_int, x, y)
    plt.scatter(x, ys, color=my_colhex, s=300, alpha=0.55)
#    plt.show()

    if int(row['lowerbetter']) == 1:
        grn_min = row['ymin']  # 8
        grn_max = row['green']  # vars_df.iloc[varx, 4]
        red_min = row['red']  # vars_df.iloc[varx, 5]
        if int(row['id']) == 16:  # Emissions per person
            red_max = max(data_max, 8)
            ymax = red_max
        else:
            red_max = row['ymax']  # vars_df.iloc[varx, 9]
        if red_max < ymax:
            red_max = ymax
        yel_min = grn_max
        yel_max = red_min
    else:
        red_min = row['ymin']  # vars_df.iloc[varx, 8]
        if int(row['id']) == 10:  # Access to electricity
            if red_min > ymin:
                ymin = red_min
        red_max = row['red']  # vars_df.iloc[varx, 5]
        grn_min = row['green']  # vars_df.iloc[varx, 4]
        grn_max = row['ymax']  # vars_df.iloc[varx, 9]
        yel_min = red_max
        yel_max = grn_min

    plt.ylim(ymin, ymax)
    xmin = 1990
    xmax = end_yr
    if not int(row['id']) == 26:  # population
        opa = 0.075
        poly_coords = [(xmin, grn_max), (xmax, grn_max), (xmax, grn_min), (xmin, grn_min)]
        ax.add_patch(plt.Polygon(poly_coords, color='green', alpha=opa))
        poly_coords = [(xmin, red_max), (xmax, red_max), (xmax, red_min), (xmin, red_min)]
        ax.add_patch(plt.Polygon(poly_coords, color='red', alpha=opa))
        poly_coords = [(xmin, yel_max), (xmax, yel_max), (xmax, yel_min), (xmin, yel_min)]
        ax.add_patch(plt.Polygon(poly_coords, color='yellow', alpha=opa))
    plt.grid(color='gainsboro', linestyle='-', linewidth=.5)
    plt.box(False)
#    plt.show()
    return anvil.mpl_util.plot_image()
#    a = 2
  
@anvil.server.background_task
@anvil.server.callable
def fake_it_serverOLD(region, single_ta):
  # region as 'nn' single ta as 'poverty', etc
  print(region)
  regrow = app_tables.regions.get(abbreviation=region)
  print (regrow)
  regidx = int(regrow['pyidx'])
  fcol_in_mdf = read_fcol_in_mdf()
  mdf = read_mdf25()
  num_rows, num_cols = mdf.shape
  my_time = time.localtime()
  my_time_formatted = time.strftime("%a %d %b %G", my_time)
  foot1 = 'mov240906 mppy GAME e4a 10reg.mdl'
  cap = foot1 + ' on ' + my_time_formatted
  regidx, long, farbe = get_reg_x_name_colx(region)
#  print(region + '  ' + long)
#  print('    ' + single_ta)
  vars_info_l, vars_info_rows = get_all_vars_for_ta(single_ta)
  plot_list = []
  for var_row in vars_info_rows:
    var_l = var_row['vensim_name']
    var_l = var_l.replace(" ", "_") # vensim uses underscores not whitespace in variable name
    varx = var_row['id']
    if varx in[18, 20, 34]: # global variable  
      idx = fcol_in_mdf[var_l] # find location of variable in mdf
    else:
      idx = fcol_in_mdf[var_l] # find location of variable in mdf

#    row = get_row_from_varl(var_l)
    print('IN fake_it_server, idx: ' + str(idx) + ' varl: ' + var_l)
    print('IN fake_it_server, idx: ' + str(idx) + ' regidx: ' + str(regidx))    
    lx = idx + regidx
    print (lx)
    dfv = mdf[:, [0, lx]]
    cur_fig = make_png(dfv, var_row, regidx, 2025)
    cur_title = 'ETI-' + str(int(var_row['sdg_nbr'])) + ': ' +var_row['sdg']
    cur_sub = var_row['indicator']
    cur_cap = cap
    fdz = {'title' : cur_title, 'subtitle' : cur_sub, 'fig' : cur_fig, 'cap' : cur_cap}
    plot_list.append(fdz)
  return plot_list

@anvil.server.background_task
@anvil.server.callable
def fake_it_server(region, single_ta):
  # region as 'nn' single ta as 'poverty', etc
    print(region + ' ' + single_ta)
    regrow = app_tables.regions.get(abbreviation=region)
#    sql = ("SELECT * FROM regions WHERE abbreviation = %s")
#    conn = connect()
#    with conn.cursor() as cur:
#      cur.execute(sql, [region])
#      row = cur.fetchone()
#    regrow = row
    regidx = int(regrow['pyidx'])
    fcol_in_mdf = read_fcol_in_mdf()
    mdf = read_mdf25()
    num_rows, num_cols = mdf.shape
    my_time = time.localtime()
    my_time_formatted = time.strftime("%a %d %b %G", my_time)
    foot1 = 'mov240906 mppy GAME e4a 10reg.mdl'
    cap = foot1 + ' on ' + my_time_formatted
    long, farbe = get_reg_x_name_colx(region)
#  print(region + '  ' + long)
#  print('    ' + single_ta)
    vars_info_l, vars_info_rows = get_all_vars_for_ta(single_ta)
    plot_list = []
    for var_row in vars_info_rows:
        var_l = var_row['vensim_name']
        var_l = var_l.replace(" ", "_") # vensim uses underscores not whitespace in variable name
        varx = var_row['id']
        if varx in[19, 21, 22, 35]: # global variable
            idx = fcol_in_mdf[var_l]
            lx = idx # find location of variable in mdf
        else:
            idx = fcol_in_mdf[var_l]
            lx = idx + regidx # find location of variable in mdf with reg offset

#    row = get_row_from_varl(var_l)
        print('IN fake_it_server, idx: ' + str(idx) + ' varl: ' + var_l)
#        print('IN fake_it_server, idx: ' + str(idx) + ' regidx: ' + str(regidx))
        dfv = mdf[:, [0, lx]]
        cur_title = 'ETI-' + str(int(var_row['sdg_nbr'])) + ': ' +var_row['sdg']
        cur_sub = var_row['indicator']
        cur_fig = make_png(dfv, var_row, regidx, 2025, cur_sub)
        cur_sub = var_row['indicator']
        cur_cap = cap
        fdz = {'title' : cur_title, 'subtitle' : cur_sub, 'fig' : cur_fig, 'cap' : cur_cap}
#        print(fdz)
        plot_list.append(fdz)
    return plot_list
