from ._anvil_designer import policyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class policy(policyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    budget = anvil.server.call('get_policy_budgets', 2025)
    print (budget)
    expl = [r['expl'] for r in app_tables.policies.search()]
    pol_name = [r['name'] for r in app_tables.policies.search()]
    tltl = [r['tltl'] for r in app_tables.policies.search()]
    gl = [r['gl'] for r in app_tables.policies.search()]
    a = 2

  @property
  def level(self):
    return self._level
  
  @level.setter
  def level(self, value):
    self._level = value
    self.update()
    
  @property
  def slider_min(self):
    return self._slider_min
  
  @slider_min.setter
  def slider_min(self, value):
    self._slider_min = value
    self.update()
    
  @property
  def slider_max(self):
    return self._slider_max
  
  @slider_max.setter
  def slider_max(self, value):
    self._slider_max = value
    self.update()
    
  @property
  def step(self):
    return self._step
  
  @step.setter
  def step(self, value):
    self._step = value
    self.update()
    
  @property
  def level(self):
    return self._level
  
  @level.setter
  def level(self, value):
    self._level = value
    self.update()
    
  def slider_change(self, value, **event_args):
    self._level = int(value)
    self.raise_event("change", level=self.level)
  
  def update(self):
    if self._shown:
      self.call_js('set_behavior', self.level, self.slider_min, self.slider_max, self.step)
  
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    self._shown = True
    self.update()
