# This file holds all of the definitions of the objects
import queue
import random


pass_arr = [1, 2, 1, 3, 1, 2, 2, 3, 4, 1]

class Intersection:
    # The intersection's traffic queues.
    # The direction refers to the direction
    # the traffic is *coming* from.

    # initializes an Intersection object
    # If no light values specified, the default is
    # west/east lights are green (1), north/south lights are red (0)
    def __init__(self, northLight=0, southLight=0, eastLight=1, westLight=1):
        self.lights = [northLight, southLight, eastLight, westLight]
        self.exits = 0
        self.eastQueue = queue.Queue()
        self.westQueue = queue.Queue()
        self.northQueue = queue.Queue()
        self.southQueue = queue.Queue()

    def lightChanges(self):
        i = 0
        while i < 4:
            if self.lights[i] == 1:
                self.lights[i] = 0
            else:
                self.lights[i] = 1
            i += 1

    # def carsToBeLetThrough(self, light_time, speed_limit):
    #     return speed_limit + light_time


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

        self.luckie_intersection = Intersection()
        self.olympic_intersection = Intersection()

    def changeTheLights(self):
        self.luckie_intersection.lightChanges()
        self.olympic_intersection.lightChanges()


class Vehicle:
    
    def __init__(self, arrival_time = 0, valid = True):
        self.time = 0
        self.arrival_time = arrival_time
        self.direction = self.chooseDirection()
        # Valid means that it is a vehicle that will count for data collection
        # A vehicles is valid if it has only been on North Avenue and no other streets in the sim
        # If a vehicle turns off North Avenue early, change valid to False
        self.valid = valid

        # The number of people in the car
        rand_pass = random.randrange(10)
        self.passengers = pass_arr[rand_pass]

        # Exit time is -1 if vehicle has not exited the simulation corridor yet
        self.exit_time = -1
        self.id = random.randint(1, 100000000)

    def __str__(self):
        return self.id

    def chooseDirection(self):
        # A direction will need to be specified to know who is going where
        randNum = random.randint(1, 3)  # chooses between 1-3, where 1 is forward, 2 is left, 3 is right.
        if randNum == 1:
            return "F"
        elif randNum == 2:
            return "L"
        elif randNum == 3:
            return "R"
