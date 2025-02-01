import unittest
from unittest.mock import patch
from utils import write_to_csv
from robot_components import Fan, Subsystem, Robot

class TestRobot(unittest.TestCase):
    def setUp(self):
        # Initialize robot
        self.robot = Robot(num_subsystems=2, num_fans=2, fans=[Fan(344.222), Fan(254), Fan(207.30)])

    def test_initialization(self):
        self.assertEqual(len(self.robot.subsystems), 2)
        self.assertEqual(len(self.robot.fans), 3)

        self.assertEqual(self.robot.fans[0].get_max_rpm(), 344.222)
        self.assertEqual(self.robot.fans[1].get_max_rpm(), 254)
        self.assertEqual(self.robot.fans[2].get_max_rpm(), 207.30)

    def test_update_fan_rpm_float_rounding(self):
        # Temp = 25 Celsius --> 20% of max RPM
        self.robot._update_fan_percent_max_rpm(25.0)
        self.assertEqual(self.robot.fans[0].get_speed(), 68.844)  
        self.assertEqual(self.robot.fans[1].get_speed(), 50.8) 
        self.assertEqual(self.robot.fans[2].get_speed(), 41.46)

        # Temp = 25 Celsius --> linear interpolation of max RPM
        self.robot._update_fan_percent_max_rpm(46.0)
        self.assertEqual(self.robot.fans[0].get_speed(), 184.503)  
        self.assertEqual(self.robot.fans[1].get_speed(), 136.144)
        self.assertEqual(self.robot.fans[2].get_speed(), 111.113)
 
        # Temp = 85 Celsius --> 100% of max RPM
        self.robot._update_fan_percent_max_rpm(85.0)
        self.assertEqual(self.robot.fans[0].get_speed(), 344.222)
        self.assertEqual(self.robot.fans[1].get_speed(), 254)
        self.assertEqual(self.robot.fans[2].get_speed(), 207.30) 

    def test_invalid_user_inputs(self):
        invalid_input_counts = [-3, 0, "three", None]
        invalid_fans = [Fan(-10), Fan("three"), Fan("slow")]

        # Tests invalid inputs for number of subsystems
        for subsystems in invalid_input_counts:
            with self.subTest(subsystems=subsystems):
                with self.assertRaises(ValueError):
                    Robot(num_subsystems=subsystems, num_fans=3, fans=[Fan(300), Fan(200)])

        # Tests invalid inputs for number of fans
        for fans_count in invalid_input_counts:
            with self.subTest(fans_count=fans_count):
                with self.assertRaises(ValueError):
                    Robot(num_subsystems=2, num_fans=fans_count, fans=[Fan(300), Fan(200)])
        
        # Tests invalid inputs for fan max RPMs
        for fans in invalid_fans:
            with self.subTest(fans=fans):
                with self.assertRaises(ValueError):
                    Robot(num_subsystems=2, num_fans=len(invalid_fans), fans=invalid_fans)

    def test_fan_zero_rpm(self):
        # Tests if setting a max fan RPM of 0 keeps output fan speed 0
        robot = Robot(num_subsystems=1, num_fans=1, fans=[Fan(0.0)])
        
        # Test with 47 Celsius, see if RPM stays 0
        robot._update_fan_percent_max_rpm(47.0)
        self.assertEquals(robot.fans[0].get_speed(), 0.0)


if __name__ == "__main__":
    unittest.main()

# random numbers --> close simulation

# invalid input --> adds wrong number of fans
# check if the rpm stays 0 if max rpm for that fan is 0! 

