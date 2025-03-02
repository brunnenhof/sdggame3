from ._anvil_designer import budget_for_futTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class budget_for_fut(budget_for_futTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.budget_for_fut.text = self.item['rep_bud_for_label']
    self.budget_for_amount.text = self.item['rep_bud_for_amount']

  def put_policy_investments(self, **event_args):
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
      alert("OOPS in put_policy_investments: forgot to set YEAR")
    row = app_tables.games.get(game_id=cid, pol=pol, runde=runde, ta=ta, reg=reg)
    print (row)
    pct_pov = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Poverty', reg=reg, runde=runde)]
    pct_ineq = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Inequality', reg=reg, runde=runde)]
    pct_emp = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Empowerment', reg=reg, runde=runde)]
    pct_food = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Food', reg=reg, runde=runde)]
    pct_ener = [r['wert'] for r in app_tables.games.search(game_id=cid, ta='Energy', reg=reg, runde=runde)]
    tltl_pov = [r['tltl'] for r in app_tables.policies.search(ta='Poverty')]
    gl_pov = [r['gl'] for r in app_tables.policies.search(ta='Poverty')]
    tltl_emp = [r['tltl'] for r in app_tables.policies.search(ta='Empowerment')]
    gl_emp = [r['gl'] for r in app_tables.policies.search(ta='Empowerment')]
    tltl_ineq = [r['tltl'] for r in app_tables.policies.search(ta='Inequality')]
    gl_ineq = [r['gl'] for r in app_tables.policies.search(ta='Inequality')]
    tltl_food = [r['tltl'] for r in app_tables.policies.search(ta='Food')]
    gl_food = [r['gl'] for r in app_tables.policies.search(ta='Food')]
    tltl_ener = [r['tltl'] for r in app_tables.policies.search(ta='Energy')]
    gl_ener = [r['gl'] for r in app_tables.policies.search(ta='Energy')]
    lb = app_tables.budget.get(reg=reg, game_id=cid, yr=yr)
    bud = lb['Bud_all_TA']
    max_cost_pov = lb['Cost_poverty']
    max_cost_food = lb['Cost_food']
    max_cost_ener = lb['Cost_energy']
    max_cost_ineq = lb['Cost_inequality']
    max_cost_emp = lb['Cost_empowerment']
    cost_pov = self.calc_cost(pct_pov, tltl_pov, gl_pov, max_cost_pov)
    cost_emp = self.calc_cost(pct_emp, tltl_emp, gl_emp, max_cost_emp)
    cost_ineq = self.calc_cost(pct_ineq, tltl_ineq, gl_ineq, max_cost_ineq)
    cost_food = self.calc_cost(pct_food, tltl_food, gl_food, max_cost_food)
    cost_ener = self.calc_cost(pct_ener, tltl_ener, gl_ener, max_cost_ener)    
    total_cost = cost_pov + cost_emp + cost_ener + cost_food + cost_ineq
    pct_of_budget = total_cost / bud * 100
    if pct_of_budget > 100:
      if pct_of_budget > 101:
        pct_shown = str(int(pct_of_budget))
      else:
        pct_shown = round(pct_of_budget, 1)
      self.budget_constraint.foreground = 'red'
    else:
      if pct_of_budget > 1:
        pct_shown = str(int(pct_of_budget))
      else:
        pct_shown = round(pct_of_budget, 1)
      self.budget_constraint.text = pct_shown
      self.budget_constraint.foreground = 'green'
    a=2

