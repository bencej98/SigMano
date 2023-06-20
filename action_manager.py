from gnome import Map, Gnome
import random
import heapq

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
                        updated_gnomes.append(user)
        for user in updated_gnomes:
            del self.user_strategies[user]

    def combat(self, map):
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
                            if gnome_first.isdead != True and gnome_second.isdead != True:
                                fight_message_dict = self._check_combat_option(gnome_first, gnome_second)
                                if gnome_first.user in self.event_dictionary:
                                    self.event_dictionary[gnome_first.user].append(fight_message_dict)
                                else:
                                    self.event_dictionary[gnome_first.user] = [fight_message_dict]
                                if gnome_second.user in self.event_dictionary:
                                    self.event_dictionary[gnome_second.user].append(fight_message_dict)
                                else:
                                    self.event_dictionary[gnome_second.user] = [fight_message_dict]
        return self.event_dictionary

    def _check_combat_option(self, gnome_one: Gnome, gnome_two: Gnome):
        gnome_one.apply_action_buffs()
        gnome_two.apply_action_buffs()
        encounter = f"{gnome_one.user} and {gnome_two.user} fought"
        fight_message_dict = {
                    "encounter": encounter,
                    "outcome": ""
                }
        
        gnomes = [gnome_one, gnome_two]
        random.shuffle(gnomes)
        gnome_first, gnome_second = gnomes
        gnome_first.fight_gnome(gnome_second)
        gnome_second.fight_gnome(gnome_first)
        gnome_first.actual_points += 15
        gnome_second.actual_points += 15
        gnome_first.remove_action_buffs()
        gnome_second.remove_action_buffs()       
        outcome = ""
        if gnome_first.current_health <= 0:
            gnome_second.kill_count += 1
            gnome_second.actual_points += 50
            gnome_first.isdead = True
            outcome = f"{gnome_second.user} killed {gnome_first.user}"
        elif gnome_second.current_health <= 0:
            gnome_first.kill_count += 1
            gnome_first.actual_points += 50
            gnome_second.isdead = True
            outcome = f"{gnome_first.user} killed {gnome_second.user}"
        fight_message_dict["outcome"] = outcome
        return fight_message_dict
    
    def participation_award(self, map: Map):
        for gnome in map.active_gnomes.values():
            gnome.actual_points += 1
    
    def check_gnome_death(self, map: Map):
        self.was_death = False
        gnome_deathnote = []
        for gnome_name, gnome in map.active_gnomes.items():
            gnome.check_if_dead()
            if gnome.isdead == True:
                gnome_deathnote.append(gnome_name)
        
        death_payload = []
        for gnome_name in gnome_deathnote:
            death_dict = {}
            dead_gnome = map.active_gnomes.pop(gnome_name)
            death_dict["user"] = dead_gnome.user
            death_dict["score"] = dead_gnome.actual_points
            death_dict["kills"] = dead_gnome.kill_count
            death_payload.append(death_dict)
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
        self.choose_strategy(map)
        for gnome_name, gnome in map.active_gnomes.items():
            if gnome.direction == 20:
                gnome.random_move(map)
            else:
                gnome.move_towards_direction(map)
            position = (gnome.location["x"], gnome.location["y"])
            position_update_dict[gnome.user] = position
        position_update_for_client = {"Type": "Position", "Payload": position_update_dict}
        return position_update_for_client

    def _set_target_towards_fight(self, gnome: Gnome, map: Map):
        closest_fight_distance = map.x_coordinate * 2
        closest_fight_location = {}
        for fight_location in self.collided_gnomes:
            position_dict = {"x": fight_location[0], "y":fight_location[1]}
            figth_vector = map.calculate_distance(gnome.location, position_dict)
            if figth_vector["distance"] <= closest_fight_distance:
                closest_fight_distance = figth_vector["distance"]
                closest_fight_location["x"] = fight_location[0]
                closest_fight_location["y"] = fight_location[1]

        return closest_fight_location

    def check_gnomes_in_range(self, gnome: Gnome, map: Map):
        gnomes_in_range = []
        for gnome_name, data in gnome.other_gnomes_dist.items():
            if data["distance"] <= 4:
                heapq.heappush(gnomes_in_range, (data["distance"], gnome_name))
        return [heapq.heappop(gnomes_in_range)[1] for _ in range(len(gnomes_in_range))]


    def check_action(self, gnome: Gnome, map, strategy, target_location):
        # if target_location == {}:
        #     target_location["x"] = map.x_coordinate
        #     target_location["y"] = map.y_coordinate
        if strategy["Action"] == "Runaway":
            gnome.set_runaway_target_location(map, target_location)
            gnome.update_direction(map)
        elif strategy["Action"] == "Approach":
            gnome.target_location = target_location
            gnome.action_mode = "Approach"
            gnome.update_direction(map)
        elif strategy["Action"] == "Defend":
            gnome.target_location = target_location
            gnome.action_mode = "Defend"
            gnome.update_direction(map)

    def choose_strategy(self, map: Map):
        for gnome_name, gnome in map.active_gnomes.items():
            gnome.has_reached_target()
            if gnome.reached_target == False or gnome.isdead == True:
                continue
            gnomes_in_range = self.check_gnomes_in_range(gnome, map)
            for strategy in gnome.strategy:
                if strategy["Event"] == "Fight happened" and self.was_fight:
                    closest_fight_location = self._set_target_towards_fight(gnome, map)
                    self.check_action(gnome, map, strategy, closest_fight_location)
                    break
                elif strategy["Event"] == "Gnomes in vicinity" and len(gnomes_in_range) > 0:
                    closest_gnome_location = map.active_gnomes[gnomes_in_range[0]].location
                    self.check_action(gnome, map, strategy, closest_gnome_location)
                    break



