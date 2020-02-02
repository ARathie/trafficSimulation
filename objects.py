# This file holds all of the definitions of the objects
import engine
import mainWorld
import queue


class World:
    def __init__(self):

        #             |           |                   |           |
        #             |           |                   |           |
        #             |           |    Bobby Dodd     |           |
        #             |northQ     |                   |northQ     |
        # ============            ====================            =======
        #                         eastQueue                       eastQueue         
        #                                                 

        #     westQueue                      westQueue
        # ============            ====================            =======
        #             |     southQ|                   |     southQ|
        #             |           |                   |           |
        #             |           |                   |           |
        #             |  Luckie   |                   |  Olympic  |


        luckie_intersection = Intersection()
        olympic_intersection = Intersection()
        
 
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

class Vehicle:
    
    def __init__(self, arrival_time, valid):
        self.arrival_time = start

        # Valid means that it is a vehicle that will count for data collection
        # A vehicles is valid if it has only been on North Avenue and no other streets in the sim
        # If a vehicle turns off North Avenue early, change valid to False
        self.valid = valid

        # Exit time is -1 if vehicle has not exited the simulation corridor yet
        self.exit_time = -1


    def exitVehicle(self, end):
        self.exit_time = current_time
        self.finished = True
        self.time = self.end - self.start + 20