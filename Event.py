# The Event class 

import random

class Event:


    #initializes an Event object, default type is '' and
    #timestamp is 0
    def __init__(self, eventType = '', timeStamp = 0):
        self.eventType = eventType
        self.timeStamp = timeStamp

    #prints the event type and timestamp
    def whoami(self):
        print(self.eventType + ", " + str(self.timeStamp))

    #sets the event type
    def setEventType(self, etype):
        self.eventType = etype

    #sets the timestamp of the event
    def setEventTimeStamp(self, timestamp):
        self.timeStamp = timestamp

    #pseudo-randomly assigns event type
    def randomEventType(self):
        randNum = random.randint(1,3) #pseudo-randomly outputs 1 or 2
        if randNum == 1:
            self.setEventType('Arrival_East') #vehicle arrives from east
        else:
            self.setEventType('Arrival_West') #vehicle arrives from west

 