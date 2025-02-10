from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_thanks_click(self, **event_args):
    alert(content="To our Alpha testers, Baesweiler", title="Thank you", large=True)
