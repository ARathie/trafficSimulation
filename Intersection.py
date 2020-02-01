# The Intersection class 

import queue 

class Intersection:

    #The intersection's traffic queues. 
    #The direction refers to the direction
    #the traffic is *coming* from.
    eastQueue = queue.Queue()
    westQueue = queue.Queue()
    northQueue = queue.Queue()
    southQueue = queue.Queue()

    #initializes an Intersection object
    #If no light values specified, the default is 
    #west/east lights are green, north/south lights are red
    def __init__(self, northLight = 'red', southLight = 'red',
                    eastLight = 'green', westLight = 'green'):
        self.northLight = northLight
        self.southLight = southLight
        self.eastLight = eastLight
        self.westLight = westLight



