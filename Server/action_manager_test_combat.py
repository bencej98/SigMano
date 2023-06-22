from gnome import Map, Gnome
from action_manager import ActionManager
import unittest

class TestActionManager(unittest.TestCase):
    def setUp(self):
        self.map = Map(10, 10, 2)
        self.gnome1 = Gnome("gnome1")
        self.gnome2 = Gnome("gnome2")
        self.action_manager = ActionManager()

    def test_combat(self):
        # Add gnomes to the map
        self.map.add_gnome_to_gnome_queue(self.gnome1)
        self.map.add_gnome_to_gnome_queue(self.gnome2)
        self.map.transfer_gnomes_to_active_gnomes()

        # Set the gnomes to the same location to ensure a fight
        self.gnome1.location = {"x": 5, "y": 5}
        self.gnome2.location = {"x": 5, "y": 5}

        # Run the combat method
        self.action_manager.combat(self.map)

        # Check that a fight occurred
        self.assertTrue(self.action_manager.was_fight)

        # Check that the event dictionary was updated correctly
        self.assertIn("gnome1", self.action_manager.event_dictionary)
        self.assertIn("gnome2", self.action_manager.event_dictionary)

    def test_check_combat_option(self):
        # Set the gnomes' stats so that gnome1 will kill gnome2
        self.gnome1.attack = 100
        self.gnome2.defense = 0
        self.gnome2.current_health = 1

        # Run the _check_combat_option method
        fight_message_dict = self.action_manager._check_combat_option(self.gnome1, self.gnome2)
        print(fight_message_dict)
        print(vars(self.gnome1))
        print(vars(self.gnome2))
        # Check that the outcome was correct
        self.assertEqual(fight_message_dict["outcome"], "gnome1 killed gnome2")

        # Check that gnome2 is dead and gnome1 got a kill
        self.assertTrue(self.gnome2.isdead)
        self.assertEqual(self.gnome1.kill_count, 1)

if __name__ == "__main__":
    unittest.main()
