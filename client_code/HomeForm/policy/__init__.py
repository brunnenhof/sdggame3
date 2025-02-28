from ._anvil_designer import policyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random

class policy(policyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.pol_name.text = self.item['pol_name']
    self.pol_expl.text = self.item['pol_expl']
    self.slide_min.text = self.item['pol_tltl']
    self.slide_max.text = self.item['pol_gl']
    self.pol_abbr.text = self.item['pol_abbr']
    
  def slider_1_change(self, **event_args):
    self.slide_val.text = self.slider_1.value

  def get_budget_for_region(self, reg):
    global budget
    lb = budget
    print(lb)
    a = 2
    
  def slider_1_change_end(self, **event_args):
    global budget
    row = app_tables.globs.get()
    cid = row['game_id']
    ta = row['ta'].capitalize()
    reg = row['reg']
    # update the games DB
    # need game_id, reg, pol, runde, to
    # set wert
    pol = self.pol_abbr.text
    runde = 1
    row = app_tables.games.get(game_id=cid, pol=pol, runde=runde, ta=ta, reg=reg)
    print (row)
    row['wert'] = float(self.slider_1.value)
    # now I need to get the percentage
    lb = self.get_budget_for_region(reg)
    a=2

  