import turtle
import time
import random
import tkinter

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
      [x, y] = x_y_for_screen([x, y])
      self.name1.goto(x, y+self.size*10)
      self.name1.clear()
      self.goto(x, y)
      self.name1.write(self.name, False, "center")

tile_size = 30
tile_number = 20

def x_y_for_screen(coordinates:list):
   x = tile_size*(coordinates[0]+0.5)
   y = tile_size*(coordinates[1]-9.5)
   return [x, y]

def create_object(object_name:str, coordinates:list, user_name, chosen_color):
   [x, y] = x_y_for_screen(coordinates)
   if user_name == object_name:
      obj = Player(object_name, x, y, chosen_color, tile_size/60, 2)
   else:
      obj = Player(object_name, x, y, "black", tile_size/60, 2)
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
json_temp = {}
user_name = 1
events = []
leader_board = []

def set_temp_json(dict_obj):
   global json_temp
   json_temp = dict_obj

def set_username(username):
   global user_name
   user_name = username

def set_fight_event(fight_event):
   print(fight_event)

def set_leader_board(order_leader_list):
   print(order_leader_list)

def set_dead_list(dead_str):
   print(dead_str)

def temp_valami(root, user_name, chosen_color):
   while True:
      event_text = list_to_string(events)
      event = tkinter.Label(root.master, text=event_text, width=82, justify='left')
      event.place(x=9,y=360)
      leader_text = list_to_string(leader_board)
      leader = tkinter.Label(root.master, text=leader_text,justify='left')
      leader.place(x=20,y=60)
      dict_data_for_screen(json_temp, user_name, chosen_color, object_list)
      time.sleep(1)

def list_to_string(list:list) -> str:
   text = ""
   for i in list:
      text = text + "\n" + i
   return text[2:]


def event_updater(new_event:str):
   if len(events) >= 10:
      events.pop(0)
   events.append(new_event)


def leaderboard_updater(leader_list):
   n = 1
   for i in leader_list:
      [key,value] = i.items()
      leader_board.append(f"{n}. {key} with {value} point(s)")

def set_fight_event(event):
   event_updater(event)

def set_dead_list(dead_str):
   event_updater(dead_str)

def set_leader_board(order_leader_list):
   leaderboard_updater(order_leader_list)


def set_screen(root, x,y):
   line = turtle.Turtle()
   line.color("black")
   line.hideturtle()
   line.speed(0)
   line.penup()
   line.goto(-10,0)
   line.pendown()
   line.goto(-x, 0)
   line.penup()
   line.goto(-10, y/2)
   line.pendown()
   line.goto(-10, -y/2)
   leaderboard = tkinter.Label(root.master, text="LEADERBORD",font=(25))
   leaderboard.place(x=240,y=20)
   message = tkinter.Label(root.master, text="EVENTS",font=(25))
   message.place(x=260,y=320)




def start_loop(chosen_color):
   # TODO: Flexible window later
   turtle.setup(2*tile_size*tile_number, tile_size*tile_number, None, None)
   window = turtle.Screen()
   window.title("Arena")
   window.bgcolor("lightgreen")
   root = window.getcanvas()
   set_screen(root, tile_size*tile_number, tile_size*tile_number)
   time.sleep(0.3)
   temp_valami(root, user_name, chosen_color)
   window.mainloop()

if __name__ == "__main__":
   start_loop(json_temp)
