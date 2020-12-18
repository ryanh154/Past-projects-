import serial
import time
import struct

#def connect():
connection = serial.Serial('/dev/ttyUSB0', baudrate=115200)

def start(): #Resets and starts the Roomba
	connection.write(chr(7)) #reset to clear active robot operations
	time.sleep(5)
	while connection.inWaiting():
		 connection.read(connection.inWaiting())#can print out diagnogstics
	#delay ends
	connection.write(chr(128)) #start command (this makes noise)
	time.sleep(1)
	'''connection.write(chr(131)) #safe
	time.sleep(0.015)'''

#Resets roomba
def reset(): #OP code to reset the Roomba
	connection.write(chr(7))

#Sets to stop mode
def stop(): #OP code to stop the Roomba
	connection.write(chr(173))

#Sets to passive mode
def passive(): #OP code to set the Roomba to passive
	connection.write(chr(128))
	
#Sets to safe mode
def safe(): 
	connection.write(chr(131)) #OP code to put a Roomba to safe mode
	
#Sets to full mode
def full():
	connection.write(chr(132))#OP code to put a Roomba to full mode

#Returns a list of booleans relative to [leftwheel, rightwheel, leftbumper, rightbumper]
def collectSensorData(): 
	connection.write(chr(142)+chr(7)) #OP code to gather and store the sensor package
	data = connection.read() #stored data to be parsed
	byte = struct.unpack('B', data)[0] #parses data
	bool(byte & 0x08)

	#Takes the integer gained from data and analyzes each bit of the byte recieved
	if byte / 8 == 1: #3rd bit
		lw = True
	else:
		lw = False
	if byte % 8 >= 4: #2nd bit
		rw = True
	else:
		rw = False
	if byte % 4 >= 2: #1st bit
		lb = True
	else:
		lb = False
	if byte % 2 == 1: #0th bit
		rb = True
	else:
		rb = False

	return[lw,rw,lb,rb] #List of booleans

#Returns a list of booleans relative to each button [clean,spot,dock,minute,hour,day,schedule,clock]
def collectButtonData(): 
	connection.write(chr(142)+chr(18)) #OP code to gather and store the sensor package
	data = connection.read() #stored data to be parsed
	byte = struct.unpack('B', data) [0]#parses data
	bool(byte & 0x08)

	#Takes the integer gained from data and analyzes each bit of the 2 bytes recieved
	if byte / 128 == 1: #7th bit
		clock = True
	else:
		clock = False
	if byte % 128 >= 64: #6th bit
		schedule = True
	else:
		schedule = False
	if byte % 64 >= 32: #5th bit
		day = True
	else:
		day = False
	if byte % 32 >= 16: #4th bit
		hour = True
	else:
		hour = False
	if byte % 16 >= 8: #3rd bit
		minute = True
	else:
		minute = False
	if byte % 8 >= 4: #2nd bit
		dock = True
	else:
		dock = False
	if byte % 4 >= 2: #1st bit
		spot = True
	else:
		spot = False
	if byte % 2 == 1: #0th bit
		clean = True
	else:
		clean = False

	return[clean,spot,dock,minute,hour,day,schedule,clock]

#Moves robot straight if a valid velocity is entered
def drive(velocity, radius): # Takes in a velocity integer and a radius integer to put into the Connection
	v = 0
	if (velocity >= 0): #Checks if velocity is negative
		v = velocity

	packed = struct.pack('>B2h', 137, velocity, radius)
	connection.write(packed)

	connection.write(chr(137)+chr(vHi)+chr(vLo)+chr(rHi)+chr(rLo)) #takes the isolated variables and puts them in the op code for drive

# Gets Angle turned since function was last used
def getAngle():
	connection.write(chr(142)+chr(9)) #OP code to gather and store the sensor package
	data = connection.read() #stored data to be parsed
	angle = struct.unpack('b', data) [0]#parses data
	bool(angle & 0x10)
	return angle

# Gets distance moved since function was last used
def getDistance():
	connection.write(chr(142)+chr(9)) #OP code to gather and store the sensor package
	data = connection.read() #stored data to be parsed
	distance = struct.unpack('b', data) [0]#parses data
	bool(distance & 0x10)
	return distance

# Collects data from all cliff sensors
def collectCliffData():
	#Collects data from left cliff sensor
	connection.write(chr(142)+chr(9))
	data = connection.read()
	byte = struct.unpack('B', data)[0]
	bool(byte & 0x08)
	if(byte==0):
		Left=False
	else:
		Left=True

	#Collects data from front left cliff sensor
	connection.write(chr(142)+chr(10))
	data = connection.read()
	byte = struct.unpack('B', data)[0]
	bool(byte & 0x08)
	if(byte==0):
		fLeft=False
	else:
		fLeft=True

	#Collects data from front right cliff sensor
	connection.write(chr(142)+chr(11))
	data = connection.read()
	byte = struct.unpack('B', data)[0]
	bool(byte & 0x08)
	if(byte==0):
		fRight=False
	else:
		fRight=True

	#Collects data from right cliff sensor
	connection.write(chr(142)+chr(12))
	data = connection.read()
	byte = struct.unpack('B', data)[0]
	bool(byte & 0x08)
	if(byte==0):
		Right=False
	else:
		Right=True

	#Return a list of all the cliff sensor readings
	return[Left,fLeft,fRight,Right]

# Drive function that takes the velocity of the right wheel and left wheel
def driveDirect(lVelocity, rVelocity):
	#Takes given left velocity and breaks it into two bites
	v = 0
	if (lVelocity >= 0): #Checks if velocity is negative
		v = lVelocity
	else:
		v = (1<<16) + lVelocity

	lVHi = v >> 8 & 0xFF #shifts the int over 8 bits to isolate the top 8 bits
	lVLo = v & 0xFF #sets the lower 8 bits

	#Takes right velocity and breaks it into two bites
	v = 0
	if (rVelocity >= 0): #Checks if velocity is negative
		v = rVelocity
	else:
		v = (1<<16) + rVelocity

	rVHi = v >> 8 & 0xFF #shifts the int over 8 bits to isolate the top 8 bits
	rVLo = v & 0xFF #sets the lower 8 bits
	
	#Passes command to Robot through serial connection
	connection.write(chr(145)+chr(rVHi)+chr(rVLo)+chr(lVHi)+chr(lVLo))

# Drive forward for a specified amount of time while pending a clean button press
def timedDrive(seconds, lVelocity, rVelocity):
	#Calculates end time
	endTime = time.time() + seconds
	#Drive with given specified speed
	driveDirect(lVelocity,rVelocity)
	cleanButton = False

	# pends button press while moving forward
	while(time.time() < endTime and cleanButton == False):
		cleanButton = collectButtonData()[0]

# Function to write song
def createSongs():
	connection.write(chr(140)+chr(0)+chr(16)+chr(78)+chr(32)+chr(77)+chr(32)+chr(74)+chr(22)+chr(76)+chr(22)+chr(77)+chr(22)+chr(76)+chr(22)+chr(74)+chr(22)+chr(73)+chr(22)+chr(74)+chr(22)+chr(76)+chr(22)+chr(78)+chr(32)+chr(83)+chr(32)+chr(71)+chr(22)+chr(73)+chr(22)+chr(74)+chr(22)+chr(76)+chr(22));
	
# Function top play written song
def playWarning():
	connection.write(chr(140)+chr(0)+chr(16)+chr(78)+chr(32)+chr(77)+chr(32)+chr(74)+chr(22)+chr(76)+chr(22)+chr(77)+chr(22)+chr(76)+chr(22)+chr(74)+chr(22)+chr(73)+chr(22)+chr(74)+chr(22)+chr(76)+chr(22)+chr(78)+chr(32)+chr(83)+chr(32)+chr(71)+chr(22)+chr(73)+chr(22)+chr(74)+chr(22)+chr(76)+chr(22));
	connection.write(chr(141)+chr(0))
	time.sleep(6.15)
	connection.write(chr(140)+chr(1)+chr(5)+chr(74)+chr(22)+chr(71)+chr(22)+chr(81)+chr(22)+chr(79)+chr(22)+chr(78)+chr(22))
	connection.write(chr(141)+chr(1))