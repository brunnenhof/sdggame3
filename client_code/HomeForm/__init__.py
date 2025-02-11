from ._anvil_designer import HomeFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
import webbrowser
from ..apg import apg

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
    self.admin_pw_box.visible=True
    self.label_enter_pw.visible=True
    """This method is called when the button is clicked"""
    pass

  def admin_pw_box_pressed_enter(self, **event_args):
#    alert(title="You entered ", content=self.admin_pw_box.text, large=True, buttons=['OK', 'Cancel'])
    ###
    # ToDo put the password into server code !!
    ###
    if self.admin_pw_box.text == 'thalloma12':
      self.card_holder_admin.visible = True
      self.card_holder_top.visible = False
    else:
      alert("Wrong password. Sorry")
      
    """This method is called when the user presses Enter in this text box"""
    pass

  def reload_sdg_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def reload_reg_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def load_sdg_var_change(self, file, **event_args):
    text = file.get_bytes()
    text_str = text.decode('utf-8')
    print(type(text_str))
    tsplit = text_str.splitlines(keepends=False)
    print(type(tsplit))
    anvil.server.call('upload_sdg_var_change', tsplit)
    alert('The file has been uploaded and saved to table')

#  def upload_sdg_var_change(self, file, **event_args):
#    text = file.get_bytes()
#    tsplit = text.splitlines(keepends=False)
#    anvil.server.call('upload_sdg_var_change', tsplit)
#    alert('The file has been uploaded and saved to table')
