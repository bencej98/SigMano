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

    def check_random_direction(self, map):
        x = self.location["x"]
        y = self.location["y"]
        map_x = map.x_coordinate
        map_y = map.y_coordinate
        direction_list = [0, 1, 2, 3, 4, 5, 6, 7]
        while True:
            rand = random.randint(0, len(direction_list) - 1)
            direction = direction_list.pop(rand)
            if x == 0 or y == 0 or x == map_x or y == map_y:
                if (x == 0 and y == 0) and (0 <= direction <= 2):
                    break
                elif (x == map_x and y == map_y) and (4 <= direction <= 6):
                    break
                elif (x == 0 and y == map_y) and (2 <= direction <= 4):
                    break
                elif (x == map_x and y == 0) and (direction in (0, 6, 7)):
                    break
                elif x == 0 and (0 <= direction <= 4):
                    break
                elif y == 0 and (0 <= direction <= 2 or direction in (6, 7)):
                    break
                elif x == map_x and (direction == 0 or 4 <= direction <= 7):
                    break
                elif y == map_y and (2 <= direction <= 6):
                    break
            else:
                break

        return direction

    def random_move(self, map):
        direction=self.check_random_direction(map)
        match direction:
            # 0 is up then clockwise
            case 0: 
                self.location["y"] += 1 
            case 1: 
                self.location["x"] += 1
                self.location["y"] += 1
            case 2: 
                self.location["x"] += 1 
            case 3: 
                self.location["x"] += 1
                self.location["y"] -= 1
            case 4: 
                self.location["y"] -= 1 
            case 5: 
                self.location["x"] -= 1
                self.location["y"] -= 1 
            case 6: 
                self.location["x"] -= 1 
            case 7: 
                self.location["x"] -= 1
                self.location["y"] += 1         
    
    def increase_event_counter(self):
        if self.event_counter < 9:
            self.event_counter += 1
        else:
            self.event_counter = 0


class Map:
    def __init__(self, max_x, max_y) -> None:
        self.x_coordinate = max_x
        self.y_coordinate = max_y
        self.active_gnomes = {}

    def add_gnome_to_active_gnomes(self, *gnomes: Gnome) -> None:
        for gnome in gnomes:
            gnome.spawn_gnome(self)
            self.active_gnomes[gnome.name] = gnome

    def check_collisions(self):
        collided_gnomes = []
        position_dict = {}
        for gnome_name, gnome in self.active_gnomes.items():
            position = (gnome.location["x"], gnome.location["y"])
            if position in position_dict:
                position_dict[position].append(gnome)
            else:
                position_dict[position] = [gnome]
        for position, gnomes in position_dict.items():
            if len(gnomes) > 1:
                collided_gnomes.append(gnomes)
        return collided_gnomes

    def move_all_gnomes(self):
        position_update_dict = {}
        for gnome_name, gnome in self.active_gnomes.items():
            gnome.random_move(self)
            position = (gnome.location["x"], gnome.location["y"])
            position_update_dict[gnome.user] = position
        return position_update_dict
    
#function check
if __name__ == "__main__":
    gnome1 = Gnome("lol", "loluser")
    gnome2 = Gnome("lol2", "loluser2")


    map = Map(19, 19)
    map.add_gnome_to_active_gnomes(gnome1, gnome2)
    gnome1.location = {"x": 0, "y": 5}
    for gnome_name, gnome in map.active_gnomes.items():
        print(gnome_name, gnome.location["x"], gnome.location["y"])
        for valami in range(20):
            gnome.random_move(map)
            print(gnome_name, gnome.location["x"], gnome.location["y"])


