import Interface1
import time
import random

#Velocity of roomba
VELOCITY = 185 
#Range of 45 degress after bumb sensor is hit
RANGE= 45
#Defined turn time is 2 seconds
TURN_TIME = 2
#Velocity Variable to stop
STOP = 0

#Starts Robot
Interface1.start()
#Puts Robot in full mode
Interface1.full()
#Creates defined warning sound
Interface1.createSongs()

#Defines and sets sensor variables to not pressed
keepRunning = False
cleanButton = False
rBumper = False
lBumper = False

#Loop that keeps program continuously running
while(keepRunning == False): 

	#Lets User know that you robot is ready to start
	print "Press Clean to start" 

	#Waits for a button or bumper press to start random walk
	while(cleanButton == False and rBumper == False and lBumper ==False): 
		#Takes sensor data from the robot and puts it into list for future use
		checkList = [Interface1.collectButtonData()[0],Interface1.collectSensorData()[3],Interface1.collectSensorData()[2]]
		
		#Assigns changes of sensors to variables to be checked later
		cleanButton = checkList[0]
		rBumper = checkList[1]
		lBumper = checkList[2]

	#If Clean button was pressed go forward
	if(cleanButton == True): 
		Interface1.timedDrive(0,VELOCITY,VELOCITY)
		cleanButton = False #Resets button state
		time.sleep(.5) #Slight delay to ignore accidental double presses 
	
	#If Bumpers were pressed turn around
	elif(rBumper == True or lBumper == True): 
		
		#adds the +/-30 degrees
		velRange = random.randrange(-RANGE,RANGE)

		if(rBumper==True): #If right bumper was pressed turn counter clockwise
			Interface1.timedDrive(TURN_TIME,-VELOCITY-velRange,VELOCITY+velRange)

			#Reset both data variables incase both were pressed
			rBumper = False
			lBumper = False
		else: #If right bumper was pressed turn clockwise
			Interface1.timedDrive(TURN_TIME,VELOCITY+velRange,-VELOCITY-velRange)

			#Reset both data variables incase both were pressed
			lBumper = False
			rBumper = False
		Interface1.driveDirect(VELOCITY,VELOCITY)


	#Adds wheel drop and cliff sensors for on the move instances
	wheelDrop = [False,False]
	cliffData = [False,False,False,False]

	#Stops movement and goes back to stopped instance if Clean button is pressed or wheels drop
	while(cleanButton == False and wheelDrop == [False, False]):

		#Waits for an any of the sensors to trigger
		while(cleanButton == False and rBumper == False and lBumper == False and wheelDrop == [False,False] and cliffData == [False,False,False,False]):
			cleanButton = Interface1.collectButtonData()[0]
			cliffData = Interface1.collectCliffData()
			sensorList = Interface1.collectSensorData()
			rBumper = sensorList[3]
			lBumper = sensorList[2]
			wheelDrop = [sensorList[0],sensorList[1]]

		#If clean Button is pressed or Wheel drop stop the wheels
		if(cleanButton == True or wheelDrop != [False,False]):
			#If wheels drop play warning sound
			if(wheelDrop!=[False,False]):
				Interface1.driveDirect(STOP,STOP)
				Interface1.playWarning()
				cleanbutton=True

			Interface1.driveDirect(STOP,STOP)
			break
			
		#If Bumpers of Cliff sensors trigger
		elif(rBumper == True or lBumper == True or cliffData != [False,False,False,False]):
			#adds the + or - 45 degrees
			velRange = random.randrange(-RANGE,RANGE)

			#If right bumper or right cliff sensors trigger
			if(rBumper==True or cliffData[2] ==True or cliffData[3] == True):
				#Turns counter Clockwise
				Interface1.timedDrive(TURN_TIME,-VELOCITY-velRange,VELOCITY+velRange)

				#Reset all sensor variables
				rBumper = False
				lBumper = False
				cliffData[2] = False
				cliffData[3] = False
				
				#If clean Button is pressed of Wheels drop stop the wheels
				if(cleanButton == True or wheelDrop != [False,False]):
					#If wheels drop play warning sound
					if(wheelDrop!=[False,False]):
						Interface1.driveDirect(STOP,STOP)
						Interface1.playWarning()
						cleanbutton=True

					Interface1.driveDirect(STOP,STOP)
					break
				
			#If left bumper or left cliff sensors trigger
			else:
				#Turn clockwise
				Interface1.timedDrive(TURN_TIME,VELOCITY+velRange,-VELOCITY-velRange)

				#reset all sensor variables
				lBumper = False
				rBumper = False
				cliffData[0] = False
				cliffData[1] = False
			
				#If clean Button is pressed of Wheels drop stop the wheels
				if(cleanButton == True or wheelDrop != [False,False]):
					#If wheels drop play warning sound
					if(wheelDrop!=[False,False]):
						Interface1.driveDirect(STOP,STOP)
						Interface1.playWarning()
						cleanbutton=True

					Interface1.driveDirect(STOP,STOP)
					break
			
			#Continue forward
			Interface1.driveDirect(VELOCITY,VELOCITY)

	#Resets the sensors that would cause the robot to stop if triggered
	cleanButton = False
	wheelDrop = [False,False]

