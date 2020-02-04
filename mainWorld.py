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
itter = 0  # to put light changes at fixed rates


###########################


# DATA COLLECTION VARIABLES


# a startup method with some kind of simulation
# initialization behavior. for now just prints
# the name of the simulator in ascii
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
avg = 3  # the average rate of arrival of vehicles (to be changed later)

###########################
# EASE OF USE
luckie_intersection = world.luckie_intersection
olympic_intersection = world.olympic_intersection


###########################

# schedules arrival events for vehicles coming from East and West
def scheduleNextArrival(avg):
    global current_time
    interarrival = math.ceil(NR.exponential(avg))  # time until next arrival event
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
        initial_num_vehicles + - 1
    elif (event.eventType == "AE"):
        olympic_intersection.eastQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AN1"):
        luckie_intersection.northQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AN2"):
        olympic_intersection.northQueue.put(objects.Vehicle(event.timeStamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AS1"):
        luckie_intersection.southQueue.put(objects.Vehicle(event.timeStamp))
    elif (event.eventType == "AS2"):
        olympic_intersection.southQueue.put(objects.Vehicle(event.timeStamp))


def onLightChange(event):
    # FOR NORTH-SOUTH
    if luckie_intersection.lights[0] is 1:
        for i in range(0, luckie_intersection.carsToBeLetThrough(30, 30)):
            # FIRST WE POP THE LUCKIE INTERSECTION
            if not luckie_intersection.northQueue.empty():
                popped = luckie_intersection.northQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    olympic_intersection.westQueue.put(popped)
                else:
                    popped.exitVehicle()
                    luckie_intersection.exits += 1

            if not luckie_intersection.southQueue.empty():
                popped = luckie_intersection.southQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    olympic_intersection.westQueue.put(popped)

            # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.northQueue.empty():
                popped = olympic_intersection.northQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    luckie_intersection.eastQueue.put(popped)

            if not olympic_intersection.southQueue.empty():
                popped = olympic_intersection.southQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    luckie_intersection.eastQueue.put(popped)
                else:
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
    # FOR EAST-WEST
    else:
        for i in range(0, luckie_intersection.carsToBeLetThrough(30, 30)):
            # FIRST WE POP THE LUCKIE INTERSECTION
            if not luckie_intersection.westQueue.empty():
                popped = luckie_intersection.westQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    olympic_intersection.westQueue.put(popped)
                elif popped.direction == "L":
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    popped.exitVehicle()
                    luckie_intersection.exits += 1

            if not luckie_intersection.eastQueue.empty():
                popped = luckie_intersection.eastQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    popped.exitVehicle()
                    luckie_intersection.exits += 1

            # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.westQueue.empty():
                popped = olympic_intersection.westQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    popped.exitVehicle()
                    olympic_intersection.exits += 1

            if not olympic_intersection.eastQueue.empty():
                popped = olympic_intersection.eastQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    luckie_intersection.eastQueue.put(popped)
                elif popped.direction == "L":
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
    world.changeTheLights()

def rePop(vehicle_num=initial_num_vehicles):
    while vehicle_num > 0:
        scheduleNextArrival(avg)
        vehicle_num -= 1


# Populating FEL w/ schedualed light changes
def populateLightChanges(time):
    newEvent = engine.Event()
    newEvent.lightChangeType()
    newEvent.setEventTimeStamp(time * 30)
    schedule_event(newEvent)


itter += 1
populateLightChanges(itter)
rePop()

while itter < 10:
    event = fel.get()
    #event.whoami()

    # If Event Type is an Arrival Event (arrival of vehicle)
    if event.eventType[0] == 'A':
        onArrival(event)

    if event.eventType == 'LC':
        onLightChange(event)
        populateLightChanges(itter)
        itter += 1
    """
     #### LIGHT CHANGES ####
    if (event.eventType == "LC"):
        world.changeTheLights()
        itter += 1
        
        populateLightChanges(itter)
        #### Now we can actually move stuff in the queues ####
    """

print(luckie_intersection.exits)
print(olympic_intersection.exits)