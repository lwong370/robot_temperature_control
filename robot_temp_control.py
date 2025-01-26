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
        self.subsystems = [Subsystem(0.0)] * num_subsystems
        self.fans = []
        
        for i in range(num_fans):
            # need error checking for fan max speed
            max_speed = check_valid_int_input(f"What is the max speed of fan {i + 1}? ")
            self.fans.append(Fan(max_speed))
        
        self.update_subsystem_temperatures()
        
    def update_subsystem_temperatures(self):
        for i, subsystem in enumerate(self.subsystems):
            temp = check_valid_int_input(f"What is the current temperature of subsystem {i + 1}? ")
            subsystem.set_temperature(temp)
            max_temp = max([subsystem.get_temperature() for subsystem in self.subsystems])
            self.__update_fan_percent_max_rpm(max_temp)

    def __update_fan_percent_max_rpm(self, curr_temps_max):
        fan_speed_percent = float(0)

        if curr_temps_max <= 25:
            fan_speed_percent = 0.2
        elif curr_temps_max > 75:
            fan_speed_percent = 1.0
        else:
            fan_speed_percent = 0.016 * curr_temps_max - 0.2
        
        for fan in self.fans:
            fan.set_speed(fan_speed_percent * fan.max_rpm)
    
### Put these functions in own file###
def check_valid_int_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print(f"\nInput not valid. Please enter a number. ")
        except EOFError:
            print(f"\nNo input given. Please enter a number. ")
#######################################
            
num_subsystems = check_valid_int_input("How many subsystems are there? ")
fans_present = check_valid_int_input("How many fans are there? ")
robot = Robot(num_subsystems, fans_present)




# IDEAS:
# give it some inital temp, then based on current temp, then change the temp to act accordingly. 
    
# def update_dashboard()
#     # landing page
#     # tkinter for gui?
#     # save to csv file
        