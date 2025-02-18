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

  def btn_join_game_click(self, **event_args):
    # check if a game is ready
    # pick up latest game_id & game_info[next_step_p] == 1
    self.card_holder_top.visible = False
    self.cp_confirm_game_id.visible    
    """This method is called when the button is clicked"""
    pass


  def cp_rejoin_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert("Not is not yet coded ... check back later ...")
    pass

  def assign_roles(self, cid):
    roles = app_tables.fill_roles.search(game_id=cid)
    print (roles)

  def cp_join_click(self, **event_args):
    """This method is called when the button is clicked"""
    row = anvil.server.call('get_latest_game')
    self.cp_top.visible= False
    self.cp_confirm_game_id.visible = True
    self.cp_id_holder.text = row['game_id']
    rr = self.assign_roles(row['game_id'])    

#    roles = anvil.server.call('get_roles', row['game_id'])
    print(row['game_id'])
    pass

  def cp_submit_game_id_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass


    