import re
from collections import deque
from queue import PriorityQueue
import copy
import sys



int_depth = -1
dest_loc = []
start_loc = []
i = 0
#closed_list = []

def_long =[[[0,0],[30,0],[60,0],[90,0],[120,0],[150,0],[180,180],[150,180],[120,180],[90,180],[60,180],[30,180]],[[0, 0], [30, 90], [60, 90], [90, 90], [120, 90], [150, 90], [180, 180],
[150, 270], [120, 270], [90, 270], [60, 270], [30, 270]]]                      #def_long[0] is longitude 0180  and  def_long[1] is longitude 90270

def_lat =[[90, 0], [90, 30], [90, 60], [90, 90], [90, 120], [90, 150], [90, 180], [90, 210],[90, 240], [90, 270], [90, 300], [90, 330]]
                                                                               #def_lat[0] is lattitude 


f = open(sys.argv[1], "r")                                                     #opened file                         
for line in f:
    y = re.search(".*?\\((.*?),\\s\\((.*?)\\),\\s.*?\\((.*?)\\)\\)", line)     #extracted data using regex
    if y:
        start_loc.append([int(yz) for yz in y.group(2).split(",")])     
        dest_loc.append([int(yz) for yz in y.group(3).split(",")])
        

def left (curr_loc):                                                           #rotate latitude clockwise 
    curr_loc = copy.deepcopy(curr_loc)
    temp_loc = copy.deepcopy(curr_loc)
    for index in range(0, 12):
        search_loc = def_lat[index]
        i = curr_loc.index(search_loc)
        new_loc = def_lat[(index + 1)%12]
        temp_loc[i] = new_loc
    return temp_loc

def right (curr_loc):                                                          #rotate latitude anticlockwise 
    curr_loc = copy.deepcopy(curr_loc)
    temp_loc = copy.deepcopy(curr_loc)
    for index in range(0, 12):
        search_loc = def_lat[index]
        i = curr_loc.index(search_loc)
        if index == 0 :
            indexx = 12
        else:
            indexx = index
        new_loc = def_lat[(indexx - 1)]
        temp_loc[i] = new_loc
    return temp_loc


def clockwise_0180 (curr_loc):                                                 #rotate longitude 0180 clockwise     
    curr_loc = copy.deepcopy(curr_loc)
    temp_loc = copy.deepcopy(curr_loc)
    for index in range(0, 12):
        search_loc = def_long[0][index]
        i = curr_loc.index(search_loc)
        if index == 0 :
            indexx = 12
        else:
            indexx = index
        new_loc = def_long[0][(indexx - 1)]
        temp_loc[i] = new_loc
    return temp_loc


def anticlockwise_0180 (curr_loc):                                             #rotate longitude 0180 anticlockwise 
    curr_loc = copy.deepcopy(curr_loc)
    temp_loc = copy.deepcopy(curr_loc)
    for index in range(0, 12):
        search_loc = def_long[0][index]
        i = curr_loc.index(search_loc)
        new_loc = def_long[0][(index + 1)%12]
        temp_loc[i] = new_loc
    return temp_loc


def anticlockwise_90270 (curr_loc):                                            #rotate longitude 90270 anticlockwise 
    curr_loc = copy.deepcopy(curr_loc)
    temp_loc = copy.deepcopy(curr_loc)
    for index in range(0, 12):
        search_loc = def_long[1][index]
        i = curr_loc.index(search_loc)
        new_loc = def_long[1][(index + 1)%12]
        temp_loc[i] = new_loc
    return temp_loc



def clockwise_90270 (curr_loc):                                                #rotate longitude 90270 clockwise 
    curr_loc = copy.deepcopy(curr_loc)
    temp_loc = copy.deepcopy(curr_loc)
    for index in range(0, 12):
        search_loc = def_long[1][index]
        i = curr_loc.index(search_loc)
        if index == 0 :
            indexx = 12
        else:
            indexx = index
        new_loc = def_long[1][(indexx - 1)]
        temp_loc[i] = new_loc
    return temp_loc
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def check_goal (curr_loc,dest_loc):                                            #check if current state is goal state     
    global int_depth
    int_depth = int_depth + 1
    for i in range(0, 30):
        for j in range(0, 2):
            if curr_loc[i][j] != dest_loc[i][j] :
                return False
    return True

def check_dup(curr_loc,closed_list):                                           #check if current state is already explored
    flag = 0
    for xx in closed_list:
        flag = 0
        for i in range(0,30):
            if curr_loc[i] != xx[i]:
                flag = 1
        if flag == 0:
            return True
    if flag == 1:
        return False

def check_dup1(curr_loc,open_list):                                            #check if current state is in queue already
    flag = 0
    if not open_list:
        for xx in open_list:
            flag = 0
            for i in range(0,30):
                if curr_loc[i] != xx[i]:
                    flag = 1
            if flag == 0:
                return True
        if flag == 1:
            return False

def heuristic (curr_loc):                                                      #calculate heuristic
    curr_loc = copy.deepcopy(curr_loc)
#   curr_loc = curr_loc_map[3]
    h_tot = 0
    for i in range(0, 30):
        for j in range(0, 2):
            h_tot = h_tot + abs(curr_loc[i][j] - dest_loc[i][j])
#   print("h ",h_tot)
    return h_tot/30






def calculations (curr_state, curr_loc_map):                                   #calculations for current state (f , g , h) 
    curr_loc_map = copy.deepcopy(curr_loc_map)
    curr_state = copy.deepcopy(curr_state)
    new_loc_map = [0,0,0,0,0]
    new_loc_map[1] = curr_loc_map[1] + 1
    new_loc_map[2] = heuristic(curr_state[3])
    new_loc_map[0] = new_loc_map[1] + new_loc_map[2]
    new_loc_map[3] = curr_state[3]
    new_loc_map[4] = curr_state[4]
    return new_loc_map




def calculations_rbfs (curr_state, curr_loc_map):                              #calculations for rbfs algorithm (F, f, g, h) 
    curr_loc_map = copy.deepcopy(curr_loc_map)
    curr_state = copy.deepcopy(curr_state)
    new_loc_map = [0,0,0,0,0,0]
    h = heuristic(curr_state[4])
    g = curr_loc_map[2] + 1
    f = g + h
    if (curr_loc_map[1] < curr_loc_map[0]):
        new_loc_map[0] = max(curr_loc_map[0], f)
    else:
        new_loc_map[0] = h
    
    new_loc_map[3] = h
    new_loc_map[2] = curr_loc_map[2] + 1
    new_loc_map[1] = f
    new_loc_map[4] = curr_state[4]
    new_loc_map[5] = curr_state[5]
    return new_loc_map




def exit_func(return_array):                                                   #to print output of RBFS algorithm 
    
    print("The number of states expanded : ", return_array[0])
    print("The final path length : ", return_array[1])
    print("The final Path: " + return_array[2] + "GOAL" )
    print("\n")

def rbfs (curr_loc_map, f_limit):                                              #RBFS algorithm 

    curr_loc_map = copy.deepcopy(curr_loc_map)
    global i
    if i == 0:
        curr_loc_map[5] = "START --> "
    i = 1

    if check_goal(curr_loc_map[4], dest_loc):
        return_array = [i, i, curr_loc_map[5]]
        exit_func(return_array)
        sys.exit(0)
    
    successors_list = PriorityQueue()

    curr_state = [0,0,0,0,0,0]
    curr_state[4] = clockwise_0180(curr_loc_map[4])
    curr_state = calculations_rbfs(curr_state, curr_loc_map)
    curr_state[5] = curr_loc_map[5] + "clockwise_0180 --> "
    successors_list.put(curr_state)

    curr_state = [0,0,0,0,0,0]
    curr_state[4] = anticlockwise_0180(curr_loc_map[4])
    curr_state = calculations_rbfs(curr_state, curr_loc_map)
    curr_state[5] = curr_loc_map[5] + "anticlockwise_0180 --> "
    successors_list.put(curr_state)

    curr_state = [0,0,0,0,0,0]
    curr_state[4] = clockwise_90270(curr_loc_map[4])
    curr_state = calculations_rbfs(curr_state, curr_loc_map)
    curr_state[5] = curr_loc_map[5] + "clockwise_90270 --> "
    successors_list.put(curr_state)

    curr_state = [0,0,0,0,0,0]
    curr_state[4] = anticlockwise_90270(curr_loc_map[4])
    curr_state = calculations_rbfs(curr_state, curr_loc_map)
    curr_state[5] = curr_loc_map[5] + "anticlockwise_90270 --> "
    successors_list.put(curr_state)

    curr_state = [0,0,0,0,0,0]
    curr_state[4] = left(curr_loc_map[4])
    curr_state = calculations_rbfs(curr_state, curr_loc_map)
    curr_state[5] = curr_loc_map[5] + "clockwise_latitude --> "
    successors_list.put(curr_state)

    curr_state = [0,0,0,0,0,0]
    curr_state[4] = right(curr_loc_map[4])
    curr_state = calculations_rbfs(curr_state, curr_loc_map)
    curr_state[5] = curr_loc_map[5] + "anticlockwise_latitude --> "
    successors_list.put(curr_state)
    

    if successors_list.empty():
        return_array = [0,9999999]
        print(return_array)
        sys.exit(0)

    best_state = successors_list.get()
    alt_best_state = successors_list.get()
    successors_list.put(best_state)
    successors_list.put(alt_best_state)


    while best_state[0] <= f_limit and best_state[0] < 99999999:

        best_state[0] = rbfs (best_state, min(f_limit, alt_best_state[0]))
        successors_list.get()
        successors_list.put(best_state)
        best_state = successors_list.get()
        alt_best_state = successors_list.get()
        
    return best_state[0]










#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def astar (curr_loc, dest_loc):
    
    #Node structure = [f, cost(g), heuristic(h), current_state, path]
    #closed_list is list of explored nodes
    #open_list is queue getting sorted using f values of the nodes present in the queue
    
    closed_list = []
    open_list = PriorityQueue()
    curr_loc = copy.deepcopy(curr_loc)
    open_list_length = 0
    x = [0,0,0, curr_loc,"START --> "]                                          
    if check_goal(x[3],dest_loc):
        return [0,0,0, "START"]

    
    open_list.put(x)
    while True:
        if open_list.empty() :
            return [0,0,0, "CAN'T FIND SOLUTION"]
        
        curr_loc_map = open_list.get()
        closed_list.append(curr_loc_map[3])

        
      #GENERATING CHILDS AND CHECKING IF GOAL STATE
      #IF NOT GOAL STATE ADD THEM TO QUEUE after updating cost and their heuristic value
      
        curr_state = [0,0,0,0,0]
        curr_state = copy.deepcopy(curr_state)
        curr_state[3] = clockwise_0180(curr_loc_map[3])
        path = curr_loc_map[4] + "clockwise_0180 --> "
        curr_state[4] = path
        
        if check_dup(curr_state[3],closed_list) or check_dup1(curr_state[3],open_list):
             s = 0

        elif check_goal(curr_state[3],dest_loc) :
            curr_state = calculations(curr_state,curr_loc_map)
            return_array = [len(closed_list), open_list_length, curr_state[1], curr_state[4]]
            return return_array
        else :    
            curr_state = calculations(curr_state,curr_loc_map)
            open_list.put(curr_state)
            open_list_length = max (open_list_length, open_list.qsize())
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0,0,0]
        curr_state = copy.deepcopy(curr_state)
        curr_state[3] = anticlockwise_90270(curr_loc_map[3])
        path = curr_loc_map[4] + "anticlockwise_90270 --> "
        curr_state[4] = path
        
        if check_dup(curr_state[3],closed_list) or check_dup1(curr_state[3],open_list):
             s = 0

        elif check_goal(curr_state[3],dest_loc) :
            curr_state = calculations(curr_state,curr_loc_map)
            return_array = [len(closed_list), open_list_length, curr_state[1], curr_state[4]]
            return return_array
        else :    
            curr_state = calculations(curr_state,curr_loc_map)
            open_list.put(curr_state)
            open_list_length = max (open_list_length, open_list.qsize())
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
        curr_state = [0,0,0,0,0]
        curr_state = copy.deepcopy(curr_state)
        curr_state[3] = clockwise_90270(curr_loc_map[3])
        path = curr_loc_map[4] + "clockwise_90270 --> "
        curr_state[4] = path
        
        if check_dup(curr_state[3],closed_list) or check_dup1(curr_state[3],open_list):
             s = 0

        elif check_goal(curr_state[3],dest_loc) :
            curr_state = calculations(curr_state,curr_loc_map)
            return_array = [len(closed_list), open_list_length, curr_state[1], curr_state[4]]
            return return_array
        else :    
            curr_state = calculations(curr_state,curr_loc_map)
            open_list.put(curr_state)
            open_list_length = max (open_list_length, open_list.qsize())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0,0,0]
        curr_state = copy.deepcopy(curr_state)
        curr_state[3] = anticlockwise_0180(curr_loc_map[3])
        path = curr_loc_map[4] + "anticlockwise_0180 --> "
        curr_state[4] = path
        
        if check_dup(curr_state[3],closed_list) or check_dup1(curr_state[3],open_list):
             s = 0

        elif check_goal(curr_state[3],dest_loc) :
            curr_state = calculations(curr_state,curr_loc_map)
            return_array = [len(closed_list), open_list_length, curr_state[1], curr_state[4]]
            return return_array
        else :    
            curr_state = calculations(curr_state,curr_loc_map)
            open_list.put(curr_state)
            open_list_length = max (open_list_length, open_list.qsize())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0,0,0]
        curr_state = copy.deepcopy(curr_state)
        curr_state[3] = left(curr_loc_map[3])
        path = curr_loc_map[4] + "clockwise_latitude --> "
        curr_state[4] = path
        
        if check_dup(curr_state[3],closed_list) or check_dup1(curr_state[3],open_list):
             s = 0

        elif check_goal(curr_state[3],dest_loc) :
            curr_state = calculations(curr_state,curr_loc_map)
            return_array = [len(closed_list), open_list_length, curr_state[1], curr_state[4]]
            return return_array
        else :    
            curr_state = calculations(curr_state,curr_loc_map)
            open_list.put(curr_state)
            open_list_length = max (open_list_length, open_list.qsize())
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0,0,0]
        curr_state = copy.deepcopy(curr_state)
        curr_state[3] = right(curr_loc_map[3])
        path = curr_loc_map[4] + "anticlockwise_latitude --> "
        curr_state[4] = path
        
        if check_dup(curr_state[3],closed_list) or check_dup1(curr_state[3],open_list):
             s = 0

        elif check_goal(curr_state[3],dest_loc) :
            curr_state = calculations(curr_state,curr_loc_map)
            return_array = [len(closed_list), open_list_length, curr_state[1], curr_state[4]]
            return return_array
        else :    
            curr_state = calculations(curr_state,curr_loc_map)
            open_list.put(curr_state)
            open_list_length = max (open_list_length, open_list.qsize())
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def bfs (curr_loc, dest_loc):
    
    #Node structure = [cost, current_state, path]
    #closed_list is list of explored nodes
    #open_list is queue of elements to be explored    
    
    closed_list = []
    open_list = deque()
    curr_loc = copy.deepcopy(curr_loc)
    open_list_length = 0
    x = [0, curr_loc,"START --> "]
    if check_goal(x[1],dest_loc):
        return [0,0,0, "START"]

    
    open_list.append(x)
    
    while True:
        if not open_list :
            return [0,0,0, "CAN'T FIND SOLUTION"]
        
        curr_loc_map = open_list.popleft()
        closed_list.append(curr_loc_map[1])
        
        
        
        curr_state = [0,0,0]
        curr_state[1] = clockwise_0180(curr_loc_map[1])
        curr_state[0] = curr_loc_map[0] + 1
        path = curr_loc_map[2] + "clockwise_0180 --> "
        curr_state[2] = path
        
        if check_dup(curr_state[1],closed_list) or check_dup1(curr_state[1],open_list):
             s = 0
        elif check_goal(curr_state[1],dest_loc) :
            return_array = [len(closed_list), open_list_length, curr_state[0], curr_state[2]]
            return return_array
        else :    
            open_list.append(curr_state)
            open_list_length = max (open_list_length, len(open_list))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0]
        curr_state[1] = anticlockwise_90270(curr_loc_map[1])
        curr_state[0] = curr_loc_map[0] + 1
        path = curr_loc_map[2] + "anticlockwise_90270 --> "
        curr_state[2] = path 
       
        if check_dup(curr_state[1],closed_list) or check_dup1(curr_state[1],open_list):
             s = 0
        elif check_goal(curr_state[1],dest_loc) :
            return_array = [len(closed_list), open_list_length, curr_state[0], curr_state[2]]
            return return_array
        else :    
            open_list.append(curr_state)
            open_list_length = max (open_list_length, len(open_list))
 #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
        curr_state = [0,0,0]
        curr_state[1] = clockwise_90270(curr_loc_map[1])
        curr_state[0] = curr_loc_map[0] + 1
        path = curr_loc_map[2] + "clockwise_90270 --> "
        curr_state[2] = path
        
        if check_dup(curr_state[1],closed_list) or check_dup1(curr_state[1],open_list):
             s = 0
        elif check_goal(curr_state[1],dest_loc) :
            return_array = [len(closed_list), open_list_length, curr_state[0], curr_state[2]]
            return return_array
        else :    
            open_list.append(curr_state)
            open_list_length = max (open_list_length, len(open_list))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0]
        curr_state[1] = anticlockwise_0180(curr_loc_map[1])
        curr_state[0] = curr_loc_map[0] + 1
        path = curr_loc_map[2] + "anticlockwise_0180 --> "
        curr_state[2] = path
        
        if check_dup(curr_state[1],closed_list) or check_dup1(curr_state[1],open_list):
             s = 0
        elif check_goal(curr_state[1],dest_loc) :
            return_array = [len(closed_list), open_list_length, curr_state[0], curr_state[2]]
            return return_array
        else :    
            open_list.append(curr_state)
            open_list_length = max (open_list_length, len(open_list))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0]
        curr_state[1] = left(curr_loc_map[1])
        curr_state[0] = curr_loc_map[0] + 1
        path = curr_loc_map[2] + "clockwise_latitude --> "
        curr_state[2] = path
        
        if check_dup(curr_state[1],closed_list) or check_dup1(curr_state[1],open_list):
             s = 0
        elif check_goal(curr_state[1],dest_loc) :
            return_array = [len(closed_list), open_list_length, curr_state[0], curr_state[2]]
            return return_array
        else :    
            open_list.append(curr_state)
            open_list_length = max (open_list_length, len(open_list))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        curr_state = [0,0,0]
        curr_state[1] = right(curr_loc_map[1])
        curr_state[0] = curr_loc_map[0] + 1
        path = curr_loc_map[2] + "anticlockwise_latitude --> "
        curr_state[2] = path
        
        if check_dup(curr_state[1],closed_list) or check_dup1(curr_state[1],open_list):
            s = 0
        elif check_goal(curr_state[1],dest_loc) :
            return_array = [len(closed_list), open_list_length, curr_state[0], curr_state[2]]
            return return_array
        else :    
            open_list.append(curr_state)
            open_list_length = max (open_list_length, len(open_list))
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



if sys.argv[2] == "BFS":

    bfs_returned_values = bfs (start_loc, dest_loc)
    print("The number of states expanded : ", bfs_returned_values[0])
    print("The maximum size of the queue during search : ", bfs_returned_values[1])
    print("The final path length : ", bfs_returned_values[2])
    print("The final Path: " + bfs_returned_values[3] + "GOAL" )
    print("\n")


elif sys.argv[2] == "AStar":

    astar_returned_values = astar (start_loc, dest_loc)
    print("The number of states expanded : ", astar_returned_values[0])
    print("The maximum size of the queue during search : ", astar_returned_values[1])
    print("The final path length : ", astar_returned_values[2])
    print("The final Path: " + astar_returned_values[3] + "GOAL" )
    print("\n")

elif sys.argv[2] == "RBFS":

    h = heuristic(start_loc)
    start_loc = [0,h,0,h,start_loc,0]
    a = rbfs (start_loc, 99999999)

else:
    print("WRONG CALL")
