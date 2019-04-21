import random
import math
from tkinter import *


def distance(x1, y1, x2, y2):
    #Distance formula
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def magnitude(vector):
    #Find the magnitude of a vector
    return (vector[0]**2+vector[1]**2)**0.5

class Sand(object):
    #Creates sand object with position and directional changes
    def __init__(self, value, cx, cy, r, dx, dy, boing, gravity=2):
        self.value=value
        self.cx=cx
        self.cy=cy
        self.r=r
        self.dx=dx
        self.dy=dy
        if dx==0:
            self.angle=3*math.pi/2
        else:
            self.angle=math.atan(abs(self.dy)/abs(self.dx))
        self.boing=boing
    def __str__(self):
        return "%0.1f %0.1f" %(self.dx, self.dy)
    def draw(self, canvas):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, self.cx+self.r, self.cy+self.r)
    def move(self):
        self.cx+=math.cos(math.radians(self.angle))*self.dx
        self.cy+=math.sin(math.radians(self.angle))*self.dy
    def moveX(self):
        self.cx+=math.cos(math.radians(self.angle))*self.dx
    def unmoveX(self):
        self.dx = - self.dx
        self.cx += math.cos(math.radians(self.angle))*self.dx
        self.dx *= self.boing
    def unmoveY(self):
        self.dy = - self.dy
        self.cy += math.sin(math.radians(self.angle))*self.dy
        self.dy *= self.boing
    def collides(self, other):
        #Check if sand collides with a wall
        if (other.x1>self.cx+self.r or other.x2<self.cx-self.r or 
            other.y1>self.cy+self.r or other.y2<self.cy-self.r):
            #Edge case
            return False
        #Use vectors to calculate angle and height to check distance
        u=(other.x1-other.x2, other.y1-other.y2)
        v=(self.cx-other.x1, self.cy-other.y1)
        product=(u[0]*v[0]+u[1]*v[1])/(magnitude(u)*magnitude(v))
        angle=math.acos(product)
        h=distance(self.cx, self.cy, other.x1, other.y1)*math.sin(angle)
        if h<self.r:
            return True
        else:
            return False
    def updateAngle(self):
        if self.dx==0:
            self.angle=3*math.pi/2
        else:
            self.angle=math.atan(abs(self.dy)/abs(self.dx))
        

class Wall(object):
    #Create wall object represented as a line
    def __init__(self, x1, y1, x2, y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.slope=-(y2-y1)/(x2-x1)
        if x2-x1==0:
            self.angle=3*math.pi/2
        else:
            self.angle=math.atan((y2-y1)/(x2-x1))
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2)

###############
# Draws a bouncing ball which can be paused
def init(data):
    data.dx = -1.5
    data.dy = 5
    data.isPaused = False
    data.timerDelay = 10
    data.gravity=2
    
    #Add a dampening effect
    data.boing = 0.6

    #Create sand and wall
    data.sand=Sand(10, data.width/2, data.height/2, 10, data.dx, data.dy, data.boing)
    data.wall=Wall(data.width/10, data.height*19/20, data.width*8/10, data.height)
    
def timerFired(data):
    if (not data.isPaused):
        print(data.sand)
        doStep(data)

def doStep(data):
    #Moves sand
    data.sand.move()
    data.sand.updateAngle()
    #Check collisions
    if data.sand.collides(data.wall):
        print()
        data.sand.cy=data.wall.slope*(data.sand.cx-data.wall.x1)+data.wall.y1
        data.sand.angle=(data.wall.angle-math.pi+data.sand.angle)
        data.sand.angle%=(2*math.pi)
        if data.sand.angle==math.pi/2 or data.sand.angle==3*math.pi/2:
            if 0<data.wall.angle<math.pi/2 or math.pi<data.wall.angle<3*math.pi/2:
                data.sand.dx=-1
            else:
                data.sand.dx=1
        data.sand.unmoveY()
        data.sand.moveX()
    #Check boundaries
    if data.sand.cx-data.sand.r<=0 or data.sand.cx+data.sand.r>=data.width:
        data.sand.unmoveX()
    if data.sand.cy-data.sand.r<=0 or data.sand.cy+data.sand.r>=data.height:
        data.sand.unmoveY()
    #Update gravity
    data.sand.dy+=data.gravity

def redrawAll(canvas, data):
    # draw the ball
    data.sand.draw(canvas)
    data.wall.draw(canvas)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()