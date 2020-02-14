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
itter = 0  # to put light changes at fixed rates
start = 12 # starting hour
end = 15 # ending hour
###########################

###########################
#  DATA
speed_limit = 10 # road speed limit (m/s for simplicity)
light_time = 300 # time of each light cycle (in seconds)
car_count = 0 # number of cars let through each light change
###########################

###########################
# DATA COLLECTION VARIABLES
time_array = np.array([]) # array of times that cars spent in simulation
num_cars_in = 0 # cars that entered the sim
num_cars_out = 0 # cars that made it through the sim
num_ppl_in = 0 # ppl that entered the sim
num_ppl_out = 0 # ppl that made it through the sim
###########################

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

###########################
# EASE OF USE
luckie_intersection = world.luckie_intersection
olympic_intersection = world.olympic_intersection
###########################

# Returns the maximum number of cars that will let through on a light change
# Dependent on speed limit and light time only
def carsToBeLetThrough(light_time, speed_limit):
    count = 0 # number of cars let through
    avg_accel = 3.5 # 3.5 m/s^2 is the average acceleration rate of cars
    avg_len = 4.5 # average car length is 4.5m
    avg_btw = 1.0 # assumed a meter between each car

    time_get_to_lim = speed_limit/avg_accel # time it takes car to get to speed limit
    dist_trav_to_lim = (avg_accel*(time_get_to_lim**2)/2) # distance traveled getting to limit
    print(dist_trav_to_lim)

    able_to_go = True # bool for saying if cars will still be able to make it through intersection
    while able_to_go:
        st_time = get_time_to_move(count)
        dist_to_go = (avg_len + avg_btw) * count
        if (dist_to_go > dist_trav_to_lim): # if car gets to speed limit before intersection
            dist_to_go2 = dist_to_go - dist_trav_to_lim # dist left after getting to limit
            time_to_get_to_inter = dist_to_go2/speed_limit
            if (st_time + time_get_to_lim + time_to_get_to_inter) < light_time:
                count += 1
            else:
                able_to_go = False
        else:
            time_to_get_to_inter = math.sqrt((2*dist_to_go)/avg_accel)
            if (st_time + time_to_get_to_inter) < light_time:
                count += 1
            else:
                able_to_go = False

    return count

# Returns time after light turns green for car to start moving
# Assumed to be an exponential type function
def get_time_to_move(x):
    return 1 + (x) + ((x**2)/64) + ((x**3)/512) + ((x**4)/13824)

car_num = carsToBeLetThrough(light_time, speed_limit)
print(car_num)

#generates a time block array in 10 minute increments 
def generateTimeBlockArray(startTime, endTime):
    numHours = endTime - startTime
    num10minBlocks = int(numHours * 6)
    timeBlockArray = [startTime]
    arrayTime = startTime
    for i in range(1, num10minBlocks + 1):
        arrayTime += 0.1667
        timeBlockArray.append(round(arrayTime, 2))
    return timeBlockArray

# schedules vehicle arrival events within a start and end time
# (startTime, endTime) should be integers representing hours in 24-hour time,
# for example, (13, 17), (12, 15), etc.
def scheduleArrivals(startTime, endTime):
    timeBlockArray = generateTimeBlockArray(startTime, endTime)
    for time in timeBlockArray:
        total = round(get_num_arrivals(time) / 6) # gen function gives the amount of cars in an hour, div by 6
        for i in range(total):
            newEvent = engine.Event()
            newEvent.randomEventType()
            newEvent.setEventTimestamp(time)
            schedule_event(newEvent)
    
def onArrival(event):
    #### PARSING ARRIVALS ####
    # Basically, I am looking through the FEL to see what deal with events
    global num_cars_in, num_ppl_in, initial_num_vehicles
    num_cars_in += 1
    car = objects.Vehicle(event.timestamp)
    num_ppl_in += car.passengers
    if (event.eventType == "AW"):
        luckie_intersection.westQueue.put(car)
    elif (event.eventType == "AE"):
        olympic_intersection.eastQueue.put(car)
    elif (event.eventType == "AN1"):
        luckie_intersection.northQueue.put(car)
    elif (event.eventType == "AN2"):
        olympic_intersection.northQueue.put(car)
    elif (event.eventType == "AS1"):
        luckie_intersection.southQueue.put(car)
    elif (event.eventType == "AS2"):
        olympic_intersection.southQueue.put(car)


def onLightChange(event):
    # FOR NORTH-SOUTH
    global light_time, speed_limit
    if luckie_intersection.lights[0] is 1:
        for i in range(car_num):
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
        for i in range(car_num):
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

# Populating FEL w/ schedualed light changes
def populateLightChanges(time):
    newEvent = engine.Event()
    newEvent.lightChangeType()
    newEvent.setEventTimestamp(time*30)
    schedule_event(newEvent)

def get_num_arrivals(x):
    east = -0.0098*(x**5) + 0.6157*(x**4) + -13.8048*(x**3) + 125.8024*(x**2) + -337.2493*x + 273.2855
    west = -0.0084*(x**5) + 0.5114*(x**4) + -11.3061*(x**3) + 102.2751*(x**2) + -205.6825*x + 218.7994
    return round(east + west)

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

scheduleArrivals(start, end)

# how many times light will change in alotted time
# ((# of hours) * (3600sec/hour)) / length of light time in seconds
itter_max = (((end - start) * 3600) / light_time)
print(itter_max)
while itter < itter_max:
    event = fel.get()
    #event.whoami()
    #If Event Type is an Arrival Event (arrival of vehicle)
    if event.eventType[0] == 'A':
        onArrival(event)

    # If event is light change
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

