from utils import write_to_csv, check_valid_input, read_csv
from datetime import datetime
import time
import math

class Fan:
    def __init__(self, max_fan_rpm):
        self._max_rpm = max_fan_rpm
        self._curr_speed = 0
    
    def get_max_rpm(self):
        return self._max_rpm
    
    def set_speed(self, new_speed):
        self._curr_speed = new_speed
    
    def get_speed(self):
        return self._curr_speed
        
class Subsystem:
    def __init__(self, curr_temp):
        self._curr_temperature = curr_temp
    
    def set_temperature(self, new_temperature):
        self._curr_temperature = new_temperature
    
    def get_temperature(self):
        return self._curr_temperature
    
class Robot():
    def __init__(self, num_subsystems, num_fans, max_rpms):
        self.subsystems = [Subsystem(0.0) for _ in range(num_subsystems)]
        self.fans = max_rpms
        self.logging_file = f"./csv_files/robot_data_log_{num_subsystems}_subsystems_{num_fans}_fans.csv"

        # for i in num_fans:
        #     max_speed = check_valid_input(f"What is the max speed (RPM) of fan {i + 1}? ", float)
        #     self.fans.append(Fan(max_speed))
        
    # def set_fan_max_rpms(self, rpm_inputs):
    #     for value in rpm_inputs:
    #         # max_speed = check_valid_input(f"What is the max speed (RPM) of fan {i + 1}? ", float)
    #         self.fans = [Fan(float(value)) for value in rpm_inputs]

    def update_subsystem_temperatures(self, temp_input_file):
        file_name = temp_input_file
        temp_generate = read_csv(file_name, len(self.subsystems))
        for row in temp_generate:
            for i, (subsystem, temp) in enumerate(zip(self.subsystems, row), start=1):
                subsystem.set_temperature(float(temp))
                print(f"Subsystem {i} Temp (C): {subsystem.get_temperature()}")
            
            # Calculate the maximum temperature and adjust fan speeds
            max_temp = max(subsystem.get_temperature() for subsystem in self.subsystems)
            self.__update_fan_percent_max_rpm(max_temp)

            # Print to console and log data
            self.print_fan_speeds()
            print("------------------------------")
            self.log_data()
            
            # Wait 2 seconds before updating with new temperature
            time.sleep(4)

    def print_fan_speeds(self):
        for i, fan in enumerate(self.fans):
            print(f"Fan {i + 1} running at {fan.get_speed():.3f} RPM")
        
    def log_data(self):
        # Get data to log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        subsystem_temps = [float(f"{subsystem.get_temperature():.3f}") for subsystem in self.subsystems]
        fan_speeds = [float(f"{fan.get_speed():.3f}") for fan in self.fans]

        header = ["Timestamp"] + \
        [f"Subsystem {i + 1} Temperature (C)" for i in range(len(self.subsystems))] + \
        [f"Fan {i + 1} Speed (RPM)" for i in range(len(self.fans))]
        row = [timestamp] + subsystem_temps + fan_speeds

        write_to_csv(self.logging_file, header, row)

    def __update_fan_percent_max_rpm(self, curr_temps_max):
        fan_speed_percent = float(0)

        if curr_temps_max <= 25.0:
            fan_speed_percent = 0.2
        elif curr_temps_max > 75.0:
            fan_speed_percent = 1.0
        else:
            fan_speed_percent = 0.016 * curr_temps_max - 0.2
        
        for fan in self.fans:
            max_rpm = fan.get_max_rpm()

            # Set the speed, rounded to three decimal places
            fan.set_speed(fan_speed_percent * math.floor(max_rpm * 1000) / 1000.0)
            
        # for fan in self.fans:
        #     max_rpm = fan.get_max_rpm()
        #     if not isinstance(max_rpm, (int, float)):
        #         raise TypeError(f"Expected numeric max RPM but got {type(max_rpm)} with value {max_rpm}")
            
        #     fan.set_speed(round(fan_speed_percent * max_rpm, 3))

 
