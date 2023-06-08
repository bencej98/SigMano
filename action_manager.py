from gnome import Map

class ActionManager:
    def __init__(self) -> None:
        self.collided_gnomes = []

    def get_collided_gnomes(self, map: Map):
        self.collided_gnomes = map.check_collisions()

    def fight(self, map):
        self.get_collided_gnomes(map)
        if len(self.collided_gnomes) > 0:
            for gnomes in self.collided_gnomes:
                for i, gnome in enumerate(gnomes):
                    if i < len(gnomes):
                        for j in range(i+1, len(gnomes)):
                            gnome_first = gnome
                            gnome_second = gnomes[j]
                            self.check_fight_option(gnome_first, gnome_second)
                            gnome_first.increase_event_counter()
                            gnome_second.increase_event_counter()

    def check_fight_option(self, gnome_first, gnome_second):
        gnome_first_action = gnome_first.strategy[gnome_first.event_counter]
        gnome_second_action = gnome_second.strategy[gnome_second.event_counter]
        match (gnome_first_action, gnome_second_action):
            case ("stone", "paper") | ("paper", "scissor") | ("scissor", "stone"):
                print(f"{gnome_second.name} won")
                gnome_second.actual_points += 1
                gnome_second.kill_count += 1
                gnome_first.actual_points -= 1
            case ("stone", "scissor") | ("paper", "stone") | ("scissor", "paper"):
                print(f"{gnome_first.name} won")
                gnome_first.actual_points += 1
                gnome_first.kill_count += 1
                gnome_second.actual_points -= 1
            case _:
                print("tie") 