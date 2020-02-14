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
num_cars_in = 0
num_cars_out = 0
num_ppl_in = 0
num_ppl_out = 0
###########################

###########################
#  DATA
time_array = np.array([])
# each element represents a 10 minute period starting at 12:00, 12pm --> 4pm
arrival_rates = np.array([390, 269, 184, 186, 177, 437, 1026, 1800, 1904, 1792, 1539, 1505, 1579, 1669, 1526, 1686, 1626, 1163, 1443, 1405, 1204, 1023, 900, 603])

#number of cars per every 10 minutes: 
#this is the array of lambdas for the exponential distribution function
arrival_rate_lambdas = arrival_rates / 10

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

#generates a time block array in 10 minute increments 
def generateTimeBlockArray(startTime, endTime):
    numHours = endTime - startTime
    num10minBlocks = int((numHours * 60) / 10)
    timeBlockArray = [startTime]
    arrayTime = startTime * 100
    for i in range(1, num10minBlocks + 1):
        if (i % 6) == 0:
            arrayTime -= 50
            arrayTime += 100
        else:
            arrayTime += 10
        timeBlockArray.append(arrayTime / 100)
    return timeBlockArray

# schedules vehicle arrival events within a start and end time
# (startTime, endTime) should be integers representing hours in 24-hour time,
# for example, (13, 17), (12, 15), etc.
def scheduleArrivals(startTime, endTime):
    global arrival_rate_lambdas
    time = startTime
    timeBlockArray = generateTimeBlockArray(startTime, endTime)

    for i in range(len(arrival_rate_lambdas)):
        while (i < (len(timeBlockArray) - 1)) and (time < timeBlockArray[i+1]):
            lambda_ = arrival_rate_lambdas[i]
            nextArrivalTime = round(time + random.expovariate(lambda_), 3) #timestamp of arrival event
            time = nextArrivalTime
            if nextArrivalTime < endTime:
                newEvent = engine.Event()
                newEvent.randomEventType()
                newEvent.setEventTimestamp(nextArrivalTime)
                schedule_event(newEvent)
    
def onArrival(event):
    #### PARSING ARRIVALS ####
    # Basically, I am looking through the FEL to see what deal with events
    global num_cars_in, num_ppl_in
    num_cars_in += 1
    car = objects.Vehicle(event.timestamp)
    num_ppl_in += car.passengers
    if (event.eventType == "AW"):
        luckie_intersection.westQueue.put(car)
        initial_num_vehicles + - 1
    elif (event.eventType == "AE"):
        olympic_intersection.eastQueue.put(car)
        initial_num_vehicles + - 1
    elif (event.eventType == "AN1"):
        luckie_intersection.northQueue.put(car)
        initial_num_vehicles + - 1
    elif (event.eventType == "AN2"):
        olympic_intersection.northQueue.put(car)
        initial_num_vehicles + - 1
    elif (event.eventType == "AS1"):
        luckie_intersection.southQueue.put(car)
    elif (event.eventType == "AS2"):
        olympic_intersection.southQueue.put(car)


def onLightChange(event):
    # FOR NORTH-SOUTH
    if luckie_intersection.lights[0] is 1:
        for i in range(0, luckie_intersection.carsToBeLetThrough(30, 30)):
            # FIRST WE POP THE LUCKIE INTERSECTION
            if not luckie_intersection.northQueue.empty():
                popped = luckie_intersection.northQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    exitVehicle(popped)
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    olympic_intersection.westQueue.put(popped)
                else:
                    exitVehicle(popped)
                    luckie_intersection.exits += 1

            if not luckie_intersection.southQueue.empty():
                popped = luckie_intersection.southQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    exitVehicle(popped)
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    exitVehicle(popped)
                    luckie_intersection.exits += 1
                else:
                    olympic_intersection.westQueue.put(popped)

            # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.northQueue.empty():
                popped = olympic_intersection.northQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    exitVehicle(popped)
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    exitVehicle(popped)
                    olympic_intersection.exits += 1
                else:
                    luckie_intersection.eastQueue.put(popped)

            if not olympic_intersection.southQueue.empty():
                popped = olympic_intersection.southQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    exitVehicle(popped)
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    luckie_intersection.eastQueue.put(popped)
                else:
                    exitVehicle(popped)
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
                    exitVehicle(popped)
                    luckie_intersection.exits += 1
                else:
                    exitVehicle(popped)
                    luckie_intersection.exits += 1

            if not luckie_intersection.eastQueue.empty():
                popped = luckie_intersection.eastQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    exitVehicle(popped)
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    exitVehicle(popped)
                    luckie_intersection.exits += 1
                else:
                    exitVehicle(popped)
                    luckie_intersection.exits += 1

            # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.westQueue.empty():
                popped = olympic_intersection.westQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    exitVehicle(popped)
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    exitVehicle(popped)
                    olympic_intersection.exits += 1
                else:
                    exitVehicle(popped)
                    olympic_intersection.exits += 1

            if not olympic_intersection.eastQueue.empty():
                popped = olympic_intersection.eastQueue.get()
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    luckie_intersection.eastQueue.put(popped)
                elif popped.direction == "L":
                    exitVehicle(popped)
                    olympic_intersection.exits += 1
                else:
                    exitVehicle(popped)
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

def get_num_vehicles():
    east = -0.0098*(x**5) + 0.6157*(x**4) + -13.8048*(x**3) + 125.8024*(x**2) + -337.2493*x + 273.2855
    west = -0.0084*(x**5) + 0.5114*(x**4) + -11.3061*(x**3) + 102.2751*(x**2) + -205.6825*x + 218.7994
    total = round(east + west, 0)

def generate_arrivals(time_interval): # time interval in tuple form ie (12, 15)
    
    # global current_time
    # interarrival = math.ceil(NR.exponential(avg)) #time until next arrival event
    # nextArrivalTime = current_time + interarrival
    # current_time = nextArrivalTime
    # newEvent = engine.Event()
    # newEvent.randomEventType()
    # newEvent.setEventTimestamp(nextArrivalTime)
    # schedule_event(newEvent)

    global arrival_rates
    relevant_arrival_rates = arrival_rates[time_interval[0]: time_interval[1]]

    global num_cars
    for i in range(len(relevant_arrival_rates)):
        for _ in range(relevant_arrival_rates[i]):
            event = engine.Event()
            event.randomEventType()
            minutes = (time_interval[1] - time_interval[0])*60
            event.setEventTimestamp(i + time_interval[0] + round(NR.uniform(0, minutes)/60.0, 3)) # TODO: Change timestamp to a stochastic time stamp
            schedule_event(event)
            num_cars += 1

def exitVehicle(car):
    from engine import current_time
    global num_ppl_out, num_cars_out, time_array
    num_cars_out += 1
    num_ppl_out += int(car.passengers)
    car.exit_time = current_time
    car.finished = True
    car.time = car.exit_time - car.arrival_time + 20


    time_array = np.append(time_array, np.array([car.time]))

def checkIfSimLive():
    return True


itter += 1
populateLightChanges(itter)

#generate_arrivals((12, 15))
scheduleArrivals(12,15)

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

print()
print("Number of cars that entered simulation: " + str(num_cars_in))
print("Number of cars that exited simulation: " + str(num_cars_out))
print()
print("Number of people that entered simulation: " + str(num_ppl_in))
print("Number of people that exited simulation: " + str(num_ppl_out))
print()
print("Total number of cars processed by sim " + str(olympic_intersection.exits + luckie_intersection.exits))
print("Average time spent in simulation " + str(np.mean(time_array)))
print()
print("Number of cars exited from luckie intersection: " + str(luckie_intersection.exits))
print("Number of cars exited from olympic intersection: " + str(olympic_intersection.exits))

