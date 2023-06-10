import turtle
import time
import random

class Player(turtle.Turtle):
   def __init__(self, name:str, x:int, y:int, color:str, size:float):
      super().__init__()
      self.penup()
      self.name = name
      self.goto(x, y)
      self.color(color)
      self.size = size
      self.shapesize(size)
      self.shape("circle")
      self.name1 = turtle.Turtle()
      self.name1.color(color)
      self.name1.hideturtle()
      self.name1.penup()
      self.name1.goto(x, y+10*size)
      self.name1.write(name, False, "center")

   def move(self, x:int, y:int):
      x = tile_size*(x-9.5)
      y = tile_size*(y-9.5)
      self.name1.goto(x, y+self.size*10)
      self.name1.clear()
      self.goto(x, y)
      self.name1.write(self.name, False, "center")

tile_size = 30
tile_number = 20

# TODO: Flexible window later

turtle.setup(tile_size*tile_number, tile_size*tile_number, None, None)
window = turtle.Screen()
window.title("Arena")
window.bgcolor("lightgreen")

Player1 = Player("Marine", -tile_size*9.5 , tile_size*0.5, "red", tile_size/60)
Player2 = Player("Zerling", -tile_size*9.5 , tile_size*1.5, "black", tile_size/60)
Player3 = Player("Zealot", -tile_size*9.5 , tile_size*2.5, "blue", tile_size/60)


for i in range(100):
   x = random.randint(0,19)
   y = random.randint(0,19)
   Player1.move(x, y)
   x = random.randint(0,19)
   y = random.randint(0,19)
   Player2.move(x, y)
   x = random.randint(0,19)
   y = random.randint(0,19)
   Player3.move(x,y)
   #time.sleep(1)

window.mainloop()