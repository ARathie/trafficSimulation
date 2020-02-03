# The Event class 

import random
import objects
from queue import PriorityQueue

current_time = 0.0
fel = PriorityQueue()

class Event:

    #initializes an Event object, default type is '' and
    #timestamp is 0
    def __init__(self, eventType = '', timeStamp = 0):
        self.event_type = eventType
        self.timestamp = timeStamp

    def __lt__(self, other):
        return self.timeStamp < other.timeStamp

    def __eq__(self, other):
        return self.timeStamp == other.timeStamp

    #prints the event type and timestamp
    def whoami(self):
        print(self.eventType + ", " + str(self.timeStamp))

    #sets the event type
    def setEventType(self, etype):
        self.eventType = etype

    #sets the timestamp of the event
    def setEventTimeStamp(self, timestamp):
        self.timeStamp = timestamp

    #pseudo-randomly assigns event type for arrivals
    def randomEventType(self):
        #if we have traffic data, we can change it so that
        #for example 40% traffic comes from east, 30% from west,
        # and 10% from north/south. Then we can randomly
        #pick from those.
        randNum = random.randint(1,7) #pseudo-randomly outputs 1-6
        if randNum == 1:
            self.setEventType('AE') #vehicle arrives from east
        elif randNum == 2:
            self.setEventType('AW') #vehicle arrives from west
        elif randNum == 3:
            self.setEventType('AN1') #vehicle arrives from north 1
        elif randNum == 4:
            self.setEventType('AN2') #vehicle arrives from north 2
        elif randNum == 5:
            self.setEventType('AS1') #vehicle arrives from south 1
        else:
            self.setEventType('AS2') #vehicle arrives from south 2

    def lightChangeType(self):
        self.setEventType("LC") #an event for light changes

def schedule_event(event: Event):
    #commenting this out bc I think the fel should 
    #contain event objects, not just timestamps.
    #if fel only contains timestamps, how will we 
    #know what kind of event it is, and thus
    #how will we be able to process it?
    #fel.put(event.timeStamp)
    fel.put(event)