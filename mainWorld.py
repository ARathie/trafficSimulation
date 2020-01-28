import numpy.random as NR
import math
import Event

from queue import PriorityQueue

fel = PriorityQueue() #the future event list
currTime = 0

avg = 3 #the average rate of arrival of vehicles (to be changed later)
def scheduleNextArrival(avg):
	global currTime
	interarrival = math.ceil(NR.exponential(avg)) #time until next arrival event
	nextArrivalTime = currTime + interarrival
	currTime = nextArrivalTime
	newEvent = Event.Event("Arrival", nextArrivalTime)
	fel.put(newEvent)


vehicles = 0 #0 vehicles at start of simulation
while vehicles < 10:
	scheduleNextArrival(avg)
	fel.get().whoami() #prints out the event
	vehicles += 1
