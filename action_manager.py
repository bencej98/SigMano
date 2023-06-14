from gnome import Map

class ActionManager:
    def __init__(self) -> None:
        self.collided_gnomes = []
        self.event_dictionary = {}
        
    def _get_collided_gnomes(self, map: Map):
        self.collided_gnomes = map.check_collisions()
    
    def update_gnomes_strategy(self, map: Map, client_strategy: dict, username: str):
        update_strategy_message = {}
        update_strategy_message[username] = client_strategy["strategy"]
        for user, strategy in update_strategy_message:
            if user in map.active_gnomes:
                pass
            else:
                for gnome in map.gnome_queue:
                    if gnome.user == user:
                        gnome.update_strategy(strategy)
                        del update_strategy_message[user]
        

    def fight(self, map):
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
        
        for gnome_name in gnome_deathnote:
            dead_gnome = map.active_gnomes.pop(gnome_name)
            map.add_gnome_to_gnome_queue(dead_gnome)
        
        return {
            "Type": "Death",
            "Payload": gnome_deathnote
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

