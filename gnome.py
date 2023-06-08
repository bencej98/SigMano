import random

class Gnome:
    def __init__(self, name, user) -> None:
        self.name = name
        self.user = user
        self.location = {}
        self.strategy = []
        self.event_counter = 0
        self.actual_points = 0
        self.kill_count = 0

    def spawn_gnome(self, map):
        self.location["x"] = random.randint(0, map.x_coordinate)
        self.location["y"] = random.randint(0, map.y_coordinate)

    def random_move(self, map):

        direction=random.randint(0,7)
        coordinate_is_valid = False
        random_counter = 0
        while coordinate_is_valid == False and random_counter < 20:
            temp_coord=self.location.copy()
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
            coordinate_is_valid = self.check_if_location_is_valid(temp_coord, map)
            random_counter += 1

        if random_counter < 20:
            self.location = temp_coord
        random_counter = 0

            
    def check_if_location_is_valid(self, coord, map):
        if map.x_coordinate >= coord["x"] >= 0 and map.y_coordinate >= coord["y"] >= 0:
            return True
        return False


class Map:
    def __init__(self, max_x, max_y) -> None:
        self.x_coordinate = max_x
        self.y_coordinate = max_y
        self.active_gnomes = {}

    def add_gnome_to_active_gnomes(self, *gnomes: Gnome) -> None:
        for gnome in gnomes:
            gnome.spawn_gnome(self)
            self.active_gnomes[gnome.name] = gnome

gnome1 = Gnome("lol", "loluser")
gnome2 = Gnome("lol2", "loluser2")

map = Map(20, 20)
map.add_gnome_to_active_gnomes(gnome1, gnome2)

if __name__ == "__main__":
    for gnome_name, gnome in map.active_gnomes.items():
        print(gnome_name, gnome.location["x"], gnome.location["y"])
        for valami in range(20):
            gnome.random_move(map)
            print(gnome_name, gnome.location["x"], gnome.location["y"])



