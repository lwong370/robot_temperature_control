import tkinter as tk
from tkinter import messagebox
from robot_components import Robot, Fan, Subsystem

class RobotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Cooling System")
        self.robot = None        
        self.fans = []
        self.fan_labels = []
        self.subsystem_labels = []
        self.fan_rpm_entries = []
        
        # User inputs
        tk.Label(root, text="Number of Subsystems:").grid(row=0, column=0)
        self.subsystem_entry = tk.Entry(root)
        self.subsystem_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Number of Fans:").grid(row=1, column=0)
        self.fan_entry = tk.Entry(root)
        self.fan_entry.grid(row=1, column=1)
        
        self.configure_button = tk.Button(root, text="Configure", command=self.configure_robot)
        self.configure_button.grid(row=2, columnspan=2)

    def configure_robot(self):
        try:
            num_subsystems = int(self.subsystem_entry.get())
            num_fans = int(self.fan_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return
        
        self.subsystem_entry.config(state='disabled')
        self.fan_entry.config(state='disabled')
        self.configure_button.grid_remove()         

        for i in range(num_fans):
            tk.Label(self.root, text=f"Max RPM for Fan {i + 1}:").grid(row=3 + i, column=0)
            self.fan_rpm_entry = tk.Entry(self.root)
            self.fan_rpm_entry.grid(row=3 + i, column=1)
            self.fan_rpm_entries.append(self.fan_rpm_entry)  # Save Entry widget for later

        # Button to process the entered RPM values
        self.submit_button = tk.Button(self.root, text="Submit Max RPMs", command=self.process_fan_rpms)
        self.submit_button.grid(row=3 + num_fans, column=1)

    def process_fan_rpms(self):
        for entry in self.fan_rpm_entries:
            try:
                rpm_value = float(entry.get())  # Now get user input
                self.fans.append(Fan(rpm_value))
                entry.config(state="disabled")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numeric RPM values.")
                return
    
        # Create robot with correct fan values
        num_subsystems = int(self.subsystem_entry.get())
        num_fans = len(self.fans)
        self.robot = Robot(num_subsystems, num_fans, self.fans)

        # Start Simulation Button
        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4 + num_fans, columnspan=2)
    
    def start_simulation(self):
        self.robot.update_subsystem_temperatures("./csv_files/temperature_input_data.csv")

        # self.display_simulation()
        # self.update_simulation()
    
    # def display_simulation(self):
    #     for widget in self.subsystem_labels + self.fan_labels:
    #         widget.destroy()
        
    #     self.subsystem_labels = [tk.Label(self.root, text=f"Subsystem {i + 1}: 0 C") for i in range(len(self.robot.subsystems))]
    #     for i, label in enumerate(self.subsystem_labels):
    #         label.grid(row=4 + i, column=0)
        
    #     self.fan_labels = [tk.Label(self.root, text=f"Fan {i + 1}: 0 RPM") for i in range(len(self.robot.fans))]
    #     for i, label in enumerate(self.fan_labels):
    #         label.grid(row=4 + len(self.robot.subsystems) + i, column=0)
    
    # def update_simulation(self):
    #     self.robot.update_subsystem_temperatures("./csv_files/temperature_input_data.csv")
        
    #     for i, subsystem in enumerate(self.robot.subsystems):
    #         self.subsystem_labels[i].config(text=f"Subsystem {i + 1}: {subsystem.get_temperature():.1f} C")
        
    #     for i, fan in enumerate(self.robot.fans):
    #         self.fan_labels[i].config(text=f"Fan {i + 1}: {fan.get_speed():.1f} RPM")
        
    #     self.root.after(4000, self.update_simulation)  # Refresh every 4 sec
        
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotUI(root)
    root.mainloop()
