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

  def get_budget_for_region(self, reg, cid, yr):
    lb = app_tables.budget.search(reg=reg, game_id=cid, yr=yr)
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
    if runde==1:
      yr = 2025
    else:
      alert("OOPS in slider_1_change_end: forgot to set YEAR")
    row = app_tables.games.get(game_id=cid, pol=pol, runde=runde, ta=ta, reg=reg)
    print (row)
    row['wert'] = float(self.slider_1.value)
    # now I need to get the percentage
    pct_pov = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Poverty', reg=reg, runde=runde)]
    pct_ineq = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Inequality', reg=reg, runde=runde)]
    pct_emp = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Empowerment', reg=reg, runde=runde)]
    pct_food = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Food', reg=reg, runde=runde)]
    pct_ener = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Energy', reg=reg, runde=runde)]
    tltl_pov = [r['tltl'] for r in app_tables.policies.search(ta='Poverty')]
    gl_pov = [r['gl'] for r in app_tables.policies.search(ta='Poverty')]
    lb = app_tables.budget.get(reg=reg, game_id=cid, yr=yr)
    bud = lb['Bud_all_TA']
    max_cost_pov = lb['Cost_poverty']
    cost_pov = 0
    for i in range(0, len(pct_pov)):
      nw = pct_pov[i] - tltl_pov[i]
      nb = 0
      nt = gl_pov[i] - tltl_pov[i]
      pct_of_range = nw / (nt - nb)
      cost_pov += max_cost_pov * pct_of_range
    total_cost = cost_pov
    pct_of_budget = total_cost / bud * 100
    self.budget_constraint.text = pct_of_budget
    if pct_of_budget > 100:
      if pct_of_budget > 101:
        pct_shown = int(pct_of_budget)
      else:
        pct_shown = round(pct_of_budget, 1)
      self.budget_feedback.text = 'You are using ' + str(pct_shown) + '% of your regional budget!'
      self.budget_feedback.foreground = 'red'
    else:
      self.budget_feedback.text = 'You are using' + str(pct_of_budget) + '% of your regional budget!'
      self.budget_feedback.foreground = 'green'
    a=2

  