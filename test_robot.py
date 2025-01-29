import unittest
from unittest.mock import patch
from utils import write_to_csv, check_valid_input, read_csv
from robot_components import Fan, Subsystem, Robot

class TestRobot(unittest.TestCase):
    def setUp(self):
        # Patch the check_valid_input directly
        patcher = patch("robot_temp_control.check_valid_input", side_effect=[523.0, 310])
        self.mock_check_valid_input = patcher.start()  # Start patching
        self.addCleanup(patcher.stop)  # Ensure it gets stopped after the test

        # Initialize robot
        self.robot = Robot(num_subsystems=2, num_fans=2)

    def test_initialization(self):
        self.assertEqual(len(self.robot.subsystems), 2)
        self.assertEqual(len(self.robot.fans), 2)

        self.assertEqual(self.robot.fans[0].get_max_rpm(), 523.0)
        self.assertEqual(self.robot.fans[1].get_max_rpm(), 310)

    def test_update_fan_percent_max_rpm(self):
        self.robot._Robot__update_fan_percent_max_rpm(25.0)
        self.assertEqual(self.robot.fans[0].get_speed(), 104.600)  
        self.assertEqual(self.robot.fans[1].get_speed(), 62.0)   

        self.robot._Robot__update_fan_percent_max_rpm(46.0)
        self.assertEqual(self.robot.fans[0].get_speed(), 280.328)  
        self.assertEqual(self.robot.fans[1].get_speed(), 166.16) 

        self.robot._Robot__update_fan_percent_max_rpm(85.0)
        self.assertEqual(self.robot.fans[0].get_speed(), 523.0)
        self.assertEqual(self.robot.fans[1].get_speed(), 310.0) 

if __name__ == "__main__":
    unittest.main()
