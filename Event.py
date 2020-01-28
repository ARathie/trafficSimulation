# The Event class 

from enum import Enum

class Event:

    EventTypes =  Enum('Arrival', 'Departure')

    def __init__(self, eventType, timeStamp):
        self.eventType = eventType
        self.timeStamp = timeStamp

    #prints the event type and timestamp
    def whoami(self):
    	print(self.eventType + ", " + str(self.timeStamp))

 