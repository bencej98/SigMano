import turtle
import time
import random

class Player(turtle.Turtle):
   def __init__(self, name:str, x:int, y:int, color:str, size:float, speed:int):
      super().__init__()
      self.name = name
      self.size = size
      self.shape("circle")
      self.shapesize(size)
      self.color(color)
      self.name1 = turtle.Turtle()
      self.name1.color(color)
      self.name1.hideturtle()
      self.name1.penup()
      self.name1.speed(speed)
      self.name1.goto(x, y+10*size)
      self.penup()
      self.speed(speed)
      self.goto(x, y)
      self.name1.write(name, False, "center")

   def move(self, x:int, y:int):
      x = x_y_for_screen(x)
      y = x_y_for_screen(y)
      self.name1.goto(x, y+self.size*10)
      self.name1.clear()
      self.goto(x, y)
      self.name1.write(self.name, False, "center")

tile_size = 30
tile_number = 20

def x_y_for_screen(coordinate:int):
   return tile_size*(coordinate-9.5)

def create_object(object_name:str, coordinates:list, user_name, chosen_color):
   x = x_y_for_screen(coordinates[0])
   y = x_y_for_screen(coordinates[1])
   if user_name == object_name:
      obj = Player(object_name, x, y, chosen_color, tile_size/60, 2)
   else:
      obj = Player(object_name, x, y, chosen_color, tile_size/60, 2)
   return obj

def get_obj_from_list(name:str,object_list:list):
   for i in object_list:
      if i.name == name:
         return i

def obj_names_from_list(obj_list:list) -> list:
   obj_names = []
   for i in obj_list:
      obj_names.append(i.name)
   return obj_names

def remove_obj_from_list(obj_list:list, json_dict:dict):
   names_from_json = []
   removable_objects = []
   for name in json_dict.keys():
      names_from_json.append(name)
   for obj in obj_list:
      if obj.name not in names_from_json:
         removable_objects.append(obj)
   for obj in removable_objects:
      obj_list.remove(obj)
      obj.color("lightgreen")
      obj.name1.clear()
      del obj

def dict_data_for_screen(json_dict:dict, user_name, chosen_color, object_list:list=[]):
   obj_names = obj_names_from_list(object_list)
   remove_obj_from_list(object_list,json_dict)
   for name, coordinates in json_dict.items():
      if name in obj_names:
         obj = get_obj_from_list(name, object_list)
         obj.move(coordinates[0], coordinates[1])
      else:
         obj = create_object(name, coordinates, user_name, chosen_color)
         object_list.append(obj)

object_list = []
json_temp = {'loluser': [2, 3], 'loluser2': [18, 9]}
user_name = 1

def set_temp_json(dict_obj, user):
   global json_temp
   json_temp = dict_obj
   global user_name
   user_name = user

# def temp_valami(user_name):
#    for i in range(10):
#       x = random.randint(0,19)
#       y = random.randint(0,19)
#       name = random.randint(1,2)
#       x2 = random.randint(0,19)
#       y2 = random.randint(0,19)
#       name2 = random.randint(3,4)
#       json = {name:[x,y], name2:[x2,y2]}
#       dict_data_for_screen(json, user_name, object_list)
#       time.sleep(1)


def temp_valami(user_name, chosen_color):
   while True:
      dict_data_for_screen(json_temp, user_name, chosen_color, object_list)
      time.sleep(1)


def start_loop(chosen_color):
   # TODO: Flexible window later
   turtle.setup(tile_size*tile_number, tile_size*tile_number, None, None)
   window = turtle.Screen()
   window.title("Arena")
   window.bgcolor("lightgreen")

   temp_valami(user_name, chosen_color)
   window.mainloop()

if __name__ == "__main__":
   start_loop(json_temp)
