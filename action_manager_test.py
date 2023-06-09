import unittest
from unittest.mock import Mock
from gnome import Map, Gnome
from action_manager import ActionManager

class TestActionManager(unittest.TestCase):
    
    def setUp(self):
        self.map = Map(10, 10)  # creating an instance of the Map with dimensions 10x10
        self.action_manager = ActionManager()  # creating an instance of the ActionManager

 

        # creating 3 gnomes
        self.gnome1 = Gnome("user1")
        self.gnome2 = Gnome("user2")
        self.gnome3 = Gnome("user3")

 

        # adding the gnomes to the map
        self.map.add_gnome_to_active_gnomes(self.gnome1, self.gnome2, self.gnome3)

        self.list1 = ["rock", "rock", "rock", "rock", "scissor", "paper","paper", "paper","scissor","paper"]
        self.list2 = ["paper","scissor", "rock","scissor","paper","rock", "rock", "rock", "rock", "rock"]
        self.list3 = ["scissor","paper", "paper","scissor","rock","paper", "rock", "scissor", "rock", "scissor"]
        self.gnome1.strategy = self.list1
        self.gnome2.strategy = self.list2
        self.gnome3.strategy = self.list3
        self.gnome2.event_counter = 1


 

    def test_fight(self):
        # First we need to ensure that all the gnomes are in the same location
        # Since we don't have a method to set the location of the gnomes,
        # we have to manually set the location of the gnomes
        self.gnome1.location = {"x": 1, "y": 1}
        self.gnome2.location = {"x": 1, "y": 1}
        self.gnome3.location = {"x": 1, "y": 1}

 

        # Then, we call the fight method
        test_dict = self.action_manager.fight(self.map)
        print(test_dict)
        # Now we can assert the conditions we expect after the fight
        # For example, we might expect that at least one gnome has won a fight and got a point
        self.assertTrue(any(gnome.actual_points > 0 for gnome in [self.gnome1, self.gnome2, self.gnome3]))

 

        # Or that the total kill count is the number of fights (in this case, 3 fights)
        total_kill_count = sum(gnome.kill_count for gnome in [self.gnome1, self.gnome2, self.gnome3])
        self.assertEqual(total_kill_count, 3)

if __name__ == "__main__":
    unittest.main()
    