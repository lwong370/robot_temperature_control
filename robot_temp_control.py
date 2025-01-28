from utils import write_to_csv, check_valid_input, read_csv
from datetime import datetime
import time

class Fan:
    def __init__(self, max_fan_rpm):
        self.max_rpm = max_fan_rpm
        self.__curr_speed = 0
    
    def set_speed(self, new_speed):
        self.__curr_speed = new_speed
    
    def get_speed(self):
        return self.__curr_speed
        
class Subsystem:
    def __init__(self, curr_temp):
        self.__curr_temperature = curr_temp
    
    def set_temperature(self, new_temperature):
        self.__curr_temperature = new_temperature
    
    def get_temperature(self):
        return self.__curr_temperature
    
class Robot():
    def __init__(self, num_subsystems, num_fans):
        self.subsystems = [Subsystem(0.0) for _ in range(num_subsystems)]
        self.fans = []
        
        for i in range(num_fans):
            # need error checking for fan max speed
            max_speed = check_valid_input(f"What is the max speed (RPM) of fan {i + 1}? ", int)
            self.fans.append(Fan(max_speed))

    def update_subsystem_temperatures(self):
        file_name = "temperature_input_data.csv"
        temp_generate = read_csv(file_name, len(self.subsystems))
        for row in temp_generate:
            for subsystem, temp in zip(self.subsystems, row):
                subsystem.set_temperature(float(temp))
            
            # Calculate the maximum temperature and adjust fan speeds
            max_temp = max(subsystem.get_temperature() for subsystem in self.subsystems)
            self.__update_fan_percent_max_rpm(max_temp)

            # Optionally log or print here
            self.print_fan_speeds()
            self.log_data()
            
            # Wait 2 seconds before fetching the next row
            time.sleep(4)

    # Old code that asks the user for temp change         
    # def update_subsystem_temperatures(self):
        # for i, subsystem in enumerate(self.subsystems):
        #     # temp = check_valid_input(f"What is the current temperature (C) of subsystem {i + 1}? ", float)

            
        #     subsystem.set_temperature(temp)
        # max_temp = max([subsystem.get_temperature() for subsystem in self.subsystems])
        # self.__update_fan_percent_max_rpm(max_temp)

    def print_fan_speeds(self):
        for i, fan in enumerate(self.fans):
            print(f"Fan {i + 1} running at {fan.get_speed():.3f} RPM")
        
    def log_data(self, filename="./robot_data_log.csv"):
        # Get data to log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        subsystem_temps = [subsystem.get_temperature() for subsystem in self.subsystems]
        fan_speeds = [fan.get_speed() for fan in self.fans]

        header = ["Timestamp"] + \
        [f"Subsystem {i + 1} Temperature (C)" for i in range(len(self.subsystems))] + \
        [f"Fan {i + 1} Speed (RPM)" for i in range(len(self.fans))]
        row = [timestamp] + subsystem_temps + fan_speeds

        write_to_csv(filename, header, row)

    def __update_fan_percent_max_rpm(self, curr_temps_max):
        fan_speed_percent = float(0)

        if curr_temps_max <= 25.0:
            fan_speed_percent = 0.2
        elif curr_temps_max > 75.0:
            fan_speed_percent = 1.0
        else:
            fan_speed_percent = 0.016 * curr_temps_max - 0.2
        
        for fan in self.fans:
            fan.set_speed(fan_speed_percent * fan.max_rpm)
    
# Run Program
num_subsystems = check_valid_input("How many subsystems are there? ", int)
fans_present = check_valid_input("How many fans are there? ", int)
robot = Robot(num_subsystems, fans_present)

robot.update_subsystem_temperatures()
robot.print_fan_speeds()
robot.log_data()

while True:
    update_again = check_valid_input("Would you like to update the temperatures again? (y/n) ", str)
    if update_again != "y":
        break
    else:
        robot.update_subsystem_temperatures()
        robot.print_fan_speeds()
        robot.log_data()


# IDEAS:
# give it some inital temp, then based on current temp, then change the temp to act accordingly. 
# make unit tests


# def update_dashboard()
#     # landing page
#     # tkinter for gui?
#     # save to csv file
        