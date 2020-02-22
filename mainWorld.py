# This file is the simulation application
# This files holds the state variables and event procedure
import sys

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
num_ppl = 0

#start time that the simulation is MODELING, i.e.: SUI time between 0 hours to 23 hours
simulationStartTime = 1

#end time for the SUI, at which the simulation stops, 0 hours to 23 hours
simulationEndTime = 23
###########################

###########################
#  DATA

# each element represents a 10 minute period starting at 12:00, 12pm --> 4pm
arrival_rates = np.array([390, 269, 184, 186, 177, 437, 1026, 1800, 1904, 1792, 1539, 1505, 1579, 1669, 1526, 1686, 1626, 1163, 1443, 1405, 1204, 1023, 900, 603])

###########################
if len(sys.argv) > 3:
    speed_limit = int(sys.argv[1])
    luckie_time = int(sys.argv[2])
    olympic_time = int(sys.argv[3])
    ped_walk = int(sys.argv[4])
    delay = int(sys.argv[5])

else:
    olympic_time = 30
    luckie_time = 30
    speed_limit = 30
    ped_walk = False
    delay = 0


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

###########################
# EASE OF USE
luckie_intersection = world.luckie_intersection
olympic_intersection = world.olympic_intersection


###########################


# schedules vehicle arrival events 
def scheduleArrivals():
    global arrival_rate_lambdas
    global num_cars
    global num_ppl
    time = simulationStartTime

    while time < simulationEndTime:

        #the lambda: (cars per minute, given a time in hours)
        lambda_ = get_num_vehicles(time) / 60
        nextArrivalTime = time + (round(random.expovariate(lambda_), 3) / 60) #timestamp of arrival event
        if nextArrivalTime < simulationEndTime:
            newEvent = engine.Event()
            newEvent.randomEventType()
            newEvent.setEventTimestamp(nextArrivalTime)
            schedule_event(newEvent)
            
            global num_ppl, num_cars
            num_cars += 1
            car = objects.Vehicle(newEvent.timestamp, newEvent.event_type)
            num_ppl += car.passengers
        time = nextArrivalTime
        
    
def onArrival(event):
    #### PARSING ARRIVALS ####
    # Basically, I am looking through the FEL to see what deal with events
    if (event.eventType == "AW"):
        luckie_intersection.westQueue.put(objects.Vehicle(event.timestamp, "AW"))
    elif (event.eventType == "AE"):
        olympic_intersection.eastQueue.put(objects.Vehicle(event.timestamp, "AE"))
    elif (event.eventType == "AN1"):
        luckie_intersection.northQueue.put(objects.Vehicle(event.timestamp, "AN1"))
    elif (event.eventType == "AN2"):
        olympic_intersection.northQueue.put(objects.Vehicle(event.timestamp, "AN2"))
    elif (event.eventType == "AS1"):
        luckie_intersection.southQueue.put(objects.Vehicle(event.timestamp, "AS1"))
    elif (event.eventType == "AS2"):
        olympic_intersection.southQueue.put(objects.Vehicle(event.timestamp, "AS2"))


def get_time_to_move(x):
    if x == 0:
        return 0
    return 7 * math.log(x)
    # return 1 + (2*x)
    # return 1 + (x/64) + ((x**2)/256) + ((x**3)/1024) + ((x**4)/8096)

def carsToBeLetThrough(light_time, speed_limit):
    count = 0  # number of cars let through
    avg_accel = 7.5  # 3.5 m/s^2 is the average acceleration rate of cars
    avg_len = 4.5  # average car length is 4.5m
    avg_btw = 1.5  # assumed distance between each car

    time_get_to_lim = speed_limit / avg_accel  # time it takes car to get to speed limit
    dist_trav_to_lim = (avg_accel * (time_get_to_lim ** 2) / 2)  # distance traveled getting to limit

    able_to_go = True  # bool for saying if cars will still be able to make it through intersection
    while able_to_go:
        st_time = get_time_to_move(count)
        # print(st_time)
        dist_to_go = (avg_len + avg_btw) * count

        if (dist_to_go > dist_trav_to_lim):  # if car gets to speed limit before intersection
            dist_to_go2 = dist_to_go - dist_trav_to_lim  # dist left after getting to limit
            time_to_get_to_inter = dist_to_go2 / speed_limit

            if (st_time + time_get_to_lim + time_to_get_to_inter) < light_time:
                count += 1
            else:
                able_to_go = False
        else:
            time_to_get_to_inter = math.sqrt((2 * dist_to_go) / avg_accel)
            if (st_time + time_to_get_to_inter) < light_time:
                count += 1
            else:
                able_to_go = False

    return count

luckie_cars_through = carsToBeLetThrough(luckie_time, speed_limit)
olympic_cars_through = carsToBeLetThrough(olympic_time, speed_limit)

def onLightChange(event):
    # FOR NORTH-SOUTH
    if luckie_intersection.lights[0] is 1:
        for i in range(luckie_cars_through):
            # FIRST WE POP THE LUCKIE INTERSECTION
            if not luckie_intersection.northQueue.empty():
                popped = luckie_intersection.northQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = luckie_intersection.northQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    if not (olympic_intersection.westQueue.qsize() > 6):
                        popped = luckie_intersection.northQueue.get()
                        popped.middle = True
                        olympic_intersection.westQueue.put(popped)
                else:
                    popped = luckie_intersection.northQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1

            if not luckie_intersection.southQueue.empty():
                popped = luckie_intersection.southQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = luckie_intersection.southQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    popped = luckie_intersection.southQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    if not (olympic_intersection.westQueue.qsize() > 6):
                        popped = luckie_intersection.southQueue.get()
                        popped.middle = True
                        olympic_intersection.westQueue.put(popped)
        for i in range(olympic_cars_through):
            # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.northQueue.empty():
                popped = olympic_intersection.northQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = olympic_intersection.northQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    popped = olympic_intersection.northQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    if not (luckie_intersection.eastQueue.qsize() > 6):
                        popped = olympic_intersection.northQueue.get()
                        popped.middle = True
                        luckie_intersection.eastQueue.put(popped)

            if not olympic_intersection.southQueue.empty():
                popped = olympic_intersection.southQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = olympic_intersection.southQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    if not (luckie_intersection.eastQueue.qsize() > 6):
                        popped = olympic_intersection.southQueue.get()
                        popped.middle = True
                        luckie_intersection.eastQueue.put(popped)
                else:
                    popped = olympic_intersection.southQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
    # FOR EAST-WEST
    else:
        for i in range(luckie_cars_through):
            # FIRST WE POP THE LUCKIE INTERSECTION
            if not luckie_intersection.westQueue.empty():
                popped = luckie_intersection.westQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    if not (olympic_intersection.westQueue.qsize() > 6):
                        popped = luckie_intersection.westQueue.get()
                        popped.middle = True
                        olympic_intersection.westQueue.put(popped)
                elif popped.direction == "L":
                    popped = luckie_intersection.westQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    popped = luckie_intersection.westQueue.get()
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

        for i in range(olympic_cars_through):
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
                popped = olympic_intersection.eastQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    if not (luckie_intersection.eastQueue.qsize() > 6):
                        popped = olympic_intersection.eastQueue.get()
                        popped.middle = True
                        luckie_intersection.eastQueue.put(popped)
                elif popped.direction == "L":
                    popped = olympic_intersection.eastQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    popped = olympic_intersection.eastQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
    world.changeTheLights()

def onLightChange2(event):
    if luckie_intersection.lights[0] is 1:
        for i in range(olympic_cars_through):
            # FIRST WE POP THE LUCKIE INTERSECTION
            if not luckie_intersection.northQueue.empty():
                popped = luckie_intersection.northQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = luckie_intersection.northQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    if not (olympic_intersection.westQueue.qsize() > 6):
                        popped = luckie_intersection.northQueue.get()
                        popped.middle = True
                        olympic_intersection.westQueue.put(popped)
                else:
                    popped = luckie_intersection.northQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1

            if not luckie_intersection.southQueue.empty():
                popped = luckie_intersection.southQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = luckie_intersection.southQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                elif popped.direction == "L":
                    popped = luckie_intersection.southQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    if not (olympic_intersection.westQueue.qsize() > 6):
                        popped = luckie_intersection.southQueue.get()
                        popped.middle = True
                        olympic_intersection.westQueue.put(popped)
        for i in range(olympic_cars_through):
            # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.northQueue.empty():
                popped = olympic_intersection.northQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = olympic_intersection.northQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    popped = olympic_intersection.northQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    if not (luckie_intersection.eastQueue.qsize() > 6):
                        popped = olympic_intersection.northQueue.get()
                        popped.middle = True
                        luckie_intersection.eastQueue.put(popped)

            if not olympic_intersection.southQueue.empty():
                popped = olympic_intersection.southQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    popped = olympic_intersection.southQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                elif popped.direction == "L":
                    if not (luckie_intersection.eastQueue.qsize() > 6):
                        popped = olympic_intersection.southQueue.get()
                        popped.middle = True
                        luckie_intersection.eastQueue.put(popped)
                else:
                    popped = olympic_intersection.southQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
    # FOR EAST-WEST
    else:
        delay2 = delay
        delay3 = delay
        for i in range(olympic_cars_through):
            if not luckie_intersection.westQueue.empty():
                popped = luckie_intersection.westQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    if not (olympic_intersection.westQueue.qsize() > 6):
                        popped = luckie_intersection.westQueue.get()
                        popped.middle = True
                        olympic_intersection.westQueue.put(popped)
                elif popped.direction == "L":
                    popped = luckie_intersection.westQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1
                else:
                    popped = luckie_intersection.westQueue.get()
                    popped.exitVehicle()
                    luckie_intersection.exits += 1

            if delay2 == 0:
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
            else:
                delay2 = delay2 - 1
        # NOW WE POP THE OLYMPIC INTERSECTION
            if not olympic_intersection.eastQueue.empty():
                popped = olympic_intersection.eastQueue.queue[0]
                popped.direction = popped.chooseDirection()
                if popped.direction == "F":
                    if not (luckie_intersection.eastQueue.qsize() > 6):
                        popped = olympic_intersection.eastQueue.get()
                        popped.middle = True
                        luckie_intersection.eastQueue.put(popped)
                elif popped.direction == "L":
                    popped = olympic_intersection.eastQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1
                else:
                    popped = olympic_intersection.eastQueue.get()
                    popped.exitVehicle()
                    olympic_intersection.exits += 1

            if delay3 == 0:
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
            else:
                delay3 = delay3 - 1
    world.changeTheLights()

# Populating FEL w/ schedualed light changes
def populateLightChanges(time):
    if time % 2 or not ped_walk:
        newEvent = engine.Event()
        newEvent.lightChangeType()
        newEvent.setEventTimestamp(time*0.00833333)
        schedule_event(newEvent)
    else:
        pedWalkTime(time)

def get_num_vehicles(hour):
    x = hour
    east = -0.0098*(x**5) + 0.6157*(x**4) + -13.8048*(x**3) + 125.8024*(x**2) + -337.2493*x + 273.2855
    west = -0.0084*(x**5) + 0.5114*(x**4) + -11.3061*(x**3) + 102.2751*(x**2) + -205.6825*x + 218.7994
    total = round(east + west, 0)
    return total

def pedWalkTime(time):
    newEvent = engine.Event()
    newEvent.pedWalkType()
    newEvent.setEventTimestamp(time*0.00833333)
    schedule_event(newEvent)

def checkIfSimLive():
    return True


itter += 1
populateLightChanges(itter)

scheduleArrivals()

while engine.current_time < simulationEndTime:
    event = fel.get()
    event.whoami()
    engine.current_time = event.timestamp
    #If Event Type is an Arrival Event (arrival of vehicle)
    if event.eventType[0] == 'A':
        onArrival(event)

    if event.eventType == 'LC':
        onLightChange2(event)
        populateLightChanges(itter)
        itter += 1

    if event.eventType == "PW":
        populateLightChanges(itter)
        itter += 1

avg_time = 0
len = 0
for i in objects.departed_cars:
    if i[1]:
        avg_time += i[0]
        #print(i[0])
        len += 1

if len != 0:
    avg_time = avg_time/len


print("Number of cars: " + str(num_cars))
print("Total number of cars processed by sim: " + str(olympic_intersection.exits + luckie_intersection.exits))
print("Total number of people processed by sim: ", num_ppl)
print("Number of cars exited from luckie intersection: " + str(luckie_intersection.exits))
print("Number of cars exited from olympic intersection: " + str(olympic_intersection.exits))

if len != 0:
    print("Average time spent in corridor: " + str(round(avg_time*60*60, 5)) + " seconds")
else:
    print("Delay parameter too high. Try a lower delay for\n"
        "accurate Average Time Spent stats.")
