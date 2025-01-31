import tkinter as tk
from robot_components import Robot
from simulation_ui import SimulationUI

# Create the main Tkinter window
root = tk.Tk()

# Create SimulationUI instance
app = SimulationUI(root)

# Runs tkinter event loop
root.mainloop()

