import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#    from ..HomeForm import Module1
#    Module1.say_hello()

# if a game is halted, these values should also be store in game_info
# what is the current round
runde = 1
# what is the next step for the game organizer
nxt_gm = 0
# what is the next step for the players
nxt_play = 0

def say_hello():
  print("Hello, world")
