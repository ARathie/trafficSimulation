# This file is the simulation application
# This files holds the state variables and event procedure

import numpy.random as NR
import math
from engine import current_time, fel, schedule_event
import engine
import objects

###########################
#  STATE VARIABLES
initial_num_vehicles = 50

###########################


# DATA COLLECTION VARIABLES



#a startup method with some kind of simulation
#initialization behavior. for now just prints
#the name of the simulator in ascii
def startup():
	print( 
		   '___________              _____  _____. __                  \n'
		   '\__    ___/___________ _/ ____\/ ____\|__| ____            \n' 
		   '  |    |  \_  __ \__ \.\   __\.\   __\|  |/ ___\           \n' 
		   '  |    |   |  | \// __ \|  |   |  |   |  \  \___           \n' 
		   '  |____|   |__|  (____  /__|   |__|   |__|\___  >          \n' 
		   '                      \/                     \/           \n' 
		   '  _________.__              .__           __                \n'
		   ' /   _____/|__| _____  __ __|  | _____  _/  |_  ___________  \n'
		   ' \_____  \ |  |/     \|  |  \  | \__  \.\   __\/  _ \_  __ \ \n'
		   ' /        \|  |  Y Y  \  |  /  |__/ __ \|  |  (  <_> )  | \/ \n'
		   '/_______  /|__|__|_|  /____/|____(____  /__|   \____/|__|    \n'
		   '        \/          \/                \/                    \n'
		 )




startup()
world = objects.World()
avg = 3 #the average rate of arrival of vehicles (to be changed later)

#schedules arrival events for vehicles coming from East and West
def scheduleNextArrival(avg):
	interarrival = math.ceil(NR.exponential(avg)) #time until next arrival event
	nextArrivalTime = current_time + interarrival
	current_time = nextArrivalTime
	newEvent = engine.Event()
	newEvent.randomEventType()
	newEvent.setEventTimeStamp(nextArrivalTime)
	schedule_event(newEvent)


vehicle_num = 0 #0 vehicles at start of simulation
while vehicle_num < 10:
	scheduleNextArrival(avg)
	fel.get().whoami() #prints out the event
	vehicles += 1