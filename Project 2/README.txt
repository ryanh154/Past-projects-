To execute the program, simply have the following files in the same directory and execute the code with "python Test Project 2.py"

Interface.py
	This is the interface for the program which contains the methods to send commands to the robot such as start,stop,rest, and drive the robot.
	It also has the methods to read and unpack the data from the sensors and buttons on the robot.
	This file can be implemented to build other applications for the robot.

Test Project 2.py
	This file is the program which initalizes the robot and randomly drives untill hitting and object. When the bumber sensor is pressed the roomba
	rotates 180 degrees + or - 45 degrees. The roomba rotates in the direction according to the sensor pressed. The roomba stops and resumes the code
	when the clean button is pressed. The roomba stops and plays a warning song if it's cliff or wheel drop sensors are activated. To use this file, 
	run the program by typing "python Test Project 2.py" and pressing the clean button when promted to begin the robots random walk.
