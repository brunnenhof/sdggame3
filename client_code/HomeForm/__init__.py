from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import webbrowser


class HomeForm(HomeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def btn_thanks_click(self, **event_args):
    alert(content="... to our Alpha testers, the students in course SW101 at the Realschule Baesweiler during April 2024 taught by René Langohr, and all the beta testers.", title="Thank you", large=True)

  def btn_help_click(self, **event_args):    
    webbrowser.open_new("http://sdggamehelp.blue-way.net")

  def btn_admin_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
