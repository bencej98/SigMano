from gnome import Map, Gnome

class ActionManager:
    def __init__(self) -> None:
        self.collided_gnomes = {}
        self.event_dictionary = {}
        self.user_strategies = {}
        #TODO
        self.was_fight = False
        self.was_death = False
        
    def _get_collided_gnomes(self, map: Map):
        self.collided_gnomes = map.check_collisions()
    
    def update_gnomes_strategy(self, map: Map, client_strategy: list, username: str):
        self.user_strategies[username] = client_strategy
        updated_gnomes = []
        for user, strategy in self.user_strategies.items():
            if user not in map.active_gnomes:
                for gnome in map.gnome_queue:
                    if gnome.user == user:
                        gnome.update_strategy(strategy)
                        gnome.event_counter = 0
                        updated_gnomes.append(user)
        for user in updated_gnomes:
            del self.user_strategies[user]

    def fight(self, map):
        self.was_fight = False
        self.event_dictionary = {}
        self._get_collided_gnomes(map)
        if len(self.collided_gnomes) > 0:
            self.was_fight = True
            for gnomes in self.collided_gnomes.values():
                for i, gnome in enumerate(gnomes):
                    if i < len(gnomes) - 1:
                        for j in range(i+1, len(gnomes)):
                            gnome_first = gnome
                            gnome_second = gnomes[j]
                            fight_message_dict = self._check_fight_option(gnome_first, gnome_second)
                            if gnome_first.user in self.event_dictionary:
                                self.event_dictionary[gnome_first.user].append(fight_message_dict)
                            else:
                                self.event_dictionary[gnome_first.user] = [fight_message_dict]
                            if gnome_second.user in self.event_dictionary:
                                self.event_dictionary[gnome_second.user].append(fight_message_dict)
                            else:
                                self.event_dictionary[gnome_second.user] = [fight_message_dict]
                            gnome_first.increase_event_counter()
                            gnome_second.increase_event_counter()
        return self.event_dictionary
    
    def check_gnome_death(self, map: Map):
        self.was_death = False
        gnome_deathnote = []
        for gnome_name, gnome in map.active_gnomes.items():
            if gnome.lose_count >= 3:
                gnome_deathnote.append(gnome_name)
        
        death_payload = []
        for gnome_name in gnome_deathnote():
            death_dict = {}
            dead_gnome = map.active_gnomes[gnome_name]
            death_dict["user"] = dead_gnome.user
            death_dict["score"] = dead_gnome.actual_points
            death_dict["kills"] = dead_gnome.kill_count
            death_payload.append(death_dict)

        for gnome_name in gnome_deathnote:
            dead_gnome = map.active_gnomes.pop(gnome_name)
            dead_gnome.event_counter = 0
            dead_gnome.actual_points = 0
            dead_gnome.kill_count = 0
            dead_gnome.lose_count = 0
            map.add_gnome_to_gnome_queue(dead_gnome)
        
        return {
            "Type": "Death",
            "Payload": death_payload
                }
    
    def move_all_gnomes(self, map: Map):
        map.update_gnomes_distances()
        position_update_dict = {}
        for gnome_name, gnome in map.active_gnomes.items():
            if gnome.direction == None:
                gnome.random_move(map)
            else:
                gnome.move_towards_direction(map)
            position = (gnome.location["x"], gnome.location["y"])
            position_update_dict[gnome.user] = position
        position_update_for_client = {"Type": "Position", "Payload": position_update_dict}
        return position_update_for_client

    def _set_target_towards_fight(self, gnome: Gnome, map: Map):
        if gnome.has_reached_target():
            closest_fight_distance = map.x_coordinate
            closest_fight_location = {}
            for fight_location in self.collided_gnomes:
                position_dict = {"x": fight_location[0], "y":fight_location[1]}
                figth_vector = map.calculate_distance(gnome.location, position_dict)
                if figth_vector["distance"] < closest_fight_distance:
                    closest_fight_distance = figth_vector["distance"]
                    closest_fight_location["x"] = fight_location[0]
                    closest_fight_location["y"] = fight_location[1]

            gnome.target_location = closest_fight_location
            gnome.update_direction(map)

    def check_action(self, gnome: Gnome, strategy):
        if strategy["action"] == "runaway":
            gnome.turn_against_direction()
        elif strategy["action"] == "approach":
            pass


    def choose_strategy(self, map: Map):
        for gnome_name, gnome in map.active_gnomes:
            if len(gnome.target_location) == 0:
                for strategy in gnome.event_reactions:
                    if strategy["event"] == "fight" and self.was_fight:
                        self._set_target_towards_fight(gnome)
                        self.check_action(gnome, strategy)
                    else:
                        gnome.direction = None


    def _check_fight_option(self, gnome_first, gnome_second):
        gnome_first_action = gnome_first.strategy[gnome_first.event_counter]
        gnome_second_action = gnome_second.strategy[gnome_second.event_counter]
        encounter = f"{gnome_first.user} used {gnome_first_action} and {gnome_second.user} used {gnome_second_action}"
        fight_message_dict = {
                    "encounter": encounter,
                    "outcome": ""
                }
        match (gnome_first_action, gnome_second_action):
            case ("rock", "paper") | ("paper", "scissor") | ("scissor", "rock"):
                print(f"{gnome_second.user} won")
                gnome_second.actual_points += 1
                gnome_second.kill_count += 1
                gnome_first.actual_points -= 1
                gnome_first.lose_count += 1
                outcome = f"{gnome_second.user} won"
                fight_message_dict["outcome"] = outcome
                return fight_message_dict
            case ("rock", "scissor") | ("paper", "rock") | ("scissor", "paper"):
                print(f"{gnome_first.user} won")
                gnome_first.actual_points += 1
                gnome_first.kill_count += 1
                gnome_second.actual_points -= 1
                gnome_second.lose_count += 1
                outcome = f"{gnome_first.user} won"
                fight_message_dict["outcome"] = outcome
                return fight_message_dict
            case _:
                print("tie") 
                outcome = "tie"
                fight_message_dict["outcome"] = outcome
                return fight_message_dict

