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

  def slider_1_change(self, **event_args):
    self.slide_val.text = m3
    """This method is called when the value of the component is changed"""
    pass

  