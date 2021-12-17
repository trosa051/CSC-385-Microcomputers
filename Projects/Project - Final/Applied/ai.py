# CSC 447 Artificial Intelligence 
# Final Project for CSC 447
#
# Omitted as part of submission for CSC 480

import sys
from collections import deque #PROCESSING SAFE

def read_file(filename):
    streetCoords = []
    postOffice = (-1,-1)
    streetInfo = []
    buildings = []
    goals = []
    goalSpots = []

    with open(filename) as f:
        for line in f:

            if "Street coordinates" in line:
                for j in line[21:-3].split("), ("):
                    x,y = j.split(", ")
                    if x[0] == '(':
                        x = x[1:]
                    streetCoords.append((int(x),int(y)))
                
            elif "My post office is located at " in line:
                postOffice = (int(line[30:-1].split(", ")[0]),int(line[30:-2].split(", ")[1]))
                
            elif "[(" in line[:2]:
                for k in line[2:].split(", ("):  
                    if len(k[:-1].split(", ")) ==2:
                        startPos= (int(k[:-1].split(", ")[0]),int(k[:-1].split(", ")[1]))
                    else:
                        endPos = (int(k[:-1].split()[0][:-1]),int(k[:-1].split()[1][:-2]))
                        streetName = (k[2:-3].split(", ")[2][1:])
                streetInfo.append([startPos,endPos,streetName])

            elif "These are my buildings "in line:
                for l in line[25:-3].split("), ("):
                    x,y = l.split(", ")
                    buildings.append((int(x),int(y)))
                
            elif "These are my goals " in line:
                for l in line[21:-2].split("), ("):
                    x,y = l.split(", ")
                    goals.append((int(x),int(y)))

                    #need to stick to the same algo as what I used in the processing sketch
                    if(int(x),int(y)+1) in streetCoords:
                        goalSpots.append((int(x),int(y)+1))
                    elif(int(x),int(y)-1) in streetCoords:
                        goalSpots.append((int(x),int(y)-1))
                    elif(int(x)+1,int(y)) in streetCoords:
                        goalSpots.append((int(x)+1,int(y)))
                    elif(int(x)-1,int(y)) in streetCoords:
                        goalSpots.append((int(x)-1,int(y)))
                    elif(int(x)-1,int(y)-1) in streetCoords:
                        goalSpots.append((int(x)-1,int(y)-1))
                    elif(int(x)-1,int(y)+1) in streetCoords:
                        goalSpots.append((int(x)-1,int(y)+1))
                    elif(int(x)+1,int(y)+1) in streetCoords:
                        goalSpots.append((int(x)+1,int(y)+1))
                    elif(int(x)+1,int(y)-1) in streetCoords:
                        goalSpots.append((int(x)+1,int(y)-1))
                    #######################################################################


        return streetCoords,postOffice,streetInfo,buildings,goals,goalSpots

class grid:
    def __init__(self, w, h, streets):
        self.w = w
        self.h = h
        self.streets = streets #keep in mind this is a list
        self.walls = []

        for x in range(w):
            for y in range(h):
                if (x,y) not in streets:
                  self.walls.append((x,y))

    def adjacent(self,position):
        #print("function adjacent recieved:" + str(position))
        x = position[0]
        y = position[1]
        results = []
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        for i in neighbors:
            if i in self.streets:
                if i[0] > self.w or i[1] > self.h or i[0] < 0 or i[1] < 0:
                    pass
                else:
                    results.append((i))
        return results        
#############################################################################
def make_node(state, parent): #, action):
    result = {}
    result ["state"] = state
    result ["parent"] = parent
    if parent:
        result["depth"] = parent["depth"]+1
    else:
        result["depth"] = 0
    #if action:
    #    result["action"] = action
    #else:
    #    result["action"] = None
    return result

def successors(state, grid):
    result = grid.adjacent(state)
    return result

def search(start, goal, grid):
    maxSize = 0
    currentSize = 0
    frontier = deque()
    frontier.append(make_node(start, None))

    reached = set()
    #reached.add(tuple(map(str,start))) #This little maneuver is going to cost us 51 years
    reached.add(start)

    while frontier:

        if maxSize < len(frontier):
            maxSize = len(frontier)

        node = frontier.popleft()
        if node["state"] == goal:
            return node# , frontier , maxSize, currentSize
        for state in successors(node["state"],grid): #for action, state
            if maxSize < len(frontier):
                maxSize = len(frontier)
            currentSize+=1
            child = make_node(state, node)#, action)
            #st = tuple(map(str,child["state"]))
            st = child["state"]
            if st not in reached:
                reached.add(st)
                frontier.append(child)
    #return node

#############################################################################

def reconstruct_path(came_from,start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path


def make_path(start, goal, grid):
    n  = search(start, goal, grid)
    path = []
    if n != None:
        while n['parent'] != None:
            path.append(n['state'])
            n = n['parent']
    path.reverse()
    return path

# def make_directions(start, goal, grid):
#     n, q, maxQ, expanCount  = search(start, goal, grid)
#     path = []
#     while n['parent'] != None:
#         path.append(n['state'])
#         n = n['parent']
#     path.reverse()
#     path



# if __name__ == "__main__":

#     if len(sys.argv) != 2:
#         print("Usage: <graph file>")
#         sys.exit()

#     streetCoords, postOffice, streetInfo, buildings, goals, goalSpots = read_file(sys.argv[1])
#     layout = grid(50,50,streetCoords)

#     start= (postOffice[0],postOffice[1]-1)
#     for j in goalSpots:
#         #if i != j:
#             print("from "+str(start)+" to "+str(j)+": "+str(make_path(start,j,layout)))

#     for i in goalSpots:
#         for j in goalSpots:
#             if i != j:
#                 print("from "+str(i)+" to "+str(j)+": "+str(make_path(i,j,layout)))
#         #print("from "+str(i)+" to "+start+": "+str(len(make_path(i,start,layout))))

#     #draw_grid(layout,start=start,house=buildings,goal=goalSpots,PO=postOffice,path=make_path(goalSpots[4],goalSpots[2],layout))
    
