import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
#The code generates a timetable a for bus route & calculates journey paths & travel times for a set of passengers

#example route with set of grid coordinates (bus stops have letters)
route = [ ( 2, 1, 'A'), ( 3, 1, ''), ( 4, 1, ''), ( 5, 1, ''),
          ( 6, 1, ''), ( 7, 1, 'B'), ( 7, 2, ''), ( 8, 2, ''),
          ( 9, 2, ''), (10, 2, ''), (11, 2, 'C'), (11, 1, ''),
          (12, 1, ''), (13, 1, ''), (14, 1, ''), (14, 2, 'D'),
          (14, 3, ''), (14, 4, ''), (13, 4, ''), (12, 4, ''),
          (11, 4, ''), (10, 4, ''), ( 9, 4, ''), ( 9, 5, 'E'),
          ( 9, 6, ''), (10, 6, ''), (11, 6, 'F'), (12, 6, ''),
          (13, 6, ''), (14, 6, ''), (15, 6, ''), (16, 6, 'G') ]

#--------

#passengers with their start & end position (with walking pace in x mins per grid unit)
passengers = { 1: [(0,2), (8,1), 15],
               2: [(0,0), (6,2), 12],
               3: [(5,2), (15,4), 16],
               4: [(4,5), (9,7), 20],
             }

#--------

#fxn 1: calculates timetable for bus when guven route
def timetable(route):
    '''
    Generates a timetable for a route as minutes from its first stop.
    '''
    time = 0
    stops = {}
    for step in route:
        if step[2]:
            stops[step[2]] = time
        time += 10
    return stops

#--------

#fxn 2: calculates passenger's walking distance to nearest start & end bus stops (remember: passengers can walk outside grid)
#NB: think what happens when 2 stops are the same distance away // or when order of closest stops does not match direction of travel
def passenger_trip(passenger, route):
    start, end, pace = passenger
    stops = [value for value in route if value[2]]
    # calculate closer stops
    ## to start
    distances = [(math.sqrt((x - start[0])**2 +
                            (y - start[1])**2), stop) for x,y,stop in stops]
    closer_start = min(distances)
    ## to end
    distances = [(math.sqrt((x - end[0])**2 +
                            (y - end[1])**2), stop) for x,y,stop in stops]
    closer_end = min(distances)
    return (closer_start, closer_end)

#--------

#fxn 3: calculates total travel time for a particular passenger
#think how to represent this separately in time on foot + time on bus
def passenger_trip_time(passenger, route):
    walk_distance_stops = passenger_trip(passenger, route)
    bus_times = timetable(route)
    bus_travel = bus_times[walk_distance_stops[1][1]] - \
                 bus_times[walk_distance_stops[0][1]]
    walk_travel = walk_distance_stops[0][0] * passenger[2] + \
                  walk_distance_stops[1][0] * passenger[2]
    return bus_travel + walk_travel

#--------

#fxn 4a: visualisation (displays a route & the stops on a grid)
def plot_map(route):
    max_x = max([n[0] for n in route]) + 5 # adds padding
    max_y = max([n[1] for n in route]) + 5
    grid = np.zeros((max_y, max_x))
    for x,y,stop in route:
        grid[y, x] = 1
        if stop:
            grid[y, x] += 1
    fig, ax = plt.subplots(1, 1)
    ax.pcolor(grid)
    ax.invert_yaxis()
    ax.set_aspect('equal', 'datalim')
    plt.show()

#--------

#fxn 4b: visualisation (displays how many people on the bus b/w stops)
def plot_bus_load(route, passengers):
    stops = {step[2]:0 for step in route if step[2]}
    for passenger in passengers.values():
        trip = passenger_trip(passenger, route)
        stops[trip[0][1]] += 1
        stops[trip[1][1]] -= 1
    for i, stop in enumerate(stops):
        if i > 0:
            stops[stop] += stops[prev]
        prev = stop
    fig, ax = plt.subplots()
    ax.step(range(len(stops)), list(stops.values()), where='post')
    ax.set_xticks(range(len(stops)))
    ax.set_xticklabels(list(stops.keys()))
    plt.show()

#--------

#generating output
print(" Stops: minutes from start\n", timetable(route))
for passenger_id, passenger in passengers.items():
    print(f"Trip for passenger: {passenger_id}")
    start, end = passenger_trip(passenger, route)
    total_time = passenger_trip_time(passenger, route)
    print((f" Walk {start[0]:3.2f} units to stop {start[1]}, \n"
           f" get on the bus and alite at stop {end[1]} and \n"
           f" walk {end[0]:3.2f} units to your destination."))
    print(f" Total time of travel: {total_time:03.2f} minutes")
# Plots the route of the bus
plot_map(route)
# Plots the number of passenger on the bus
plot_bus_load(route, passengers)

#--------

#checking bus route using chain code (as bus can only move horizontally & vertically, not diagonally)
#to check that a route satisfies this, the route is converted to chain code & checked for the odd numbers (which there shouldn't be?)
def route_cc(route):
    '''
    Converts a set of route into a Freeman chain code
    3 2 1
    \ | /
    4 - C - 0
    / | \
    5 6 7
    '''
    start = route[0][:2]
    cc = []
    freeman_cc2coord = {0: (1, 0),
                        1: (1, -1),
                        2: (0, -1),
                        3: (-1, -1),
                        4: (-1, 0),
                        5: (-1, 1),
                        6: (0, 1),
                        7: (1, 1)}
    freeman_coord2cc = {val: key for key,val in freeman_cc2coord.items()}
    for b, a in zip(route[1:], route):
        x_step = b[0] - a[0]
        y_step = b[1] - a[1]
        cc.append(str(freeman_coord2cc[(x_step, y_step)]))
    return start, ''.join(cc)

#how to use
start_point, cc = route_cc(route)
print((f"The bus route starts at {start_point} and\n"
       f"it's described by this chain code:\n{cc}"))
