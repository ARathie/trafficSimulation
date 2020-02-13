# This file is the simulation application
# This files holds the state variables and event procedure

import numpy.random as NR
import random
import math
from engine import current_time, fel, schedule_event
import engine
import objects
import math
import numpy as np


###########################
#  STATE VARIABLES
initial_num_vehicles = 20
itter = 0  # to put light changes at fixed rates
num_cars = 0

#start time that the simulation is MODELING, i.e.: SUI time between 0 hours to 23 hours
simulationStartTime = 0

#end time for the SUI, at which the simulation stops, 0 hours to 23 hours
simulationEndTime = 5
###########################

###########################
#  DATA

# each element represents a 10 minute period starting at 12:00, 12pm --> 4pm
arrival_rates = np.array([390, 269, 184, 186, 177, 437, 1026, 1800, 1904, 1792, 1539, 1505, 1579, 1669, 1526, 1686, 1626, 1163, 1443, 1405, 1204, 1023, 900, 603])

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


# schedules vehicle arrival events 
def scheduleArrivals():
    global arrival_rate_lambdas
    global num_cars
    time = simulationStartTime

    while time < simulationEndTime:

        #the lambda: (cars per minute, given a time in hours)
        lambda_ = get_num_vehicles(time) / 60
        nextArrivalTime = time + (round(random.expovariate(lambda_), 3) / 100) #timestamp of arrival event
        if nextArrivalTime < simulationEndTime:
            newEvent = engine.Event()
            newEvent.randomEventType()
            newEvent.setEventTimestamp(nextArrivalTime)
            schedule_event(newEvent)
            num_cars += 1
        time = nextArrivalTime
        
    
def onArrival(event):
    #### PARSING ARRIVALS ####
    # Basically, I am looking through the FEL to see what deal with events
    if (event.eventType == "AW"):
        luckie_intersection.westQueue.put(objects.Vehicle(event.timestamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AE"):
        olympic_intersection.eastQueue.put(objects.Vehicle(event.timestamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AN1"):
        luckie_intersection.northQueue.put(objects.Vehicle(event.timestamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AN2"):
        olympic_intersection.northQueue.put(objects.Vehicle(event.timestamp))
        initial_num_vehicles + - 1
    elif (event.eventType == "AS1"):
        luckie_intersection.southQueue.put(objects.Vehicle(event.timestamp))
    elif (event.eventType == "AS2"):
        olympic_intersection.southQueue.put(objects.Vehicle(event.timestamp))


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
        scheduleArrivals(avg)
        vehicle_num -= 1

       

# Populating FEL w/ schedualed light changes
def populateLightChanges(time):
    newEvent = engine.Event()
    newEvent.lightChangeType()
    newEvent.setEventTimestamp(time*30)
    schedule_event(newEvent)

def get_num_vehicles(hour):
    x = hour
    east = -0.0098*(x**5) + 0.6157*(x**4) + -13.8048*(x**3) + 125.8024*(x**2) + -337.2493*x + 273.2855
    west = -0.0084*(x**5) + 0.5114*(x**4) + -11.3061*(x**3) + 102.2751*(x**2) + -205.6825*x + 218.7994
    total = round(east + west, 0)
    return total


def checkIfSimLive():
    return True


itter += 1
populateLightChanges(itter)

scheduleArrivals()

while itter < 1000:
    event = fel.get()
    event.whoami()
    #If Event Type is an Arrival Event (arrival of vehicle)
    if event.eventType[0] == 'A':
        onArrival(event)

    if event.eventType == 'LC':
        onLightChange(event)
        populateLightChanges(itter)
        itter += 1

print("Number of cars: " + str(num_cars))
print("Total number of cars processed by sim " + str(olympic_intersection.exits + luckie_intersection.exits))
print("Number of cars exited from luckie intersection: " + str(luckie_intersection.exits))
print("Number of cars exited from olympic intersection: " + str(olympic_intersection.exits))

