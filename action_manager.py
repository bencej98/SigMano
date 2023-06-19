from gnome import Map

class ActionManager:
    def __init__(self) -> None:
        self.collided_gnomes = []
        self.event_dictionary = {}
        self.user_strategies = {}
        
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
        self.event_dictionary = {}
        self._get_collided_gnomes(map)
        if len(self.collided_gnomes) > 0:
            for gnomes in self.collided_gnomes:
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
            death_dict["lose_count"] = dead_gnome.kill_count
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
            "Payload": death_dict
                }

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

