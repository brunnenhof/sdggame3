from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
import webbrowser
from ..apg import apg
import random
import string

class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_thanks_click(self, **event_args):
    alert(content="... to our Alpha testers, the students in course SW101 at the Realschule Baesweiler during April 2024 taught by René Langohr, and all the beta testers.", title="Thank you", large=True)

  def btn_help_click(self, **event_args):    
    webbrowser.open_new("http://sdggamehelp.blue-way.net")

  def btn_admin_click(self, **event_args):
    self.admin_pw_box.visible=True
    self.label_enter_pw.visible=True
    """This method is called when the button is clicked"""
    pass

  def admin_pw_box_pressed_enter(self, **event_args):
#    alert(title="You entered ", content=self.admin_pw_box.text, large=True, buttons=['OK', 'Cancel'])
    ###
    # ToDo put the password into server code !!
    ###
    if self.admin_pw_box.text == 'thalloma12':
      self.card_holder_admin.visible = True
      self.card_holder_top.visible = False
    else:
      alert("Wrong password. Sorry")
      
    """This method is called when the user presses Enter in this text box"""
    pass

  def load_csv_file_into_db(self, file, server, **event_args):
    text = file.get_bytes()
    text_str = text.decode('utf-8')
#    print(type(text_str))
    tsplit = text_str.splitlines(keepends=False)
#    print(type(tsplit))
    anvil.server.call(server, tsplit)
    alert('The file has been uploaded and saved to table')
    
  def load_sdg_var_change(self, file, server):
    text = file.get_bytes()
    text_str = text.decode('utf-8')
#    print(type(text_str))
    tsplit = text_str.splitlines(keepends=False)
#    print(type(tsplit))
    anvil.server.call('upload_sdg_var_change', tsplit)
    alert('The file has been uploaded and saved to table')

#  def upload_sdg_var_change(self, file, **event_args):
#    text = file.get_bytes()
#    tsplit = text.splitlines(keepends=False)
#    anvil.server.call('upload_sdg_var_change', tsplit)
#    alert('The file has been uploaded and saved to table')

  def load_sdg_change(self, file, **event_args):
    self.load_csv_file_into_db(file, 'upload_sdg_change')
#    self.load_csv_file_into_db(self, file, 'upload_sdg_change')

  def Load_runto_change(self, file, **event_args):
    self.load_csv_file_into_db(file, 'upload_runto_change')

  def load_regions_change(self, file, **event_args):
      self.load_csv_file_into_db(file, 'upload_regions_change')

  def load_policies_change(self, file, **event_args):
      self.load_csv_file_into_db(file, 'upload_policies_change')

  def load_ministries_change(self, file, **event_args):
      self.load_csv_file_into_db(file, 'upload_ministries_change')

  def load_games_info_change(self, file, **event_args):
      self.load_csv_file_into_db(file, 'upload_game_info_change')

  def load_games_change(self, file, **event_args):
      self.load_csv_file_into_db(file, 'upload_games_change')

  def btn_continue_game_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(title="ToDo", content="does not yet work :(")

  def btn_log_in_gm_click(self, **event_args):
    self.card_holder_top.visible = False
    self.gm_login_card.visible = True
    
  def gm_login_box_pressed_enter(self, **event_args):
    if self.gm_login_box.text == 'gol':
      self.gm_login_card.visible = False
      self.card_holder_gm.visible = True
    else:
      gm_pw = alert("Sorry, wrong password.", buttons=['Try again', 'Cancel'])
      if gm_pw == 'Cancel':
        self.gm_login_card.visible = False

  def generate_custom_id(self):
    global cid
    cid = ''.join(random.choices(string.ascii_uppercase, k=5))
    a = random.randint(100, 999)
    d = random.randint(100, 999)
    cid = cid + '-' + str(d) + '-' + str(a) 
    # cid = 'TEST'  #  while testing ...
    return f"{cid}"

  def start_new_game_click(self, **event_args):
    """This method is called when the button is clicked"""
    global cid
    cid = self.generate_custom_id()
    self.label_glb_game_id.visible = True
    self.box_glb_text.visible = True
    self.box_glb_text.text = cid
    #set_new_game = anvil.server.call('start_new_game', cid)
    self.btn_new_game2.visible = False
    self.btn_continue_game.visible = False
#    self.select_regions_label.visible = True
    self.gm_reg_selection_card.visible = True

  def button_submit_not_played_click(self, **event_args):
    """This method is called when the button is clicked"""
    global cid
    npbhp = [] # not played by human players
    if self.check_box_us.checked:
      npbhp.append('us')
    if self.check_box_af.checked:
      npbhp.append('af')
    if self.check_box_cn.checked:
      npbhp.append('cn')
    if self.check_box_me.checked:
      npbhp.append('me')
    if self.check_box_sa.checked:
      npbhp.append('sa')
    if self.check_box_la.checked:
      npbhp.append('la')
    if self.check_box_pa.checked:
      npbhp.append('pa')
    if self.check_box_ec.checked:
      npbhp.append('ec')
    if self.check_box_eu.checked:
      npbhp.append('eu')
    if self.check_box_se.checked:
      npbhp.append('se')
    self.button_submit_not_played.visible = False
    set_up_gi, npbhp_str = anvil.server.call('start_new_game', cid, npbhp, 1)
    if set_up_gi:
      self.label_set_up_game_info.visible = True
      temp, regions = anvil.server.call('set_up_game_db', 1, cid, npbhp)
      if temp:
        self.label_rd1_setup1.visible = True
      anvil.server.call('set_up_game_db', 2, cid, npbhp)
      self.label_rd2_setup.visible = True
      anvil.server.call('set_up_game_db', 3, cid, npbhp)
      self.label_rd3_setup.visible = True
      anvil.server.call('set_up_role_assignments', cid, npbhp, regions)
      txt = 'Role assignments are set up ... Now tell your players to join game ' + cid + ' and log in to their roles. You need to wait until all players have submitted their decisions for round 1, 2025 to 2040'
      self.label_role_assign.text = txt
      self.label_role_assign.visible = True
    else:
      alert("Something went wrong setting up the game info")

  def btn_poc_click(self, **event_args):
    alert("Neither the user interface nor the server code is elegant nor efficient. Contact us if you can help making either or all better.",
         title="This app is a Proof of Concept")
    """This method is called when the button is clicked"""
    pass

  def assign_roles(self, cid):
    roles = app_tables.fill_roles.search(game_id=cid)
    print (roles)

  def btn_join_new_click(self, **event_args):
    row = anvil.server.call('get_latest_game')
    self.cp_top.visible= False
    self.cp_confirm_game_id.visible = True
    self.cp_id_holder.text = row['game_id']
    rr = self.assign_roles(row['game_id'])    

  def btn_rejoin_existing_click(self, **event_args):
    alert("Not is not yet coded ... check back later ...")

  def btn_join_game_click(self, **event_args):
    self.card_holder_top.visible = False
    self.cp_top.visible = True

  def set_not_played_regions_to_invisible(self, reg):
    if reg == 'us':
      self.rb_us2.visible = False
    elif reg == 'af':
      self.rb_af2.visible = False
    elif reg == 'cn':
      self.rb_cn2.visible = False
    elif reg == 'me':
      self.rb_me2.visible = False
    elif reg == 'sa':
      self.rb_sa2.visible = False
    elif reg == 'la':
      self.rb_la2.visible = False
    elif reg == 'pa':
      self.rb_pa2.visible = False
    elif reg == 'ec':
      self.rb_ec2.visible = False
    elif reg == 'eu':
      self.rb_eu2.visible = False
    elif reg == 'se':
      self.rb_se2.visible = False


  def cp_submit_game_id_click(self, **event_args):
    global cid
    cid = self.cp_id_holder.text
    if cid == '':
      alert("You must enter a Game ID in the format LLLLL-XXX-XXX")
    else:
      self.cp_confirm_game_id.visible = False
      roles = app_tables.fill_roles.search(game_id=cid)
      for r in roles:
        if not r['reg_avail']:
            self.set_not_played_regions_to_invisible(r['region'])
      self.choose_role2.visible = True

  def set_ministries_visible(self, cid, reg):
#    self.label_radio_ministry.visible = True
    self.submit_role.visible = False
    ministries = app_tables.fill_roles.search(game_id=cid, region=reg)
    for key in ministries:
#      print('IN for key in ministries:')
#      print(key) # key is a row <LiveObject: anvil.tables.Row>
#      print(type(key)) # <class 'anvil.LiveObjectProxy'>
      for col in key:
#        print('IN for r in key:')
#        print(col[0] + ' ' + str(col[1])) 
        cname = col[0] # column name
        cval = col[1] # column value
        if cname == 'poverty':
          if cval:
            self.rb_pov.visible = True
          else:
            self.rb_pov.visible = False
        elif cname == 'empowerment':
          if cval:
            self.rb_emp.visible = True
          else:
            self.rb_emp.visible = False
        elif cname == 'inequality':
          if cval:
            self.rb_ineq.visible = True
          else:
            self.rb_ineq.visible = False
        elif cname == 'food':
          if cval:
            self.rb_foo.visible = True
          else:
            self.rb_foo.visible = False
        elif cname == 'energy':
          if cval:
            self.rb_ene.visible = True
          else:
            self.rb_ene.visible = False
        elif cname == 'future':
          if cval:
            self.rb_fut.visible = True
          else:
            self.rb_fut.visible = False
 
  def rb_me2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    # set all available ministries for me visible
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'me')

  def rb_foo_clicked(self, **event_args):
    self.submit_role.visible = True

  def rb_us2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'us')

  def rb_af2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'af')

  def rb_cn2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'cn')

  def rb_sa2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'sa')

  def rb_pa2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'pa')

  def rb_ec2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'ec')

  def rb_eu2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'eu')

  def rb_se2_clicked(self, **event_args):
    global cid
    print ('in me btn ' + cid)
    self.label_5.visible = True
    self.set_ministries_visible(cid, 'se')

  def rb_pov_clicked(self, **event_args):
    self.submit_role.visible = True

  def rb_ineq_clicked(self, **event_args):
    self.submit_role.visible = True

  def rb_emp_clicked(self, **event_args):
    self.submit_role.visible = True

  def rb_ene_clicked(self, **event_args):
    self.submit_role.visible = True

  def rb_fut_clicked(self, **event_args):
    self.submit_role.visible = True

  def region_clicked(self):
    if self.rb_af2.selected:
      return 'af'
    if self.rb_us2.selected:
      return 'us'
    if self.rb_cn2.selected:
      return 'cn'
    if self.rb_me2.selected:
      return 'me'
    if self.rb_sa2.selected:
      return 'sa'
    if self.rb_la2.selected:
      return 'la'
    if self.rb_pa2.selected:
      return 'pa'
    if self.rb_ec2.selected:
      return 'ec'
    if self.rb_eu2.selected:
      return 'eu'
    if self.rb_se2.selected:
      return 'se'
    return None

  def minstry_clicked(self):
    if self.rb_pov.selected:
      return 'poverty'
    if self.rb_ineq.selected:
      return 'inequality'
    if self.rb_emp.selected:
      return 'empowerment'
    if self.rb_foo.selected:
      return 'food'
    if self.rb_ene.selected:
      return 'energy'
    if self.rb_fut.selected:
      return 'future'
    return None  

  
  def save_player_choice(self, game_id, ministry, region):
    print ('in save_player_choice: ' + region)
    print ('in save_player_choice: ' + ministry)
    minis = [r['mini'] for r in app_tables.ministries.search()]
    print(minis)
    row = app_tables.fill_roles.get(game_id=game_id, region=region)
    for r in row:
      print(r)
      col_name = r[0]
      col_val = r[1]
      if col_name in minis:
        if col_val:
          rowup = app_tables.fill_roles.get(game_id=game_id, region=region)
          if col_name == 'future':
            app_tables.fill_roles.get(game_id=game_id, region=region, future = False)
#          row=app_tables.tableA.get(name="dave")
#          besty=app_tables.tableB.get(bestfriend="ernie")
          # check is reg_avail
          if not reg_avail:
            pass
        else:
          alert("Taken")
      else:
        continue
        
  # qick check if that role is still available  
#    if ministry == 'energy':
#    sql = ("SELECT energy FROM fill_roles WHERE game_id = %s AND region = %s")
#    sqls = ("UPDATE fill_roles SET energy = 1 WHERE game_id = %s AND region = %s") # prepare for save
#    elif ministry == 'poverty':
#    sql = ("SELECT poverty FROM fill_roles WHERE game_id = %s AND region = %s")
#    sqls = ("UPDATE fill_roles SET poverty = 1 WHERE game_id = %s AND region = %s")  
#  elif ministry == 'inequality':
#    sql = ("SELECT inequality FROM fill_roles WHERE game_id = %s AND region = %s")
#    sqls = ("UPDATE fill_roles SET inequality = 1 WHERE game_id = %s AND region = %s")  
#  elif ministry == 'food':
#    sql = ("SELECT food FROM fill_roles WHERE game_id = %s AND region = %s")
#    sqls = ("UPDATE fill_roles SET food = 1 WHERE game_id = %s AND region = %s")  
#  elif ministry == 'future':
#    sql = ("SELECT future FROM fill_roles WHERE game_id = %s AND region = %s")
#    sqls = ("UPDATE fill_roles SET future = 1 WHERE game_id = %s AND region = %s")  
#  elif ministry == 'empowerment':
#    sql = ("SELECT empowerment FROM fill_roles WHERE game_id = %s AND region = %s")
#    sqls = ("UPDATE fill_roles SET empowerment = 1 WHERE game_id = %s AND region = %s")  
#    if row[ministry] == 1:
#      return False
# handle False, ie role no longer available in client code
# we now know that the role is still available, so save it  
#  conn = connect()
#  with conn.cursor() as cur:
#    cur.execute(sqls, (game_id, region))
#    conn.commit()
#    # now check if setting this role as taken alse means that ALL roles are taken
    # and the region needs to be set as taken / no longer available
#    sql = ("SELECT * FROM `fill_roles` WHERE `game_id` = %s AND `region`= %s")
#    cur.execute(sql, (game_id, region))
#    all_regs = cur.fetchone()
#    if all_ministries_taken(all_regs):  # set region to not available
#      sql = ("UPDATE fill_roles SET reg_avail = 0 WHERE game_id = %s AND region = %s")
#      cur.execute(sql, (game_id, region))
#      conn.commit()
#  return True

  def submit_role_click(self, **event_args):
    global cid
    which_ministy = self.minstry_clicked()
    which_region = self.region_clicked()
    print('IN btn_submit_role_clicked')
    save_ok = self.save_player_choice(cid, which_ministy, which_region)
    if not save_ok:
      alert("Unfortunately, someone else was quicker and took the role. Please choose another one.")
        # TODO refresh ministries and regions with the correct choices still available
    else:
      wrx, which_region_long  = anvil.server.call('get_reg_long_names', which_region)
      wmx, which_ministy_long = anvil.server.call('get_ministry_long', which_ministy)
      your_game_id = game_id_entered + "-" + str(wrx) + str(wmx)
      msgid = "\nYour personal Game ID is:\n" + your_game_id + "\nPlease make a note of it!"
      msg = ("Congratulations, you have been confirmed as the Minister " + which_ministy_long + " in " + which_region_long + '.' + msgid)
      alert(msg)
      self.choose_role2.visible = False
      self.card_info_round1.visible = True
      self.card_for_plots.visible = True
      self.region_label.text = which_region_long
      temp = 'Minister ' + which_ministy_long
      self.minister_label.text = temp
      anvil.server.call('load_plots', which_region, which_ministy)
      a = 2


 


    