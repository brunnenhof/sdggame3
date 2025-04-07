from ._anvil_designer import rep_wait_decTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rep_wait_dec(rep_wait_decTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.rwd_reg.text = self.item['rwd_reg']
