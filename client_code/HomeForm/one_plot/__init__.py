from ._anvil_designer import one_plotTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class one_plot(one_plotTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Set the Labels to have fields from the `item` dictionary,
    # which is one entry in the RepeatingPanel's `items` list:
    self.one_plot_title.text = self.item['title']
    self.one_plot_subtitle.text = self.item['subtitle']
    self.one_plot_units.text = self.item['unit']
    self.one_plot_caption.text = self.item['cap']
    self.one_plot_img.source = self.item['fig']
