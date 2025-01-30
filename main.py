import sys
from robot_components import Robot, check_valid_input
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from robot_components import Robot

# Get user input
num_subsystems = check_valid_input("How many subsystems are there? Can choose up to 20. ", int)
fans_present = check_valid_input("How many fans are there? ", int)

# Create instance of Robot with user input
robot = Robot(num_subsystems, fans_present)

# Update subsystem temperatures, for purpose of simulation
robot.update_subsystem_temperatures("./csv_files/temperature_input_data.csv")



# app = QApplication(sys.argv)
# window = SimulationUI()
# window.show()
# sys.exit(app.exec_())
