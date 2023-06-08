import random

class Gnome:
    def __init__(self, name, user) -> None:
        self.name = name
        self.user = user
        self.location = {}
        self.strategy = []
        self.health = 10
        self.attack = 3
        self.defense = 2

    def spawn_gnome(self, map):
        self.location["x"] = random.randint(0, map.x_coordinate)
        self.location["y"] = random.randint(0, map.y_coordinate)
        

class Map:
    def __init__(self) -> None:
        self.x_coordinate = 20
        self.y_coordinate = 20
        self.active_gnomes = {}

