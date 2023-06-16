import random
import math


class Gnome:
    def __init__(self, user) -> None:
        self.user = user
        self.location = {}
        self.strategy = []
        self.other_gnomes_dist = {}
        self.event_counter = 0
        self.actual_points = 0
        self.kill_count = 0
        self.lose_count = 0

    def spawn_gnome(self, map):
        self.location["x"] = random.randint(0, map.x_coordinate)
        self.location["y"] = random.randint(0, map.y_coordinate)

    def update_strategy(self, strategy_list: list):
        self.strategy = strategy_list

    def _check_random_direction(self, map):
        x = self.location["x"]
        y = self.location["y"]
        map_x = map.x_coordinate
        map_y = map.y_coordinate
        direction_list = [0, 1, 2, 3, 4, 5, 6, 7]
        is_valid2 = True
        while is_valid2:
            rand = random.randint(0, len(direction_list) - 1)
            direction = direction_list.pop(rand)
            is_valid2 = False
            while not self.validate_movement(x, y, direction, map_x, map_y):
                is_valid2 = True
                break
        return direction
    
    def check_direction(self, map, location, direction):
        pass

    def validate_movement(self, x, y, direction, map_x, map_y):
            is_valid = False
            if x == 0 or y == 0 or x == map_x or y == map_y:
                if (x == 0 and y == 0) and (0 <= direction <= 2):
                    is_valid = True
                elif (x == map_x and y == map_y) and (4 <= direction <= 6):
                    is_valid = True
                elif (x == 0 and y == map_y) and (2 <= direction <= 4):
                    is_valid = True
                elif (x == map_x and y == 0) and (direction in (0, 6, 7)):
                   is_valid = True
                elif (x == 0 and y != map_y and y != 0) and (0 <= direction <= 4):
                    is_valid = True
                elif (y == 0 and x != map_x and x != 0) and (0 <= direction <= 2 or direction in (6, 7)):
                    is_valid = True
                elif (x == map_x and y != 0 and y != map_y) and (direction == 0 or 4 <= direction <= 7):
                    is_valid = True
                elif (y == map_y and x != 0 and x != map_x) and (2 <= direction <= 6):
                   is_valid = True
            else:
                is_valid = True
            return is_valid

    
    def random_move(self, map):
        direction=self._check_random_direction(map)
        self.move_by_direction(direction)

    def move_by_direction(self, direction):
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
        if self.event_counter < len(self.strategy) - 1:
            self.event_counter += 1
        else:
            self.event_counter = 0


class Map:
    def __init__(self, max_x, max_y, maximum_gnomes) -> None:
        self.x_coordinate = max_x
        self.y_coordinate = max_y
        self.maximum_gnomes = maximum_gnomes
        self.active_gnomes = {}
        self.gnome_queue = []
        self.all_gnomes = {}

    def add_gnome_to_gnome_queue(self, gnome: Gnome) -> None:
        self.gnome_queue.append(gnome)

    def transfer_gnomes_to_active_gnomes(self) -> None:
        while len(self.active_gnomes) < self.maximum_gnomes and len(self.gnome_queue) > 0:
            gnome = self.gnome_queue.pop(0)
            gnome.spawn_gnome(self)
            self.active_gnomes[gnome.user] = gnome

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
        position_update_for_client = {"Type": "Position", "Payload": position_update_dict}
        return position_update_for_client
    
    def update_gnomes_distances(self):
        for gnome_name in self.active_gnomes:
            for other_gnome_name in self.active_gnomes:
                if gnome_name != other_gnome_name:
                    gnome = self.active_gnomes[gnome_name]
                    other_gnome = self.active_gnomes[other_gnome_name]
                    gnome.other_gnomes_dist[other_gnome_name] = self.calculate_distance(gnome, other_gnome)

    def calculate_distance(self, gnome: Gnome, other_gnome: Gnome):
        x = gnome.location["x"] - other_gnome.location["x"]
        y = gnome.location["y"] - other_gnome.location["y"]

        distance = math.sqrt((x * x) + (y * y))
        
        return [distance, self._convert_unit_to_direction([x, y])]
    
    def _convert_dist_vector_to_unit(vector):
        x = vector[0]
        y = vector[1]

        if x < - 0.5:
            x = -1
        elif -0.5 <= x <= 0.5:
            x = 0
        elif 0.5 < x:
            x = 1    

        if y < - 0.5:
            y = -1
        elif -0.5 <= y <= 0.5:
            y = 0
        elif 0.5 < y:
            y = 1

        return x, y

    def _convert_unit_to_direction(self, vector):
        converted_vector = self._convert_dist_vector_to_unit(vector)
        direction = 0
        x = converted_vector[0]
        y = converted_vector[1]
        if x == -1:
            if y == -1:
                direction = 5
            elif y == 0:
                direction = 6
            elif y ==1:
                direction = 7
        elif x == 0:
            if y == -1:
                direction = 4
            elif y == 0:
                direction = random.randint(0, 7)
            elif y ==1:
                direction = 0
        elif x == 1:
            if y == -1:
                direction = 3
            elif y == 0:
                direction = 2
            elif y ==1:
                direction = 1

        return direction
    
    
#function check
if __name__ == "__main__":
    gnomes_list = []
    for n in range (10):
        gnome = Gnome(f"loluser{n}")
        gnomes_list.append(gnome)

    map = Map(5, 5, 5)
    for gnome in gnomes_list:
        map.add_gnome_to_gnome_queue(gnome)
    map.transfer_gnomes_to_active_gnomes()

    for gnome_name, gnome in map.active_gnomes.items():
        print(gnome_name, gnome.location["x"], gnome.location["y"])
        for valami in range(20):
            gnome.random_move(map)
            print(gnome_name, gnome.location["x"], gnome.location["y"])
    position_dict = map.move_all_gnomes()
    print(position_dict)
    print(map.active_gnomes)
    print(map.gnome_queue)
