# Robot Temperature Control

## Overview
### Motivation
Little programming exercise that develops a robot with multiple subsystems and cooling fans that implements object oriented programming in python. I tried created this with the following thought process:
- First and foremost, according to the prompt, we want to show that the robot accurately works for ranges of temperatures from -20 to 85 degree Celcius. Thus, this robot will not emulate a real-working system where the temperature is more stable, and will be fed random float values across this range. 
- real-world application and importance, maybe connect it back to the role?

### User Assumptions
- Temperatures and fan speeds are reported up to the third decimal. 
- The subsystem temperatures will be updated every 2 seconds.
- As mentioned in motivations, our goal is to see how the fans of the robot reacts across a broad range of subsystem temperatures. Thus, the user can expect the subsystem temperatures to be random values between -20 to 85 degrees Celcius. The response can be viewed accordingly in the Fan RPMs that are updated every 2 seconds. 

### How to Use
- Run main.py
- Tkinter UI will pop up asking for integers to represent the number of subsystems and fans to include in the system. Click "Configure" button.
- Set the max RPM values of each fan. Once finished, click on the "Start Simulation" button.
- Observe how the fan speeds change as the temperature of each subsystem is automatically updated with a random float value between -20 and 85 degrees Celcius.

### Libraries Used
- Tkinter

## Code Information
### Simulation in Tkinter
Within the simulation_ui.py, observe these functions and their objectives:
- `configure_robot()` → Captures user input
- `process_fan_rpms()` → Validates input, initializes fans
- `start_simulation()` → Sets up simulation
- `display_simulation()` → Creates UI elements
- `update_simulation()` → Loops the updates

### Testing
Within test_robot.py, I wrote some unit tests to test the overall system. These include edge cases such as:
- User inputs with negative numbers → invalid input
- User inputs with special characters → invalid input

## TODO IDEAS:
- give it some inital temp, then based on current temp, then change the temp to act accordingly. 

## TODO: def update_dashboard()
- negative-proof number inputs of fan and subsystem amounts
- explain reason why I used csv files to store data
- gui is for making this application easier to use. the goal is to make this more visual

## Future Improvements
