#MONIAC.py game
import math
from tkinter import *

class Variable(object):
    def __init__(self, name, cx, cy, width, height, value):
        self.name=name
        self.x1=cx-width
        self.x2=cx+width
        self.y1=cy-height
        self.y2=cy+height
        self.cx=cx
        self.cy=cy
        self.value=value
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2)
        canvas.create_text(self.cx, self.cy, text='%s: %d'%(self.name, self.value))
    def move(self):
        self.cy-=5
        self.y1-=5
        self.y2-=5
    def reachesCheckPoint(self, checkPointHeight):
        if self.cy>=checkPointHeight:
            return True
        else:
            return False

class Button(object):
    def __init__(self, name, cx, cy, width, height, value):
        self.name=name
        self.x1=cx-width
        self.x2=cx+width
        self.y1=cy-height
        self.y2=cy+height
        self.cx=cx
        self.cy=cy
        self.value=value
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2)
        canvas.create_text(self.cx, self.cy, text='%s: %d'%(self.name, self.value))
    def isClicked(self, mouseX, mouseY):
        if (mouseX>=self.x1 and mouseX<=self.x2 and mouseY>=self.y1 and
            mouseY<=self.y2):
            return True
        else:
            return False

class Wall(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        if x2-x1==0:
            self.angle=3*math.pi/2
        else:
            self.angle=math.atan((y2-y1)/(x2-x1))
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2)

def init(data):
    # Initialize values
    data.newX=data.width*2/3
    data.walls=initializeWalls(data)

def initializeWalls(data):
    #border wall
    wall0=Wall(data.newX, 0, data.newX, data.height)
    #G trapezoid
    wall1=Wall(data.newX/3, data.height/18, data.newX/3, data.height/2)
    wall2=Wall(data.newX/3, data.height/9, data.newX/6, data.height/3)
    wall3=Wall(data.newX/6, data.height/3, data.newX/6, data.height*4/9)
    wall4=Wall(data.newX/6, data.height*4/9, data.newX/3, data.height/2)
    #G bottom
    wall5=Wall(0, data.height*5/9, data.newX/3, data.height*2/3)
    wall6=Wall(data.newX/3, data.height*2/3, data.newX/3, data.height)
    #S trapezoid
    wall7=Wall(data.newX*2/3, data.height/9, data.newX*2/3, data.height*5/9)
    wall8=Wall(data.newX*2/3, data.height/3, data.newX*5/6, data.height*7/18)
    wall9=Wall(data.newX*5/6, data.height*7/18, data.newX*5/6, data.height/2)
    wall10=Wall(data.newX*5/6, data.height/2, data.newX*2/3, data.height*5/9)
    #I triangle
    wall11=Wall(data.newX*2/3, data.height*12/18, data.newX*17/18, data.height*31/54)
    wall12=Wall(data.newX*2/3, data.height*12/18, data.newX*17/18, data.height*15/18)
    wall13=Wall(data.newX*17/18, data.height/2, data.newX*17/18, data.height*14/18*11/10*16/15)
    #MX triangle
    wall14=Wall(data.newX/2, data.height*113/180*11/10, data.newX/2, data.height*8/9)
    wall15=Wall(data.newX/2, data.height*113/180*11/10, data.newX*3/4, data.height*14/18*11/10)
    wall16=Wall(data.newX*3/4, data.height*14/18*11/10, data.newX/2, data.height*8/9)
    #MX base trapezoid
    wall17=Wall(data.newX*3/4, data.height*14/18*11/10*16/15, data.newX/2, data.height*8/9*16/15)
    wall18=Wall(data.newX*3/4, data.height*14/18*11/10*16/15, data.newX*5/6, 
                data.height*14/18*11/10*16/15)

    return [wall0, wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, 
            wall9, wall10, wall11, wall12, wall13, wall14, wall15, wall16, 
            wall17, wall18]
    
def mousePressed(event, data):
    pass
    
def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def redrawAll(canvas, data):
    for wall in data.walls:
        wall.draw(canvas)
#################################################################
# use the run function as-is
#################################################################

def runAnimation(width=1200, height=600):
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

runAnimation()