from room_creator import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

color_dict = {'castle' : '#6C3483','dungeon' : '#424949','city' : '#99A3A4','sewers' : '#B9770E',
                'forest' : '#145A32' ,'warrens' : '#641E16','mountains' : '#3498DB','mines' : '#F4D03F'}

def my_f(x):
  """formats numbers into right string for dictionary labels"""
  if abs(x)<10:
    if x<0:
      return f'-0{abs(x)}'
    else:
      return f'+0{x}'
  else:
    if x<0:
      return f'-{abs(x)}'
    else:
      return f'+{x}'

class dungeon:
    def __init__(self, length=10 , width = 10, depth = 1, lat_bias = 4, vert_bias = 4):
        self.length = length
        self.width = width
        self.depth = depth
        self.lb = lat_bias
        self.vb = vert_bias
        self.rooms = {}

    def get_room(self, coords = 'x+00y+00z+00'):
        """returns the co-ords of the room in list/integer form"""
        return self.rooms[coords]
    
    def create_dungeon(self):
        """creates a consistent dungeon using dimesions specified  in the class"""
        for d in range(-self.depth,self.depth):
            y = -self.length
            while y < self.length:
                x = -self.width
                while x < self.width:
                    current_coords = f'x{my_f(x)}y{my_f(y)}z{my_f(d)}'
                    new_room = room(current_coords)
                    #join up to old rooms
                    if x!= -self.width and self.get_room(f'x{my_f(x-1)}y{my_f(y)}z{my_f(d)}').exits['e_exit']:
                        new_room.exits['w_exit'] = True
                    if y!=-self.length and self.get_room(f'x{my_f(x)}y{my_f(y-1)}z{my_f(d)}').exits['n_exit']:
                        new_room.exits['s_exit'] = True
                    if d!=-self.depth and self.get_room(f'x{my_f(x)}y{my_f(y)}z{my_f(d-1)}').exits['stairs_up']:
                        new_room.exits['stairs_down'] = True
                    #extra random exits
                    if x!= self.width:
                        new_room.exits['e_exit'] = random.choice([True] + [False]*self.lb)
                    if y!= self.length:
                        new_room.exits['n_exit'] = random.choice([True] + [False]*self.lb)
                    if d!= self.depth:
                        new_room.exits['stairs_up'] = random.choice([True] + [False]*self.vb)  #making staircases rarer than even
                    self.rooms[current_coords] = new_room
                    x += 1
                y += 1

    def create_regions(self,origin = [0,0,0]):
        "splits the map into regions"
        for room in self.rooms:
            rc = self.rooms[room]
            if rc.coords[0] >= 0 and rc.coords[1] >= 0 and rc.coords[2] >= 0:
                rc.region = 'castle'
            if rc.coords[0] >= 0 and rc.coords[1] >= 0 and rc.coords[2] < 0:
                rc.region = 'dungeon'
            if rc.coords[0] >= 0 and rc.coords[1] < 0 and rc.coords[2] >= 0:
                rc.region = 'city'
            if rc.coords[0] >= 0 and rc.coords[1] < 0 and rc.coords[2] < 0:
                rc.region = 'sewers'
            if rc.coords[0] < 0 and rc.coords[1] < 0 and rc.coords[2] >= 0:
                rc.region = 'forest'
            if rc.coords[0] < 0 and rc.coords[1] < 0 and rc.coords[2] < 0:
                rc.region = 'warrens'
            if rc.coords[0] < 0 and rc.coords[1] >= 0 and rc.coords[2] >= 0:
                rc.region = 'mountains'
            if rc.coords[0] < 0 and rc.coords[1] >= 0 and rc.coords[2] < 0:
                rc.region = 'mines'

    def render_map_ni(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        direction_dic = {'n_exit' : [0,1,0], 's_exit' : [0,-1,0], 'w_exit' : [1,0,0], 'e_exit' : [-1,0,0],
                        'stairs_up' : [0,0,1], 'stairs_down' : [0,0,-1]}
        all_points = []
        for r in self.rooms:
            for exit in self.rooms[r].exits:
                if self.rooms[r].exits[exit]:
                    old_point = self.rooms[r].coords#[:2]
                    new_point = [(i+j) for i,j in  zip(old_point,direction_dic[exit])]
                    region_color = color_dict[self.rooms[r].region]
                    plt.plot([old_point[0],new_point[0]], [old_point[1],new_point[1]],[old_point[2],new_point[2]], region_color)
                    all_points.append([old_point,new_point])
            #ax.scatter(x_space,y_space,z_space)
        strFile = 'map_plot.png'
        if os.path.isfile(strFile):
            os.remove(strFile)
        plt.savefig(strFile)
