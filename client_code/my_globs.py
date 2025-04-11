import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#    from .. import Module1
#    Module1.say_hello()
###
### these are CLIENT globals, ie all forms on the client side can access them
my_game_id = ''
my_reg = ''
my_ministry = ''
my_personal_game_id = ''
my_step = 1
game_step = 0
###
### comment this out in production and ask interactively
not_played_by_players = ['us', 'af', 'cn', 'sa', 'la', 'pa', 'eu', 'se']
###
### below does not change, evah!
roles = ['pov', 'ineq', 'emp', 'food', 'ener', 'fut']
ro_nbr = [0, 1, 2, 3, 4, 5]
regs = ['us', 'af', 'cn', 'me', 'sa', 'la', 'pa', 'ec', 'eu', 'se']
re_nbr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



