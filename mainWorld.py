# This file is the simulation application
# This files holds the state variables and event procedure

import numpy.random as NR
import math
from engine import current_time, fel, schedule_event
import engine
import objects
import math


###########################
#  STATE VARIABLES
initial_num_vehicles = 20
itter = 0 # to put light changes at fixed rates

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

###########################
# EASE OF USE
luckie_intersection = world.luckie_intersection
olympic_intersection = world.olympic_intersection
###########################

#schedules arrival events for vehicles coming from East and West
def scheduleNextArrival(avg):
    global current_time
    interarrival = math.ceil(NR.exponential(avg)) #time until next arrival event
    nextArrivalTime = current_time + interarrival
    current_time = nextArrivalTime
    newEvent = engine.Event()
    newEvent.randomEventType()
    newEvent.setEventTimeStamp(nextArrivalTime)
    schedule_event(newEvent)

def onArrival(event):
    #### PARSING ARRIVALS ####
    # Basically, I am looking through the FEL to see what deal with events
    if (event.eventType == "AW"):
        luckie_intersection.westQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles +- 1
    elif (event.eventType == "AE"):
        olympic_intersection.eastQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles +- 1
    elif (event.eventType == "AN1"):
        luckie_intersection.northQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles +- 1
    elif (event.eventType == "AN2"):
        olympic_intersection.northQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles +- 1
    elif (event.eventType == "AS1"):
        luckie_intersection.southQueue.put(objects.Vehicle(event.timeStamp))
    elif (event.eventType == "AS2"):
        olympic_intersection.southQueue.put(objects.Vehicle(event.timeStamp))

	current_time = event.timestamp

def onLightChange(event):
    pass

def rePop(vehicle_num = initial_num_vehicles):
    while vehicle_num > 0:
        scheduleNextArrival(avg)
        vehicle_num -= 1

# Populating FEL w/ schedualed light changes
def populateLightChanges(time):
    newEvent = engine.Event()
    newEvent.lightChangeType()
    newEvent.setEventTimeStamp(time*30)
    schedule_event(newEvent)

def get_num_vehicles():
	east = -0.0098*(x**5) + 0.6157*(x**4) + -13.8048*(x**3) + 125.8024*(x**2) + -337.2493*x + 273.2855
	west = -0.0084*(x**5) + 0.5114*(x**4) + -11.3061*(x**3) + 102.2751*(x**2) + -205.6825*x + 218.7994
	total = round(east + west, 0)

def generate_arrivals(time_interval): # time interval in tuple form ie (12, 14)
	
	# global current_time
    # interarrival = math.ceil(NR.exponential(avg)) #time until next arrival event
    # nextArrivalTime = current_time + interarrival
    # current_time = nextArrivalTime
    # newEvent = engine.Event()
    # newEvent.randomEventType()
    # newEvent.setEventTimeStamp(nextArrivalTime)
    # schedule_event(newEvent)

	# each element represents a 10 minute period starting at 12:00
	arrival_rates = np.array([390, 269, 184, 186, 177, 437, 1026, 1800, 1904, 1792, 1539, 1505, 1579, 1669, 1526, 1686, 1626, 1163, 1443, 1405, 1204, 1023, 900, 603])
	relevant_arrival_rates = arrival_rates[time_interval]

	for i in range(len(relevant_arrival_rates)):
		for _ in range(relevant_arrival_rates[i]):
			event = engine.Event()
			event.randomEventType(event)
			event.setEventTimeStamp(i + time_interval[0] + math.round(NR.random(0, (time_interval[1] - time_interval[0])*60), 4)) # TODO: Change timestamp to a stochastic time stamp
			schedule_event(event)

itter+=1
populateLightChanges(itter)
rePop()
generate_arrivals((12, 15))

while itter<300:
    event = fel.get()
    event.whoami()

    #If Event Type is an Arrival Event (arrival of vehicle)
    if event.eventType[0] == 'A':
        onArrival(event)

    if event.eventType == 'LC':
        onLightChange(event)
    """
     #### LIGHT CHANGES ####
    if (event.eventType == "LC"):
        world.changeTheLights()
        itter += 1
        populateLightChanges(itter)
        #### Now we can actually move stuff in the queues ####
    """
