import random

class Gnome:
    def __init__(self, user) -> None:
        self.user = user
        self.location = {}
        self.strategy = []
        self.other_gnomes_dist = {}
        self.actual_points = 0
        self.kill_count = 0
        self.target_location = {}
        self.direction = 20
        self.max_health = 100
        self.current_health = 100
        self.attack = 5
        self.defense = 2
        self.isdead = False
        self.action_mode = None
        self.reached_target = False

    def fight_gnome(self, gnome):
        if self.isdead != True and gnome.isdead != True:
            gnome.current_health -= max(1, self.attack - gnome.defense)

    def check_if_dead(self):
        if self.current_health <= 0:
            self.isdead = True

    def apply_action_buffs(self):
        if self.action_mode == "Approach":
            self.attack += 5
        elif self.action_mode == "Defend":
            self.defense += 3
        elif self.action_mode == "Runaway":
            self.defense -= 1
    
    def remove_action_buffs(self):
        self.attack = 10
        self.defense = 2

    def spawn_gnome(self, map):
        self.isdead = False
        self.current_health = self.max_health
        self.location["x"] = random.randint(0, map.x_coordinate)
        self.location["y"] = random.randint(0, map.y_coordinate)
        self.target_location["x"] = self.location["x"]
        self.target_location["y"] = self.location["y"]

    def has_reached_target(self):
        if self.target_location["x"] == self.location["x"] and self.target_location["y"] == self.location["y"]:
            self.action_mode = None
            self.reached_target = True

    def set_runaway_target_location(self, map, target_location):
        vector_to_target = {
            "x": target_location["x"] - self.location["x"],
            "y": target_location["y"] - self.location["y"]
        }

        vector_away_from_target = {
            "x": -vector_to_target["x"],
            "y": -vector_to_target["y"]
        }

        new_target_location = {
            "x": self.location["x"] + vector_away_from_target["x"],
            "y": self.location["y"] + vector_away_from_target["y"]
        }

        new_target_location["x"] = max(0, min(map.x_coordinate, new_target_location["x"]))
        new_target_location["y"] = max(0, min(map.y_coordinate, new_target_location["y"]))

        self.target_location = new_target_location
        
    def update_strategy(self, strategy_list: list):
        self.strategy = strategy_list

    def _check_random_direction(self, map):
        direction_list = [0, 1, 2, 3, 4, 5, 6, 7]
        while True:
            rand = random.randint(0, len(direction_list) - 1)
            direction = direction_list.pop(rand)
            if self._validate_movement(direction, map):
                return direction

    def _validate_movement(self, direction, map):
        is_valid = False
        x = self.location["x"]
        y = self.location["y"]
        map_x = map.x_coordinate
        map_y = map.y_coordinate
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
        self._move_by_direction(direction)
        self.update_direction(map)

    def move_towards_direction(self, map):
        is_direction_valid = self._validate_movement(self.direction, map)
        if is_direction_valid:
            self._move_by_direction(self.direction)
        else:
            first_alter_direction = self._direction_converter(self.direction + 1)
            second_alter_direction = self._direction_converter(self.direction - 1)
            if self._validate_movement(first_alter_direction, map):
                self._move_by_direction(first_alter_direction)
            elif self._validate_movement(second_alter_direction, map):
                self._move_by_direction(second_alter_direction)
            else:
                self.random_move(map)

    def update_direction(self, map):
        relative_x = self.target_location["x"] - self.location["x"]
        relative_y = self.target_location["y"] - self.location["y"]
        self.direction = map.convert_unit_to_direction((relative_x, relative_y))

    def _direction_converter(self,direction):
        converted_direction = direction
        if direction == 8:
            converted_direction = 0
        elif direction == -1:
            converted_direction = 7
        
        return converted_direction

    def turn_against_direction(self):
        if self.direction == 0 or self.direction == 1 or self.direction == 2 or self.direction == 3:
            self.direction + 4
        else:
            self.direction - 4

    def _move_by_direction(self, direction):
        match direction:
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

class Map:
    def __init__(self, max_x, max_y, maximum_gnomes) -> None:
        self.x_coordinate = max_x
        self.y_coordinate = max_y
        self.maximum_gnomes = maximum_gnomes
        self.active_gnomes = {}
        self.gnome_queue = []
        self.all_gnomes = {}
        self.fight_locations = {}

    def add_gnome_to_gnome_queue(self, gnome: Gnome) -> None:
        self.gnome_queue.append(gnome)

    def transfer_gnomes_to_active_gnomes(self) -> None:
        while len(self.active_gnomes) < self.maximum_gnomes and len(self.gnome_queue) > 0:
            gnome = self.gnome_queue.pop(0)
            gnome.spawn_gnome(self)
            self.active_gnomes[gnome.user] = gnome

    def check_collisions(self):
        position_dict = {}
        for gnome in self.active_gnomes.values():
            position = (gnome.location["x"], gnome.location["y"])
            if position in position_dict:
                position_dict[position].append(gnome)
            else:
                position_dict[position] = [gnome]
        positions_with_collided_gnomes = {}
        for position, gnomes in position_dict.items():
            if len(gnomes) > 1:
                positions_with_collided_gnomes[position] = gnomes
        return positions_with_collided_gnomes
    
    def update_gnomes_distances(self):
        for gnome_name in self.active_gnomes:
            gnome = self.active_gnomes[gnome_name]
            gnome.other_gnomes_dist = {}
            for other_gnome_name in self.active_gnomes:
                if gnome_name != other_gnome_name:
                    other_gnome = self.active_gnomes[other_gnome_name]
                    gnome.other_gnomes_dist[other_gnome_name] = \
                        self.calculate_distance(gnome.location, other_gnome.location)

    def calculate_distance(self, base_location, target_location):
        x = base_location["x"] - target_location["x"]
        y = base_location["y"] - target_location["y"]
        abs_y = abs(y)
        abs_x = abs(x)

        if abs_x <= abs_y:
            distance = abs_y
        else:
            distance = abs_x
        
        return {"distance": distance, "direction": self.convert_unit_to_direction([x, y])}
    
    def _convert_dist_vector_to_unit(self, vector):
        x = vector[0]
        y = vector[1]

        if x < 0:
            x = -1
        elif 0 < x:
            x = 1

        if y < 0:
            y = -1
        elif 0 < y:
            y = 1


        return x, y

    def convert_unit_to_direction(self, vector):
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
    
    
