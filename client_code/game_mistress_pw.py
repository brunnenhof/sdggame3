from ._anvil_designer import game_mistress_pwTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class game_mistress_pw(game_mistress_pwTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def admin_pw_ok_click(self, **event_args):
    self.raise_event('x-close-alert', value = self.admin_pw_entry.text)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

