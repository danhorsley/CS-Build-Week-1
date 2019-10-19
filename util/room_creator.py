import random
from region_dictionaries import *

class room:
  """creates room class which hold all the details of the 
  room: co-ords, exits, region, items and description"""
  def __init__(self, coords = 'x+00y+00z+00', region ='castle'):

    self.exits = {'n_exit' : False, 's_exit' : False, 'w_exit' : False, 'e_exit' : False,
                  'stairs_up': False,'stairs_down': False, 'secret_passage': False}
    self.id = id(self)
    self.coords = [int(coords[1:4]),int(coords[5:8]),int(coords[9:])]
    self.region = region
    self.description = f'''this is a room with co-ordinates {self.coords}.'''

  def create_full_description(self):
    d_text = {'n_exit' : 'north', 's_exit' : 'south ', 'w_exit' : 'west', 'e_exit' : 'east',
                  'stairs_up': 'stairs up','stairs_down': 'stairs down', 'secret_passage': 'a secret passage'}
    cur_reg_dict = all_regions[self.region]
    sights = random.sample(cur_reg_dict['Sights'],2)
    smells = random.sample(cur_reg_dict['Smells'],2)
    sounds = random.sample(cur_reg_dict['Sounds'],2)
    feels = random.sample(cur_reg_dict['Touch'],2)
    paths = random.sample(cur_reg_dict['Paths'],4)
    hows = random.sample(cur_reg_dict['How'],4)
    available_exits = [e for e in self.exits.keys() if self.exits[e] is not False]
    exit_text = ''
    counter = 0
    for t in available_exits:

      if t in ['n_exit','w_exit','s_exit','e_exit']:
        exit_text = exit_text + '  A' + paths[counter] + f' {hows[counter]} to the {d_text[t]}.'
      elif t=='stairs_up':
        exit_text = exit_text + '  A' +  random.choice(cur_reg_dict['Up']) + f' leads upwards.'
      elif t=='stairs_down':
        exit_text = exit_text + '  A' + random.choice(cur_reg_dict['Down']) + f' leads downwards.'
      counter += 1

    self.description = (f'''You are in a {self.region}.  You see {sights[0]} and 
                        {sights[1]}.  You can smell {smells[0]} and hear {sounds[0]}.
                          You feel {feels[0]}.  ''' + exit_text).replace('\n                        ','')