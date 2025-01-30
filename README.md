# Robot Temperature Control

## Motivation
Little programming exercise that develops a robot with multiple subsystems and cooling fans that implements object oriented programming in python. I tried created this with the following thought process:
- First and foremost, according to the prompt, we want to show that the robot accurately works for ranges of temperatures from -20 to 85 degree Celcius. Thus, this robot will not emulate a real-working system where the temperature is more stable, and will be fed random float values across this range. 

## User Assumptions
- A robot can only have a maximum of 20 subsystems.
- Temperatures and fan speeds are reported up to the third decimal 
- The subsystem temperatures will be updated every 2 seconds.
- As mentioned in motivations, our goal is to see how the fans of the robot reacts across a broad range of subsystem temperatures. Thus, the user can expect the subsystem temperatures to be random values between -20 to 85 degrees Celcius. The response can be viewed accordingly in the Fan RPMs that are updated every 2 seconds. 

## How to Use
- Run main.py
- Console will ask for the number of subsystems and fans you would like to include in your robot. 
- Console will then ask for the maximum RPMs of each individual fan that you have created in your robot.
- Observe how the fan speeds change as the temperature of each subsystem is automatically updated using data from temperature_input_data.csv.

# TODO: IDEAS:
- give it some inital temp, then based on current temp, then change the temp to act accordingly. 

# TODO: def update_dashboard()
-  landing page
- tkinter for gui?