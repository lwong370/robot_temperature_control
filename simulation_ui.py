import tkinter as tk
from tkinter import messagebox
from robot_components import Robot, Fan
from utils import is_invalid_number

class SimulationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Temperature Control System")
        
        # Robot Attributes
        self.robot = None     
        self.num_subsystems = 0   
        self.num_fans = 0
        
        # To store UI elements 
        self.fans = []
        self.fan_labels = []
        self.subsystem_labels = []
        self.fan_rpm_entries = []
        
        self.init_ui()

    def init_ui(self):
        # Get number of subsystems from user
        tk.Label(self.root, text="Number of Subsystems:").grid(row=0, column=0)
        self.subsystem_entry = tk.Entry(self.root)
        self.subsystem_entry.grid(row=0, column=1)

        # Get number of fans from user
        tk.Label(self.root, text="Number of Fans:").grid(row=1, column=0)
        self.fan_entry = tk.Entry(self.root)
        self.fan_entry.grid(row=1, column=1)
        
        # Configure button
        self.configure_button = tk.Button(self.root, text="Configure", command=self.configure_robot)
        self.configure_button.grid(row=2, columnspan=2)

    def configure_robot(self):
        try:
            self.num_subsystems = int(self.subsystem_entry.get())
            self.num_fans = int(self.fan_entry.get())

            if self.num_subsystems <= 0 or self.num_fans <= 0:
                raise ValueError("Numbers must be non-negative.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return
        
        self.subsystem_entry.config(state='disabled')
        self.fan_entry.config(state='disabled')
        self.configure_button.grid_remove()         

        for i in range(self.num_fans):
            tk.Label(self.root, text=f"Max RPM for Fan {i + 1}:").grid(row=3 + i, column=0)
            self.fan_rpm_entry = tk.Entry(self.root)
            self.fan_rpm_entry.grid(row=3 + i, column=1)
            self.fan_rpm_entries.append(self.fan_rpm_entry) 

        # Button to process the entered RPM values
        self.submit_button = tk.Button(self.root, text="Submit Max RPMs", command=self.process_fan_rpms)
        self.submit_button.grid(row=3 + self.num_fans, column=1)

    def process_fan_rpms(self):
        # Checks if fan max RPMs are valid
        invalid_found = False
        for entry in self.fan_rpm_entries:
            if is_invalid_number(entry.get()):
                invalid_found = True
                break    
        if invalid_found:
            messagebox.showerror("Input Error", "Please enter valid numeric RPM values.")
            return
        
        # Once all max RPM inputs are good
        for entry in self.fan_rpm_entries:
            rpm_value = float(entry.get())  
            self.fans.append(Fan(rpm_value))
            entry.config(state="disabled")
    
        # Create robot with correct fan values
        self.robot = Robot(self.num_subsystems, self.num_fans, self.fans)

        # Start Simulation Button
        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4 + self.num_fans, columnspan=2)
    
    def start_simulation(self):
        self.submit_button.grid_remove()
        self.start_button.grid_remove()
        self.display_simulation()
        self.update_simulation()

    def display_simulation(self):  
        # Create and display subsystem temperature labels
        start_row = 4 + len(self.fan_rpm_entries)
        for i in range(len(self.robot.subsystems)):
            label = tk.Label(self.root, text=f"Subsystem {i + 1} °C")
            label.grid(row=start_row + i, column=0, padx=5, pady=2, sticky="w")
            self.subsystem_labels.append(label)

        # Create and display fan speed labels
        fan_start_row = start_row + len(self.robot.subsystems)
        for i in range(self.num_fans):
            label = tk.Label(self.root, text=f"Fan {i + 1} RPM")
            label.grid(row=fan_start_row + i, column=0, padx=5, pady=2, sticky="w")
            self.fan_labels.append(label)

        # Add End Simulation Button
        self.end_button = tk.Button(self.root, text="End Simulation", command=self.end_simulation)
        self.end_button.grid(row=fan_start_row + self.num_fans, column=1)

    def update_simulation(self):
        self.robot.update_subsystem_temperatures()

        # Update subsystem temperature labels
        for i, subsystem in enumerate(self.robot.subsystems):
            self.subsystem_labels[i].config(text=f"Subsystem {i + 1}: {subsystem.get_temperature():.3f} °C")

        # Update fan speed labels
        for i, fan in enumerate(self.robot.fans):
            self.fan_labels[i].config(text=f"Fan {i + 1}: {fan.get_speed():.3f} RPM")

        # Schedule next update in 2000ms (2 seconds)
        self.root.after(2000, self.update_simulation)

    def end_simulation(self):
        self.root.quit()
        self.root.destroy()
        
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SimulationUI(root)
#     root.mainloop()
