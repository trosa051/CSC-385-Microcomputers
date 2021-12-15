import random

class Building:
    def __init__(self, btype, coords, takenSpots):
        self.type = btype
        self.streetCoords = coords
        self.coords = coords
        if coords in takenSpots:
            try:
                if(coords[0],coords[1]+1) not in takenSpots:
                    self.coords = (coords[0],coords[1]+1)
                elif(coords[0],coords[1]-1) not in takenSpots:
                    self.coords = (coords[0],coords[1]-1)
                elif(coords[0]+1,coords[1]) not in takenSpots:
                    self.coords = (coords[0]+1,coords[1])
                elif(coords[0]-1,coords[1]) not in takenSpots:
                    self.coords = (coords[0]-1,coords[1])
                #Wouldnt be too happy about these but if it works it works
                elif(coords[0]-1,coords[1]-1) not in takenSpots:
                    self.coords = (coords[0]-1,coords[1]-1)
                elif(coords[0]-1,coords[1]+1) not in takenSpots:
                    self.coords = (coords[0]-1,coords[1]+1)
                elif(coords[0]+1,coords[1]+1) not in takenSpots:
                    self.coords = (coords[0]+1,coords[1]+1)
                elif(coords[0]+1,coords[1]-1) not in takenSpots:
                    self.coords = (coords[0]+1,coords[1]-1)
            except:
                print("unable to create "+btype)
                self.coords = (0,0)
        else:
            self.coords = coords
    def __str__(self):
        return str([self.type, self.coords])
    #def getCoords(self):
    #    return str(self.coords)

class Street:
    # def __init__(self,  name, *parentSt):
    #    self.name = name
    #    self.start = random.choice(parentSt.coords)

    def __init__(self, start, end, name, *parentSt):
        self.start = start
        self.end = end
        self.name = name
        self.vLen = abs(start[1] - end[1])
        self.hLen = abs(start[0] - end[0])
        self.dir = "horizontal" if abs(start[1] - end[1]) == 0.0 else "vertical"
        #     if self.dir == "horizontal":
        #         self.sign = "positive" if if start[0] - end[0] > 0.0 else "negative"
        #     elif self.dir == "vertical":
        #         self.sign = "positive" if if start[1] - end[1] > 0.0 else "negative"
        # #self.sign = "positive" if start[1] - end[1] > 0.0 else "vertical"
        
        self.coords = list()
        #creates a [list] of int coordinates horizontally
        if self.dir == "horizontal":
            var = min(start[0],end[0])
            const = start[1]
            revers = True if start[0]>end[0] == True else False
            #print(revers)
            for x in range(0,self.hLen):
                self.coords.append((var,const))
                if revers:
                    var = var - 1
                else:
                    var = var + 1
        #creates a [list] of int coordinates vertically
        if self.dir == "vertical":
            var = min(start[1],end[1])
            const = start[0]
            revers = True if start[1]>end[1] == True else False
            for x in range(0,self.vLen):
                self.coords.append((const,var))
                if revers:
                    var = var - 1
                else:
                    var = var + 1

        
    def __str__(self):
            return str([self.start,self.end,self.name])

    def rand_pos(self):
            return random.choice(self.coords)
