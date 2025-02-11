import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
import pandas as pd
import csv
import datetime

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
#    for j in range(0,4):
      #      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))

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
    #for j in range(0,7):#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))
#id	abbreviation	name	tltl	gl	expl	ta
#1	ExPS	Expand policy space	0	100	Cancels a percentage of Govt debt outstanding to private lenders in policy start year	Poverty

@anvil.server.callable
def upload_ministries_change(data):
  # Delete all rows in the table
  app_tables.ministries.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.ministries.add_row(id=float(dro[0]), ministry=dro[1], longname=dro[2])
    #for j in range(0,3):#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))
#id	ministry	longname
#1	Poverty	against Poverty

@anvil.server.callable
def upload_game_info_change(data):
  # Delete all rows in the table
  app_tables.games_info.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.games_info.add_row(id=float(dro[0]), game_id=dro[1], started_on=dro[2], updated=dro[3],
                            closed=dro[4], next_step_p=float(dro[5]), next_step_gm=float(dro[6]), npbhp=dro[7])
    #for j in range(0,8):#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))
#id	game_id	started_on	updated	closed	next_step_p	next_step_gm	npbhp
#17	ZJTZP-732-665	29/01/2025 12:46	NULL	0	0	1	['us', 'cn', 'me', 'pa', 'se']

@anvil.server.callable
def upload_games_change(data):
  # Delete all rows in the table
  app_tables.games.delete_all_rows()
  laenge = len(data)
  for i in range(1, laenge):
    dro = clean_csv(data[i])
    app_tables.games.add_row(id=float(dro[0]), game_id=dro[1], reg=dro[2], wert=float(dro[3]),
                            runde=float(dro[4]), pol=dro[5], ta=dro[6])
    #for j in range(0,7):#      print(str(i) + ' ' + str(j) + ' value: ' + dro[j] + ' type: ' + str(type(dro[j])))
#id	game_id	acro_reg	wert	runde	acro_pol	ta
#1	TEST-000-111	us	0	1	ExPS	Poverty

@anvil.server.callable
def start_new_game(cid, npbhpv, next_step_gmv):
  nn_str = ' '.join(npbhpv)
  jetzt = datetime.datetime.now()
  app_tables.games_info.add_row(game_id=cid , npbhp=nn_str, next_step_gm= next_step_gmv , started_on = jetzt) 
  return True

def get_games_info_last_row(cid):
  row = app_tables.games_info.get(game_id=cid)
  print (row)
  print (type(row))
  return row
  
def make_list_from_str(npbhp):
  a = npbhp.replace("['", '')
  a = a.replace("']", '')
  a = a.replace("', '", ' ')
  return a.split(' ')
    
def set_up_role_assignments(game_id, npbhp, regions):
  print (game_id)
  print (npbhp)
  conn = connect()
  with conn.cursor() as cur:
    sql = ("DELETE FROM `fill_roles` WHERE `id` > 0")
    cur.execute(sql)
    conn.commit()
    sql = ("ALTER TABLE `fill_roles` AUTO_INCREMENT = 0;")
    cur.execute(sql)
    conn.commit()
    for r in regions:
      sql = ("INSERT INTO `fill_roles` (`game_id`, `region`, `poverty`, `inequality`,`empowerment`,`food`,`energy`,`future`,`reg_avail`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
      if r not in npbhp:
        cur.execute(sql, (game_id, r, 1, 1, 1, 1, 1, 1, 1))
      else:
        cur.execute(sql, (game_id, r, 0, 0, 0, 0, 0, 0, 0))    
    conn.commit()

def get_sql(table, col):
#  names = [r['name'] for r in app_tables.people.search()]
  if table == 'regions':
    names = [r[col] for r in app_tables.regions.search()]
  elif table == 'policies':
    names = [r[col] for r in app_tables.policies.search()]
  else:
    print ("ooops - need to add an elif with table name")
  return names

@anvil.server.callable
def set_up_game_db(runde, cid):
  k = runde
  ### 
  gi = get_games_info_last_row(cid)
  print(gi)
#    npbhp = gi[0]['npbhp']
#    if not npbhp == '[]':
#      npbhp = make_list_from_str(npbhp)
#      print(npbhp)
#      game_id = gi[0]['game_id']
#      regions = get_sql('regions', 'abbreviation')
#     print(regions)
#      policies = get_sql('policies', 'abbreviation')  # read policies as abbreviation
#      tltl = get_sql('policies', 'tltl')  # read tltl values
#      gl = get_sql('policies', 'gl')  # read gl values
#      ta = get_sql('policies', 'ta')  # read tas as list as long as policies
#      for i in regions:
#        gg = 0
#        for j in policies:
#          print(str(k) + ' ' + i + ' ' + j)
#          if i in npbhp:  # if this region is not played by human players set a random value
#            mymin = tltl[gg]
#            mymax = gl[gg]
#            myhalf = (mymax - mymin) / 2
#            wert = random.uniform(myhalf, mymax)  # random policy value biased towards GL
#          else:
#            wert = tltl[gg]
#          sql = ("INSERT INTO `games` (`game_id`, `acro_reg`, `wert`, `acro_pol`,`runde`,`ta`) VALUES (%s, %s, %s, %s, %s, %s)")
#          cur.execute(sql, (game_id, i, wert, j, k, ta[gg]))
#          gg += 1
#      conn.commit()
#  set_up_role_assignments(game_id, npbhp, regions)


    