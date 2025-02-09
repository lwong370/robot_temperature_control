import tkinter as tk
from tkinter import messagebox
from robot_components import Robot, Fan

class SimulationUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Temperature Control System")
        self.scroll_frame = None
                
        self.init_ui()

    def init_ui(self):
        # Robot Attributes
        self.robot = None     
        self.num_subsystems = 0   
        self.num_fans = 0
        
        # To store UI elements 
        self.fans = []
        self.fan_labels = []
        self.subsystem_labels = []
        self.fan_rpm_entries = []

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set base window to a quarter of the screen size
        window_width = screen_width // 2  
        window_height = screen_height // 2 

        # Set root window dimensions
        self.root.geometry(f"{window_width}x{window_height}")

        # Set up scroll view
        self.make_scroll_view()

        # Get number of subsystems from user
        tk.Label(self.scroll_frame, text="Number of Subsystems:").grid(row=0, column=0)
        self.subsystem_entry = tk.Entry(self.scroll_frame)
        self.subsystem_entry.grid(row=0, column=1)

        # Get number of fans from user
        tk.Label(self.scroll_frame, text="Number of Fans:").grid(row=1, column=0)
        self.fan_entry = tk.Entry(self.scroll_frame)
        self.fan_entry.grid(row=1, column=1)
        
        # Configure button
        self.configure_button = tk.Button(self.scroll_frame, text="Configure", command=self.configure_robot)
        self.configure_button.grid(row=2, columnspan=2)

    def configure_robot(self):
        # Reset input box colors to default white
        self.subsystem_entry.config(bg="white")
        self.fan_entry.config(bg="white")

        has_error = False  # Track if any errors occur

        # Validate Number of Subsystems
        try:
            self.num_subsystems = int(self.subsystem_entry.get())
            if self.num_subsystems <= 0:
                raise ValueError
        except ValueError:
            self.subsystem_entry.config(bg="#ffcccc")  # Highlight invalid input
            has_error = True

        # Validate Number of Fans
        try:
            self.num_fans = int(self.fan_entry.get())
            if self.num_fans <= 0:
                raise ValueError
        except ValueError:
            self.fan_entry.config(bg="#ffcccc")  # Highlight invalid input
            has_error = True

        # If there's an error, show an alert and stop execution
        if has_error:
            messagebox.showerror("Input Error", "Please enter valid whole numbers.")
            return

        # Disable input fields after successful validation
        self.subsystem_entry.config(state="disabled")
        self.fan_entry.config(state="disabled")
        self.configure_button.grid_remove()

        # Create fan RPM input fields dynamically
        for i in range(self.num_fans):
            tk.Label(self.scroll_frame, text=f"Max RPM for Fan {i + 1}:").grid(row=3 + i, column=0)
            fan_rpm_entry = tk.Entry(self.scroll_frame)
            fan_rpm_entry.config(bg="white")
            fan_rpm_entry.grid(row=3 + i, column=1)
            self.fan_rpm_entries.append(fan_rpm_entry)

        # Submit button to process RPM values
        self.submit_button = tk.Button(self.scroll_frame, text="Submit Max RPMs", command=self.process_fan_rpms)
        self.submit_button.grid(row=3 + self.num_fans, column=1)

    def process_fan_rpms(self):
        # Checks if fan max RPMs are valid
        invalid_found = False
        for entry in self.fan_rpm_entries:
            entry.config(bg="white")  
            try:
                rpm_value = float(entry.get())
                if rpm_value < 0:
                    raise ValueError
            except ValueError:
                entry.config(bg="#ffcccc")  
                invalid_found = True

        if invalid_found:
            messagebox.showerror("Input Error", "Please enter valid positive RPM values.")
            return
        
        # Once all max RPM inputs are good
        for entry in self.fan_rpm_entries:
            rpm_value = float(entry.get())  
            self.fans.append(Fan(rpm_value))
            entry.config(state="disabled")
            self.submit_button.config(state="disabled")

        # Create robot with correct fan values
        self.robot = Robot(self.num_subsystems, self.num_fans, self.fans)

        # Start Simulation Button
        self.start_button = tk.Button(self.scroll_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=4 + self.num_fans, columnspan=2)
    
    def start_simulation(self):
        self.submit_button.grid_remove()
        self.start_button.grid_remove()
        self.make_color_legend()
        self.display_simulation()
        self.update_simulation()

    def display_simulation(self):  
        # Create and display subsystem temperature labels
        start_row = 4 + len(self.fan_rpm_entries)
        for i in range(len(self.robot.subsystems)):
            label = tk.Label(self.scroll_frame, text=f"Subsystem {i + 1} °C")
            label.grid(row=(start_row+1) + i, column=0, padx=5, pady=2, sticky="w") # Add 1 to start_row to account for color legend
            self.subsystem_labels.append(label)

        # Create and display fan speed labels
        fan_start_row = start_row + len(self.robot.subsystems) + 2
        title_label = tk.Label(self.scroll_frame, text="Fan Speeds:", font=("Arial", 12, "bold"))
        title_label.grid(row=fan_start_row, column=0, padx=5, pady=2, sticky="w")
        for i in range(self.num_fans):
            label = tk.Label(self.scroll_frame, text=f"Fan {i + 1} RPM")
            label.grid(row=(fan_start_row+1) + i, column=0, padx=5, pady=2, sticky="w")
            self.fan_labels.append(label)

        # Add End Simulation Button
        self.end_button = tk.Button(self.scroll_frame, text="End Simulation", command=self.end_simulation)
        self.end_button.grid(row=fan_start_row + self.num_fans, column=1)

    def update_simulation(self):
        # Update subsystem temperature labels 
        self.robot.update_subsystem_temperatures()

        for i, subsystem in enumerate(self.robot.subsystems):
            # Determine text color based on temperature range
            temp = subsystem.get_temperature()
            if temp <= 25:  # Cold temperature
                color = "blue"      
            elif temp >= 75:  # Hot temperature
                color = "orange"    
            else:  # Normal 
                color = "black"     
            self.subsystem_labels[i].config(text=f"Subsystem {i + 1}: {subsystem.get_temperature():.3f} °C", fg=color)

        # Update fan speed labels
        for i, fan in enumerate(self.robot.fans):
            self.fan_labels[i].config(text=f"Fan {i + 1} running at ~{fan.get_percent_rpm()*100:.0f}% = {fan.get_speed():.3f} RPM")

        # Schedule next update in 2000ms (2 seconds)
        self.scroll_frame.after(2000, self.update_simulation)

    def make_color_legend(self):
        # Create a frame to hold legend
        legend_frame = tk.Frame(self.scroll_frame)
        legend_frame.grid(row=4 + self.num_fans, column=0, padx=0, pady=0)  # Adjust the grid position as needed

        # Create and display legend
        title_label = tk.Label(legend_frame, text="Subsystem Temperatures: ", font=("Arial", 12, "bold"))
        title_label.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        cold_label = tk.Label(legend_frame, text="Cold", fg="blue")
        cold_label.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        normal_label = tk.Label(legend_frame, text="Normal", fg="black")
        normal_label.grid(row=0, column=4, padx=5, pady=2, sticky="w")

        hot_label = tk.Label(legend_frame, text="Hot", fg="orange")
        hot_label.grid(row=0, column=6, padx=5, pady=2, sticky="w")

    def make_scroll_view(self):
        # Make new canvas to put scroll view in
        canvas = tk.Canvas(root)
        canvas.pack(side="left", fill="both", expand=True)

        # Create scrollbar and put in the canvas
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create frame inside the canvas to hold content in scrollable view
        self.scroll_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Update scroll region when window size or content changes
        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Lets scroll region update when content inside frame changes
        self.scroll_frame.bind("<Configure>", update_scroll_region)

    def end_simulation(self):
        # Clear contents of UI
        for widget in root.winfo_children():
            widget.destroy()

        # Message box for saving data
        messagebox.showinfo("Information", f"Data saved to {self.robot.get_log_file_name()}")
        
        self.init_ui()


# Create the main Tkinter window
root = tk.Tk()

# Create SimulationUI instance
app = SimulationUI(root)

# Run tkinter event loop
root.mainloop()
