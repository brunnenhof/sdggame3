from ._anvil_designer import ineq_temlateTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ineq_temlate(ineq_temlateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.pol_ineq_name.text = self.item['pol_name']
    self.pol_ineq_amount.text = self.item['pol_amount']

