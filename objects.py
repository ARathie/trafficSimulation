# This file holds all of the definitions of the objects
import queue
import random
import math as math

departed_cars = list()
pass_arr = [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,3,3,4]

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

    def turnOffLights(self):
        i = 0
        while i < 4:
            self.lights[i] = 0

    def resetTheLights(self):
        self.northLight = 0
        self.southLight = 0
        self.eastLight = 1
        self.westLight = 1

    def carsToBeLetThrough(self, light_time, speed_limit=30):
        return speed_limit + light_time


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

    def lightsOff(self):
        self.luckie_intersection.turnOffLights()
        self.olympic_intersection.turnOffLights()

    def lightReset(self):
        self.luckie_intersection.resetTheLights()
        self.olympic_intersection.resetTheLights()


class Vehicle:
    def __init__(self, arrival_time, start, valid = True):
        self.arrival_time = arrival_time
        # Valid means that it is a vehicle that will count for data collection
        # A vehicles is valid if it has only been on North Avenue and no other streets in the sim
        # If a vehicle turns off North Avenue early, change valid to False
        self.valid = valid
        self.start = start
        self.middle = False
        # Exit time is -1 if vehicle has not exited the simulation corridor yet
        self.exit_time = -1
        self.id = random.randint(1, 100000000)
        self.direction = self.chooseDirection()
        rand_pass = random.randrange(20)
        self.passengers = pass_arr[rand_pass]

    def __str__(self):
        return self.id

    def chooseDirection(self):
        # A direction will need to be specified to know who is going where

        # chooses between 1-3, where 1 is forward, 2 is left, 3 is right.
        if self.start == "AS1" or "AS2" or "AN1" or "AN2":
            randNum = random.randint(1, 3)
            if randNum == 1:
                return "F"
            elif randNum == 2:
                return "L"
            elif randNum == 3:
                return "R"
        if self.start == "AE" or "AW":
            randNum = random.randint(1, 4)
            if randNum == 1 or 2:
                return "F"
            elif randNum == 3:
                return "L"
            elif randNum == 4:
                return "R"

    def exitVehicle(self):
        from engine import current_time
        self.exit_time = current_time
        self.finished = True
        self.time = self.exit_time - self.arrival_time
        departed_cars.append((self.time, self.middle, self.passengers, self.start))

    def get_time_to_move(x):
        if x == 0:
            return 0
        return 10 * math.log(x)
        # return 1 + (2*x)
        # return 1 + (x/64) + ((x**2)/256) + ((x**3)/1024) + ((x**4)/8096)

    def carsToBeLetThrough(self, light_time, speed_limit):
        count = 0  # number of cars let through
        avg_accel = 7.5  # 3.5 m/s^2 is the average acceleration rate of cars
        avg_len = 4.5  # average car length is 4.5m
        avg_btw = 1.5  # assumed distance between each car

        time_get_to_lim = speed_limit / avg_accel  # time it takes car to get to speed limit
        dist_trav_to_lim = (avg_accel * (time_get_to_lim ** 2) / 2)  # distance traveled getting to limit

        able_to_go = True  # bool for saying if cars will still be able to make it through intersection
        while able_to_go:
            st_time = self.get_time_to_move(count)
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
