# Robot Temperature Control

## Motivation
Little programming exercise that develops a robot with multiple subsystems and cooling fans that implements object oriented programming in python.

## User Assumptions
- A robot can only have a maximum of 20 subsystems.
- Temperatures and fan speeds are reported up to the third decimal 

## How to Use
- Run main.py
- Console will ask for the number of subsystems and fans you would like to include in your robot. 
- Console will then ask for the maximum RPMs of each individual fan that you have created in your robot.
- Observe how the fan speeds change as the temperature of each subsystem is automatically updated using data from temperature_input_data.csv.

# TODO: IDEAS:
- give it some inital temp, then based on current temp, then change the temp to act accordingly. 
- make unit tests

# TODO: def update_dashboard()
-  landing page
- tkinter for gui?
- save to csv file