from ._anvil_designer import futureTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class future(futureTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
  # Set the Labels to have fields from the `item` dictionary,
    # which is one entry in the RepeatingPanel's `items` list:
    self.
    self.one_plot_title.text = self.item['title']
    self.one_plot_subtitle.text = self.item['subtitle']
    self.one_plot_caption.text = self.item['cap']
    self.one_plot_img.source = self.item['fig']