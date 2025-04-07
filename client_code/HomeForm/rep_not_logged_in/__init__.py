from ._anvil_designer import rep_not_logged_inTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class rep_not_logged_in(rep_not_logged_inTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.nli_reg.text = self.item['nli_reg']
    self.nli_ministry.text = self.item['nli_ministry']
