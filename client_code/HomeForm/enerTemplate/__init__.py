from ._anvil_designer import enerTemplateTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class enerTemplate(enerTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    self.pol_ener_name.text = self.item['pol_name']
    self.pol_ener_amount.text = self.item['pol_amount']
