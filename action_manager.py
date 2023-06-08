from gnome import Gnome, Map

class ActionManager:
    def __init__(self, gnome_first: Gnome, gnome_second: Gnome) -> None:
        self.gnome_first = gnome_first
        self.gnome_second = gnome_second

    def fight(self):
        gnome_first_action = self.gnome_first.strategy[self.gnome_first.event_counter]
        gnome_second_action = self.gnome_second.strategy[self.gnome_second.event_counter]
        match (gnome_first_action, gnome_second_action):
            case ("stone", "paper") | ("paper", "scissor") | ("scissor", "stone"):
                print(f"{self.gnome_second.name} won")
                self.gnome_second.actual_points += 1
                self.gnome_second.kill_count += 1
                self.gnome_first.actual_points -= 1
            case ("stone", "scissor") | ("paper", "stone") | ("scissor", "paper"):
                print(f"{self.gnome_first.name} won")
                self.gnome_first.actual_points += 1
                self.gnome_first.kill_count += 1
                self.gnome_second.actual_points -= 1
            case _:
                print("tie")
        self.gnome_first.event_counter += 1
        self.gnome_second.event_counter += 1

gnome1 = Gnome("a", "a")
gnome2 = Gnome("b", "b")
list1 = ["stone", "stone", "stone", "stone", "scissor", "paper","paper", "paper","scissor","paper"]
list2 = ["paper","scissor", "stone","scissor","paper","stone", "stone", "stone", "stone", "stone"]
gnome1.strategy = list1
gnome2.strategy = list2
manager=ActionManager(gnome1, gnome2)
for i in range(10):
    manager.fight()

