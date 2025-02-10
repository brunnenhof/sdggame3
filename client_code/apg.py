from ._anvil_designer import apgTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class apg(apgTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def admin_pw_entry_change(self, **event_args):
    self.admin_pw_entry.enabled = (self.admin_pw_entry.text == "thalloma12")

  def admin_pw_btn_click(self, **event_args):
    self.raise_event('x-close-alert', value = self.admin_pw_entry.text)

