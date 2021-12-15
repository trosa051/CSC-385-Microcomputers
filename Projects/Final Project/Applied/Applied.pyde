'''
STUDENT NAME: TJ Rosario-Rosa
CSC480 Fall 2021 Final Project

RAPID PROTOTYPING SAMPLE


INTERACTION:
keyPressed():
    mousePressed:
        Drag the screen around
    mouseWheel:
        Zoom into the simulation to get a better look at things
    '0' or '1':
        change cameras. 0 *should* be top down orthogonal and 1 is a 3rd person camera
    'Up', 'Down', 'Left', "Right':
        Move the mailman
    'R':
        Experimental!! Resets movement back to original points. Breaks 3rd person camera temporarily 
'''


add_library('ocd')
import timeit, random
from lib import Street
from lib import Building
from ai import search
from ai import make_path
from ai import grid
import gc

def setup():

    size(1920, 1080, P3D)
    background(0)
    noSmooth()
    gc.enable()
    pixelDensity(2)
    
    global grid, tImg, sphereShape, framesElapsed, cam, pov, state, feed, speed, mail_amt, tic, taken, populated, buildings, goals, sts, postOffice, spawnPos, bil, gls, poof, mov
    visualizeGrid = True
    imgSize = 40
    gridxy = 20
    speed = 10
    mail_amt = 5
    tic=timeit.default_timer()
    taken = []
    populated = []
    buildings = []
    goals = []
    sts = []
    bil = []
    gls = []
    mov = [-20,0,0]
    nCols = 50
    nRows = 50  
    gridSize = 50
    grid = []
    density = 12;
    names =["Church Street","Elm Street","High Street","Washington Street","Park Avenue","2nd Street","Walnut Street","Chestnut Street","Maple Avenue","Maple Street","Broad Street","Oak Street","Center Street","Pine Street","River Road","Market Street","Water Street","Union Street","South Street","Park Street","3rd Street","Washington Avenue","Cherry Street","North Street","4th Street","Court Street","Highland Avenue","Mill Street","Franklin Street","Prospect Street","School Street","Spring Street","Central Avenue","1st Street","State Street","Front Street","West Street","Jefferson Street","Cedar Street","Jackson Street","Park Place","Bridge Street","Locust Street","Madison Avenue","Meadow Lane","Spruce Street","Grove Street","Ridge Road","5th Street","Pearl Street","Lincoln Street","Madison Street","Dogwood Drive","Lincoln Avenue","Pennsylvania Avenue","Pleasant Street","4th Street West","Adams Street","Jefferson Avenue","3rd Street West","7th Street","Academy Street","11th Street","2nd Avenue","East Street","Green Street","Hickory Lane","Route 1 Street","Summit Avenue","Virginia Avenue","12th Street","5th Avenue","6th Street","9th Street","Charles Street","Cherry Lane","Elizabeth Street","Hill Street","River Street","10th Street","Colonial Drive","Monroe Street","Valley Road","Winding Way","1st Avenue","Fairway Drive","Liberty Street","2nd Street West","3rd Avenue","Broadway","Church Road","Delaware Avenue","Prospect Avenue","Route 30 Street","Sunset Drive","Vine Street","Woodland Drive","6th Street West","Brookside Drive","Hillside Avenue","Lake Street","13th Street","4th Avenue","5th Street North","College Street","Dogwood Lane","Mill Road","7th Avenue","8th Street","Beech Street","Division Street","Harrison Street","Heather Lane","Lakeview Drive","Laurel Lane","New Street","Oak Lane","Primrose Lane","Railroad Street","Willow Street","4th Street North","5th Street West","6th Avenue","Berkshire Drive","Buckingham Drive","Circle Drive","Clinton Street","George Street","Hillcrest Drive","Hillside Drive","Laurel Street","Park Drive","Penn Street","Railroad Avenue","Riverside Drive","Route 32 Street","Route 6 Street","Sherwood Drive","Summit Street","2nd Street East","6th Street North","Cedar Lane","Creek Road","Durham Road","Elm Avenue","Fairview Avenue","Front Street North","Grant Street","Hamilton Street","Highland Drive","Holly Drive","King Street","Lafayette Avenue","Linden Street","Mulberry Street","Poplar Street","Ridge Avenue","7th Street East","Belmont Avenue","Cambridge Court","Cambridge Drive","Clark Street","College Avenue","Essex Court","Franklin Avenue","Hilltop Road","James Street","Magnolia Drive","Myrtle Avenue","Route 10 Street","Route 29 Street","Shady Lane","Surrey Lane","Walnut Avenue","Warren Street","Williams Street","Wood Street","Woodland Avenue"];
    tImg = [requestImage("0.png"),requestImage("1.png"),requestImage("1a.png"),requestImage("2b.png"),requestImage("2a.png"),requestImage("2.png"),requestImage("2c.png"),requestImage("3a.png"),requestImage("3c.png"),requestImage("3.png"),requestImage("3b.png"),requestImage("4.png")]
    feed = 0
    framesElapsed = 0
    
    #OCD Camera
    pov = Camera(this, 500.0, -1000.0, 500)
    pov.arc(radians(-5))
    pov.zoom(radians(-110) / 2.0)
    pov.jump(600,-40,600)
    pov.arc(radians(-5))
    
    #OCD Camera
    cam = Camera(this, 500.0, -1000.0, 500)
    cam.aim((20*25), 0, (20*25))
    cam.tilt(0)
    cam.roll(PI/2)
    cam.jump((20*25), -1000, (20*25))

    perspective((PI/3.0), float(width) / float(height), (height / 2.0) / tan(PI / 3.0 / 2.0) / 10000, (height / 2.0) / tan(PI / 3.0 / 2.0) * 1000.0)
    #ortho()
    if visualizeGrid:
        stroke(0)
    else:
        noStroke()
    for i in range(0,gridSize):
        grid.append([])
        for j in range(0,gridSize):
            temp = createShape()
            temp.beginShape()
            temp.vertex(     0, 0,      0,       0, 0)
            temp.vertex(gridxy, 0,      0, imgSize, 0)
            temp.vertex(gridxy, 0, gridxy, imgSize, imgSize)
            temp.vertex(     0, 0, gridxy,       0, imgSize)
            temp.endShape()
            grid[i].append([])
            grid[i][j]=temp
    
    
    #global b
    #b = createShape(BOX,5)
    
    skyboxTexture = loadImage("sky.jpg")

    noStroke()
    sphereShape = createShape(SPHERE,10001)
    sphereShape.setTexture(skyboxTexture)
    sphereShape.rotateY(-PI/2);
   
    stroke(0)
    poof = createShape(BOX,5)
    poof.stroke(0)

    #names lifted from https://www.livingplaces.com/streets/most-popular_street_names.html
    mainSt = Street((0,int(nCols/2)),(nRows,int(nCols/2)),"Main Street")
    sts.append(mainSt)
    for elm in mainSt.coords:
        populated.append(elm)
    spawnPos = mainSt.rand_pos()
    post_office = Building("PostOffice", spawnPos, populated)
    postOffice = post_office.coords
    print("My post office is located at")
    print(postOffice)   
    
      
    print(mainSt)
    for i in xrange(6):   
        try:
            place_1=mainSt.rand_pos()
            #print(place_1)
            place_2=(place_1[0],random.randint(0,nCols-2))
            #print(place_2)
            while place_1 == place_2:
                print("fixing dupe")
                place_2 =(random.choice(range(10,nCols-2,5)),place_1[1])
            pos = [place_1,place_2]
            random.shuffle(pos)
            #print(pos)
            offshoot_1 = Street(pos[0],pos[1],names.pop(random.randrange(len(names))),mainSt)
            sts.append(offshoot_1)
        except:
            print("Failed to make road1")
        #print(offshoot_1)
        if postOffice not in offshoot_1.coords:
            for elm in offshoot_1.coords:
            #if elm != postOffice:
                populated.append(elm)  
        try:    
            place_1=offshoot_1.rand_pos()
            #random.randint(6,nCols-2)
            place_2=(random.choice(range(10,nCols-2,5)),place_1[1])
            if place_1 == place_2:
                place_2 =(random.choice(range(10,nCols-2,5)),place_1[1])
            pos = [place_1,place_2]
        except:
            print("How did you even fail this")
            
        random.shuffle(pos)
        print(pos)
        try:
            offshoot_2 = Street(pos[0],pos[1],names.pop(random.randrange(len(names))),offshoot_1)
            sts.append(offshoot_2)
        except:
            print("Failed to make road2")
        print(offshoot_2)
        if postOffice not in offshoot_2.coords:
            for elm in offshoot_2.coords:
                if elm != postOffice:
                    populated.append(elm)   
    
    for i in xrange(density): 
        try:
            houmse = Building("House", random.choice(populated), populated+buildings)
        except:
            pass
        buildings.append(houmse)
        bil.append(houmse.coords)
    print("These are my buildings")
    print(bil)
    for i in buildings:
        taken.append(i)
    for i in populated:
        taken.append(i)
    for i in xrange(mail_amt): 
        goals.append(buildings.pop(random.randrange(len(buildings))))
    for i in goals:
        gls.append(i.coords)
    print("These are my goals")
    print(gls)
    
    print("Street coordinates:") 
    print(populated)
    
    
    noStroke()
    shape(sphereShape)
    translate(0,0,0)
    for i in xrange(50):
        for j in xrange(50):
            #translate((i*20),0,(j*20))
            if (i,j) in populated:#these are roads
                #neighbors = [(i-1,j),(i,j-1),(i+1,j),(i,j+1)]
                if (i-1,j) in populated and (i,j-1) in populated and (i+1,j) in populated and (i,j+1) in populated:   # ╋
                    grid[i][j].setTexture(tImg[11])
                elif (i-1,j) in populated and (i+1,j) in populated and (i,j-1) in populated:                          # ┳
                    grid[i][j].setTexture(tImg[10])
                elif (i,j+1) in populated and (i,j-1) in populated and (i+1,j) in populated:                          # ┣
                    grid[i][j].setTexture(tImg[9])
                elif (i,j+1) in populated and (i,j-1) in populated and (i-1,j) in populated:                          # ┫
                    grid[i][j].setTexture(tImg[8])
                elif (i,j+1) in populated and (i-1,j) in populated and (i+1,j) in populated:                          # ┻
                    grid[i][j].setTexture(tImg[7])
                elif (i-1,j) in populated and (i,j-1) in populated:                                                   # ┓
                    grid[i][j].setTexture(tImg[6])
                elif (i+1,j) in populated and (i,j-1) in populated:                                                   # ┏
                    grid[i][j].setTexture(tImg[5])
                elif (i+1,j) in populated and (i,j+1) in populated:                                                   # ┗
                    grid[i][j].setTexture(tImg[4])
                elif (i-1,j) in populated and (i,j+1) in populated:                                                   # ┛
                    grid[i][j].setTexture(tImg[3])
                elif [(i-1,j),(i+1,j)] in populated or (i+1,j) in populated or (i-1,j) in populated:                  # ━
                    grid[i][j].setTexture(tImg[1])
                elif [(i,j-1),(i,j+1)] in populated or (i,j-1) in populated or (i,j+1) in populated:                  # ┃
                    grid[i][j].setTexture(tImg[2])
                else:
                    grid[i][j].setTexture(tImg[11])
            elif (i,j) == postOffice:
                #grid[i][j].setTexture(tuple((198,89,17)))
                grid[i][j].setTexture(tImg[0])
            elif (i,j) in buildings:
                #grid[i][j].setTexture(tuple((128,128,128)))
                grid[i][j].setTexture(tImg[0])
            elif (i,j) in goals:
                #grid[i][j].setTexture(tuple((255,255,0)))
                grid[i][j].setTexture(tImg[0])
            else:
                grid[i][j].setTexture(tImg[0]) # This sets every block to grass
            translate(20,0,0) #good
        translate(-50*20,0,20)

    pov.aim(postOffice[1]*20+10-20,-2.5,postOffice[0]*20+10)


    #aiGrid = grid(50, 50)
    #grass = grid(50,50).diff(populated)
    
    
def draw():

    global feed, pov, poof, mov, framesElapsed
    framesElapsed = framesElapsed+1
    
      
    if feed == 0:
        cam.feed()
    if feed == 1:
        pov.feed()

    toc=timeit.default_timer()
    elapsed=toc - tic
    shape(sphereShape)
    translate(0,0,0)
    for i in xrange(50):
        for j in xrange(50):
            if (i,j) == postOffice:
                push()
                stroke(0)
                translate(10,-10,10)
                fill(198,89,17)
                box(20)
                pop()
            elif (i,j) in gls:
                push()
                stroke(0)
                translate(10,-10,10)
                fill(255,255,0)
                box(20)
                pop()
            elif (i,j) in bil:
                push()
                stroke(0)
                translate(10,-10,10)
                fill(128)
                box(20)
                pop()


            shape(grid[i][j])
            translate(20,0,0) #good
        translate(-50*20,0,20)
    #print(spawnPos)
    
    #=translate(0,0,0)
    for i in goals:
        translate(0,0,0)
        #print(goals)
        with push():
            translate(0,0,0)
            translate(10,-2.5,10)
            translate(i.coords[1]*20,0,i.coords[0]*20-50*20)
            
            
            coordDiff = [i.coords[b] - i.streetCoords[b] for b in range(2)]
            if coordDiff == [0,-1] or coordDiff == [-1,-1]:
                #print("goal placed on house at "+str((i.coords[1],i.coords[0]))+"| up")
                translate(20,0,0)
                stroke(255,255,0) #yellow
                noFill()
                box(5)
                #break
            elif coordDiff == [0,1] or coordDiff == [1,1]:
                #print("goal placed on house at "+str((i.coords[1],i.coords[0]))+"|down")
                translate(-20,0,0)
                stroke(255,255,0) #yellow
                noFill()
                box(5)
                #break
            elif coordDiff == [-1,0] or coordDiff == [-1,1] :
                #print("goal placed on house at "+str((i.coords[1],i.coords[0]))+"|right")
                translate(0,0,20)
                stroke(255,255,0) #yellow
                noFill()
                box(5)
                #break
            elif coordDiff == [1,0] or coordDiff == [1,-1] :
                #print("goal placed on house at "+str((i.coords[1],i.coords[0]))+"|left")
                translate(0,0,-20)
                stroke(255,255,0) #yellow
                noFill()
                box(5)
            else:
                #print("man what happened")
                pass
    

    translate(0,0,0) #resetting translates
    stroke(0)
    fill(255)
    #easier to visualize with multiple translates
    translate(10,-2.5,10) #Setting small cube to the center of the tile
    translate(postOffice[1]*20,0,postOffice[0]*20-50*20) #Set position to post office
    translate(-20,0,0) #Set position to below post office (THIS CAN BE AN ISSUE, BUT LITERALLY ALWAYS WORKED)
    stroke(255,255,0) #Yellow
    noFill()
    box(5)# Post office position visualizer
    translate(20,0,0)
    #The line below moves the "poof" shape around
    translate(mov[0],mov[1],mov[2])
    shape(poof)

    
    #Every 1/(10)+1 frames
    
    
    if framesElapsed == speed:
        # This is the global position
        # (((postOffice[0]*20)+(mov[2]))/20,((postOffice[1]*20)+(mov[0]))/20)
        #Example: currentPos = (24,26)
        
        # This is the destination position
        #Example: destination = (24, 30)
        
        #If the length of the reachedGoals is 5, then the next function should lead back to the post office
        #reachedGoals = []
        
        # This function will return a list of coordinates required to get from current position to next target
        # directionList = reconstruct_path(came_from, start, goal)
        
        # when emptied it will generate a new list of coordinates while also adding the position reached to a new list
        #if directionList == []:
        #    reachedGoals.append(currentPos)
        #    directionList = reconstruct_path(came_from, start, goal)
        
        #if directionList not == []:
        #   currDir = directionList.pop
        #   currDir = (currDir[0] - currentPos[0],currDir[0] - currentPos[0]) # The direction on this might be wrong
        
        if 0:
            if currDir==(0,1):
                control("Up")
            if currDir==(0,-1):
                control("Down")
            if currDir==(-1,0):
                control("Left")
            if currDir==(1,0):
                control("Right")
        #reset count
        framesElapsed = 0
        
        # moves to be done should be enqued. An easy way to do this is to provide coordinates and the math 
        # will be done here to determine what direction to move in
        # The AI function is what will be providing the queue
        # pop the oldest next move, do the next move in a queued up list of moves to take




    if keyPressed and key == '1':
        #clear()
        cam.feed()
        feed = 0    
            
    if keyPressed and key == '2':
        #clear()
        pov.feed()
        feed = 1

                
    if feed == 0: 
        if mousePressed:
            cam.track(mouseX - pmouseX, mouseY - pmouseY)
            pass
            
    if feed == 1:
        if mousePressed:
            pov.circle(radians(mouseX - pmouseX))
            pass  
    

    # -------------HUD-------------
    # https://discourse.processing.org/t/drawing-2d-gui-over-a-3d-sketch/22819
    hint(DISABLE_DEPTH_TEST); 
    stroke(0)
    camera()
    ortho()
    fill(255)
    rect(20, 10, 180, 200)
    fill(0)
    text(("FPS: "+str(frameRate)[:5]), 30, 30)
    text(("Time Elapsed: "+str(elapsed)[:5]), 30, 45)
    text(("Packages Left: "+str(mail_amt)), 30, 60)
    #text("Local Pos: "+str((mov[0]/20,mov[2]/20)), 30, 75)
    text("Global Pos: "+str((((postOffice[0]*20)+(mov[2]))/20,((postOffice[1]*20)+(mov[0]))/20)), 30, 75)
    line(24, 86, 190, 86)
    text("Distance from [Post Office]:", 30, 100)
    text("A: []", 30, 115)
    text("B: []", 30, 130)
    text("C: []", 30, 145)
    text("D: []", 30, 160)
    text("E: []", 30, 175)
    line(24, 187.5, 190, 187.5)
    hint(ENABLE_DEPTH_TEST);
    

def control(direction):
    global populated    
    poX=postOffice[1]
    poY=postOffice[0]
    localX = mov[0]/20
    localY = mov[2]/20
    globX  = ((poX)+(mov[0]+20))/20
    globY  = (poY*20+(mov[2]))/20
    
    if direction == "Up":
        if (globY,((poX*20)+(mov[0]+20))/20) in populated:
            pov.aim((poX*20)+(mov[0]+20),pov.target()[1],(poY*20+(mov[2])))
            pov.jump((mov[0]+20),-40,500)
            mov[0]=mov[0]+20    
        if (globY,((poX*20)+(mov[0]+20))/20) not in populated:
            #print("Illegal move") # Can't drive on grass
            pass
            
    if direction == "Down":
        if (globY,((poX*20)+(mov[0]-20))/20) in populated:
            pov.aim((poX*20)+(mov[0]-20),pov.target()[1],(poY*20+(mov[2])))
            pov.jump((mov[0]-20),-40,500)
            mov[0]=mov[0]-20    
        if (globY,((poX*20)+(mov[0]-20))/20) not in populated:
            #print("Illegal move") # Can't drive on grass
            pass

    if direction == "Left":
        if (((poY*20)+(mov[2]-20))/20,((poX*20)+(mov[0]))/20) in populated:
            pov.aim((poX*20)+(mov[0]-20),pov.target()[1],(poY*20+(mov[2])))
            pov.jump((mov[0]-20),-40,500)
            mov[2]=mov[2]-20
        elif (((poY*20)+(mov[2]-20))/20,((poX*20)+(mov[0]))/20) not in populated:
            #print("Illegal move") # Can't drive on grass
            pass

    if direction == "Right":
        if (((poY*20)+(mov[2]+20))/20,((poX*20)+(mov[0]))/20) in populated:
            pov.aim((poX*20)+(mov[0]+20),pov.target()[1],(poY*20+(mov[2])))
            pov.jump((mov[0]+20),-40,500)
            mov[2]=mov[2]+20
        elif (((poY*20)+(mov[2]+20))/20,((poX*20)+(mov[0]))/20) not in populated:
            #print("Illegal move") # Can't drive on grass
            pass        


    
def keyPressed():
    global populated
    #print (key, keyCode)
    poX=postOffice[1]
    poY=postOffice[0]
    
    localX = mov[0]/20
    localY = mov[2]/20
    globX  = ((poX)+(mov[0]+20))/20
    globY  = (poY*20+(mov[2]))/20
    
    def debug():
        print(" Local: "+str((localY,localX)))
        print("Global: "+str((((poY*20)+(mov[2]))/20,((poX*20)+(mov[0]))/20)))
        pass
        
    if keyCode == 38:
        control("Up")
        #debug()

    if keyCode == 40:
        control("Down")
        #debug()
        
    if keyCode == 37:
        control("Left")
        #debug()

    if keyCode == 39:
        control("Right")
        #debug()
        
    if key == 'r':
        pov.jump(600,-40,600)
        cam.jump(500, -1000, 500)
        cam.aim(500, 0, 500)
        cam.tilt(0)

    # garbage collection idea?
    if key == ESC: 
        this.key = '0'
        print("beginning cleanup...")
        global taken, populated, buildings, goals, sts, grid
        del taken
        del populated
        del buildings
        del goals
        del sts
        del grid
        gc.collect()
        exit()



def mouseWheel(event): 
    global feed
    e = event.getCount()
    if feed == 0:
        if cam.position()[1] < -175 and e < 0:
            cam.dolly(e*25)
        if cam.position()[1] > -900 and e > 0:
            cam.dolly(e*25)
    if feed == 1:
        pov.zoom(radians(e) / 2.0)
