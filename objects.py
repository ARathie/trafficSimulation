# This file holds all of the definitions of the objects
import engine
import mainWorld

class World:
    def __init__(self):
        # Explanation of Variable naming: the cardinal direction denotes the direction that those
        # cars are traveling in. The number denotes which intersectection it is in.
        # 1 = N. Ave and Luckie St.
        # 2 = N. Ave and Centennial Olympic Park Drive

        #             |           |                   |           |
        #             |           |                   |           |
        #             |           |    Bobby Dodd     |           |
        #             |south1     |                   |south2     |
        # ============            ====================            =======
        #                         west1                            west2         
        #                  1                                2

        #         east1                          east2
        # ============            ====================            =======
        #             |     north1|                   |     north2|
        #             |           |                   |           |
        #             |           |                   |           |
        #             |  Luckie   |                   | Cent Olym |


        self.east1 = queue.Queue()
        self.east2 = queue.Queue()

        self.west1 = queue.Queue()
        self.west2 = queue.Queue()

        self.north1 = queue.Queue()
        self.north2 = queue.Queue()

        self.south1 = queue.Queue()
        self.south2 = queue.Queue()


        #Initialize world with some cars in the roads:
        for i in range(INITIAL_VEH):
            self.q10to11.put(Vehicle(0))
            self.q11to12.put(Vehicle(0))
            self.q12to13.put(Vehicle(0))
            self.q13to14.put(Vehicle(0))
 
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