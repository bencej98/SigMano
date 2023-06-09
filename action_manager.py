from gnome import Map

class ActionManager:
    def __init__(self) -> None:
        self.collided_gnomes = []
        self.event_dictionary = {}
        
    def get_collided_gnomes(self, map: Map):
        self.collided_gnomes = map.check_collisions()

    def fight(self, map):
        self.get_collided_gnomes(map)
        if len(self.collided_gnomes) > 0:
            for gnomes in self.collided_gnomes:
                for i, gnome in enumerate(gnomes):
                    if i < len(gnomes) - 1:
                        for j in range(i+1, len(gnomes)):
                            gnome_first = gnome
                            gnome_second = gnomes[j]
                            fight_message_dict = self.check_fight_option(gnome_first, gnome_second)
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

    def check_fight_option(self, gnome_first, gnome_second):
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
                outcome = f"{gnome_second.user} won"
                fight_message_dict["outcome"] = outcome
                return fight_message_dict
            case ("rock", "scissor") | ("paper", "rock") | ("scissor", "paper"):
                print(f"{gnome_first.user} won")
                gnome_first.actual_points += 1
                gnome_first.kill_count += 1
                gnome_second.actual_points -= 1
                outcome = f"{gnome_first.user} won"
                fight_message_dict["outcome"] = outcome
                return fight_message_dict
            case _:
                print("tie") 
                outcome = "tie"
                fight_message_dict["outcome"] = outcome
                return fight_message_dict

