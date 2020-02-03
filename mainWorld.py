# This file is the simulation application
# This files holds the state variables and event procedure

import numpy.random as NR
import math
from engine import current_time, fel, schedule_event
import engine
import objects

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

itter+=1
populateLightChanges(itter)
rePop()

while itter<300:
    event = fel.get()
    event.whoami()

    #If Event Type is an Arrival Event (arrival of vehicle)
    if event.eventType[0] == 'A':
        onArrival(event)

    if event.eventType == 'LC'
        onLightChange(event)
    """
     #### LIGHT CHANGES ####
    if (event.eventType == "LC"):
        world.changeTheLights()
        itter += 1
        populateLightChanges(itter)
        #### Now we can actually move stuff in the queues ####
    """
