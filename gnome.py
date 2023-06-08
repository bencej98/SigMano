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

    def random_move(self):
        temp_coord=self.location

        direction=random.randint(0,7)
        coordinate_is_valid = False
        while coordinate_is_valid == False:
            match direction:
                # 0 is up then clockwise
                case 0: 
                    temp_coord["y"] += 1 
                case 1: 
                    temp_coord["x"] += 1
                    temp_coord["y"] += 1 
                case 2: 
                    temp_coord["x"] +=1 
                case 3: 
                    temp_coord["x"] += 1
                    temp_coord["y"] -= 1  
                case 4: 
                    temp_coord["y"] -= 1 
                case 5: 
                    temp_coord["x"] -= 1
                    temp_coord["y"] -= 1 
                case 6: 
                    temp_coord["x"] -= 1 
                case 7: 
                    temp_coord["x"] -= 1
                    temp_coord["y"] += 1         
            coordinate_is_valid = self.check_if_location_is_valid(temp_coord)
        
        self.location = temp_coord

            


    def check_if_location_is_valid(map, coord):
        if map.x_coordinate >= coord["x"] >= 0 and map.y_coordinate >= coord["y"] >= 0:
            return True
        return False


class Map:
    def __init__(self) -> None:
        self.x_coordinate = 20
        self.y_coordinate = 20
        self.active_gnomes = {}

