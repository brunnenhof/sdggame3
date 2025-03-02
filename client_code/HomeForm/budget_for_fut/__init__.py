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
