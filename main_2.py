import random
from data_structs import *
class Plane:
    @classmethod
    def generate_plane(cls, probability_of_arrival, current_time):
        if random.random() < probability_of_arrival/100:
            return Plane(current_time, random.randint(1,3), random.randint(5,15))
        else:
            return None
    
    @classmethod
    def generate_plane_takeoff(cls, probability_of_takeoff, current_time):
        if random.random() < probability_of_takeoff/100:
            return Plane(current_time, random.randint(1,3), random.randint(5,15))
        else:
            return None

    def __init__(self, arrival_time, transaction_time, plane_fuel):
        self.arrival_time = arrival_time
        self.transaction_time = transaction_time
        self.plane_fuel = plane_fuel

    def arrival_time(self):
        return self.arrival_time

    def transaction_time(self):
        return self.transaction_time

    def serve(self):
        self.transaction_time -= 1

    def __lt__(self, other):
        return self.plane_fuel < other.plane_fuel

    def __le__(self, other):
        return self.plane_fuel <= other.plane_fuel

    def __eq__(self, other):
        return self.plane_fuel == other.plane_fuel

    def __gt__(self, other):
        return self.plane_fuel > other.plane_fuel

    def __ge__(self, other):
        return self.plane_fuel >= other.plane_fuel



class runway:
    def __init__(self):
        self.average_time_takeoff = 0
        self.average_time_landing = 0
        self.longest_wait_takeoff = 0
        self.longest_wait_landing = 0
        self.landing_queue = MinHeap()
        self.takeoff_queue = ArrayQueue()
        self.did_crash = False
        self.current_plane = None
        self.planes_total = 0
        self.time_waited = None
        self.takeoff_total = 0
        self.landing_total = 0

    def add_plane_landing(self, p):
        self.landing_queue.add(p)

    def add_plane_takeoff(self, p):
        self.takeoff_queue.add(p)

    def serve_plane(self, current_time):
            if self.landing_queue.is_empty() and self.takeoff_queue.is_empty():
                return
            elif self.landing_queue.is_empty() and not self.takeoff_queue.is_empty():
                if self.current_plane is None:
                    self.current_plane = self.takeoff_queue.pop()
                    self.takeoff_total += 1
                    self.time_waited = current_time - self.current_plane.arrival_time
                    self.average_time_takeoff = self.average_time_takeoff + self.time_waited
                    if self.time_waited > self.longest_wait_takeoff:
                        self.longest_wait_takeoff = self.time_waited
            else:
                if self.current_plane is None:
                    self.current_plane = self.landing_queue.pop()
                    self.landing_total += 1
                    self.time_waited = current_time - self.current_plane.arrival_time
                    self.average_time_landing = self.average_time_landing + self.time_waited
                    if self.current_plane.plane_fuel < self.time_waited:
                        self.did_crash = True
                    if self.time_waited > self.longest_wait_landing:
                        self.longest_wait_landing = self.time_waited
    
            self.current_plane.serve()
            if self.current_plane.transaction_time == 0:
                self.current_plane = None
                self.planes_total += 1

    
    def print_stats(self):
        print("Longest Wait Landing: " + str(self.longest_wait_landing))
        print("Longest Wait Takeoff: " + str(self.longest_wait_takeoff))
        print("Did Crash: " + str(self.did_crash))
        print("Total Planes: " + str(self.planes_total))
        if self.landing_total == 0:
            print("Average Time Landing: 0")
        else:
            print("Average Time Landing: " + str(self.average_time_landing / self.landing_total))
        if self.takeoff_total == 0:
            print("Average Time Takeoff: 0")
        else:
            print("Average Time Takeoff: " + str(self.average_time_takeoff  / self.takeoff_total))

class ATC:

    def __init__(self, lenth, odds_of_new_plane, odds_of_takeoff):
        self.sim_lenth = lenth
        self.odds_of_new_plane = odds_of_new_plane
        self.odds_of_takeoff = odds_of_takeoff
        self.runway = runway()

    def run_simulation(self):
        for i in range(self.sim_lenth):
            new_arrival = Plane.generate_plane(self.odds_of_new_plane, i)
            new_takeoff = Plane.generate_plane_takeoff(self.odds_of_takeoff, i)

            if new_arrival is not None:
                self.runway.add_plane_landing(new_arrival)
            if new_takeoff is not None:
                self.runway.add_plane_takeoff(new_takeoff)
            
            
            self.runway.serve_plane(i)

        self.runway.print_stats()
    
def main():

    num_arrivals = 100
    num_departures = 25
    num_of_simulations = 100

    p = ATC(num_of_simulations, num_arrivals, num_departures)
    p.run_simulation()

main()