class Fan:
    def __int__(self, max_fan_rpm):
        self.__max_rpm = max_fan_rpm
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
    def __init__(self, num_subsystems, fans_present):
        self.subsystems = [Subsystem()] * num_subsystems
        self.fans = []
        
        for i in range(num_fans):
            # need error checking for fan max speed
            max_speed = int(input(f"What is the max speed of fan {i + 1}? "))
            fans.append(Fan(max_speed))
            
        for i, subsystem in enumerate(self.subsystems):
            temp = int(input(f"What is the current temperature of subsystem {i + 1}? "))
            subsystem.set_temperature(temp)
            max_temp = max(max_temp, temp)
            update_fan_percent_max_rpm(max_temp)

    def update_fan_percent_max_rpm(self, curr_temps_max):
        fan_speed_percent = float(0);

        if curr_temps_max <= 25:
            fan_speed_percent = 0.2
        elif curr_temps_max > 75:
            fan_speed_percent = 1.0
        else:
            fan_speed_percent = 0.016 * curr_temps_max - 0.2
        
        for fan in self.fans:
            fan.set_speed(fan_speed_percent * fan.max_rpm)

        #iterate through list of fan objects with set_fan_speed_percent
    
### Put these functions in own file###
def get_valid_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print(f"\nInput not valid. Please enter a number.")
        except EOFError:
            print(f"\nNo input given. Please enter a number.")
#######################################
            
num_subsystems = get_valid_input("How many subsystems are there?")
fans_present = get_valid_input("How many fans are there?")
robot = Robot(num_subsystems, fans_present)

# give it some inital temp, then based on current temp, then change the temp to act accordingly. 



    
# def update_dashboard()
#     # landing page
#     # tkinter for gui?
#     # save to csv file
        