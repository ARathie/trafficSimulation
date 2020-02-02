import numpy.random as NR
import math
import Event
import Intersection

from queue import PriorityQueue

#a startup method with some kind of simulation
#initialization behavior. for now prints
#the name of the simulator in ascii and instantiates
#2 intersections
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

	#Initialize the 2 intersections
	intersection1 = Intersection.Intersection()
	intersection2 = Intersection.Intersection()

startup()
fel = PriorityQueue() #the future event list
currTime = 0

avg = 3 #the average rate of arrival of vehicles (to be changed later)

#schedules arrival events for vehicles coming from East and West
def scheduleNextArrival(avg):
	global currTime
	interarrival = math.ceil(NR.exponential(avg)) #time until next arrival event
	nextArrivalTime = currTime + interarrival
	currTime = nextArrivalTime
	newEvent = Event.Event()
	newEvent.randomEventType()
	newEvent.setEventTimeStamp(nextArrivalTime)
	fel.put(newEvent)


vehicles = 0 #0 vehicles at start of simulation
while vehicles < 10:
	scheduleNextArrival(avg)
	fel.get().whoami() #prints out the event
	vehicles += 1