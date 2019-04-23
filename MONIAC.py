#MONIAC.py game
import math
import random
from tkinter import *

def readCsvFile(path):
    # Returns a 2d list with the data in the given csv file
    result = [ ]
    for line in readFile(path).splitlines():
        result.append(line.split(','))
    return result

def distance(x1, y1, x2, y2):
    #Distance formula
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def magnitude(vector):
    #Find the magnitude of a vector
    return (vector[0]**2+vector[1]**2)**0.5


## Sand, Wall, Variable, and Button Objects
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
        if h<=self.r:
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
        #Calculate slope
        if x1==x2:
            self.slope=0
        else: self.slope=-(y2-y1)/(x2-x1)
        #Calculate angle
        if x2-x1==0:
            self.angle=3*math.pi/2
        else:
            self.angle=math.atan((y2-y1)/(x2-x1))
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2)

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
    def __init__(self, name, cx, cy, width, height, clicked=False):
        self.name=name
        self.x1=cx-width
        self.x2=cx+width
        self.y1=cy-height
        self.y2=cy+height
        self.cx=cx
        self.cy=cy
        self.clicked=clicked
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2)
    def isClicked(self, mouseX, mouseY):
        if (mouseX>=self.x1 and mouseX<=self.x2 and mouseY>=self.y1 and
            mouseY<=self.y2):
            return True
        else:
            return False

class VariableButton(Button):
    def __init__(self, name, cx, cy, width, height, value, clicked=False):
        super().__init__(name, cx, cy, width, height, clicked)
        self.value=value
    def draw(self, canvas):
        super().draw(canvas)
        canvas.create_text(self.cx, self.cy, text='%s: %0.2f'%(self.name, self.value))

class Valve(object):
    def __init__(self, rate, x1, y1, x2, y2):
        self.rate=rate
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
    def draw(self, canvas):
        pass

## MVC
def init(data):
    #initialize values
    data.interestRate=0.02
    data.taxRate=0.05
    data.importRate=0.5
    data.exportRate=0.5
    data.govSpendingRate=0.5
    # Initialize objects
    data.newX=data.width*2/3
    data.walls=initializeWalls(data)
    data.buttons=initializeButtons(data)
    #pausing
    data.isPaused=False
    data.buttonOn=False
    #Create sand
    data.dx = 1
    data.dy = 5
    data.timerDelay = 10
    data.gravity=2
    data.boing = 0.3
    data.sand=Sand(10, 10, 10, 10, data.dx, data.dy, data.boing)

def initializeWalls(data):
    #creates walls with amazing hard code
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
    
def initializeButtons(data):
    #creates buttons with more amazing hard code
    bWidth=data.width/15
    bHeight=data.height/25
    xPos=data.width*8/9
    interestRateButton=VariableButton("Interest Rt", xPos, data.height*6/11,
                              bWidth, bHeight, data.interestRate)
    taxRateButton=VariableButton("Tax Rt", xPos, data.height*7/11, bWidth,
                         bHeight, data.taxRate)
    importRateButton=VariableButton("Import Rt", xPos, data.height*8/11,
                            bWidth, bHeight, data.importRate)
    exportRateButton=VariableButton("Export Rt", xPos, data.height*9/11,
                            bWidth, bHeight, data.exportRate)
    govSpendingButton=VariableButton("Gov. Spending Rt", xPos,
                             data.height*10/11, bWidth, bHeight, 
                             data.govSpendingRate)
    return [interestRateButton, taxRateButton, importRateButton, 
            exportRateButton, govSpendingButton]

def timerFired(data):
    if (not data.isPaused):
        doStep(data)

def doStep(data):
    #Moves sand
    data.sand.move()
    data.sand.updateAngle()
    for wall in data.walls:
        if data.sand.collides(wall):
            print(data.sand.dx, data.sand.dy, data.sand.cx, data.sand.cy)
            if wall.slope==0:
                data.sand.unmoveX()
            else:
                data.sand.cy=wall.slope*(data.sand.cx-wall.x1)-data.sand.r
                data.sand.angle=(wall.angle-math.pi+data.sand.angle)
                data.sand.angle%=(2*math.pi)
                data.sand.unmoveY()
                data.sand.moveX()
            print(data.sand.dx, data.sand.dy, data.sand.cx, data.sand.cy)
    if data.sand.cx-data.sand.r<=0 or data.sand.cx+data.sand.r>=data.width:
        data.sand.unmoveX()
    if data.sand.cy-data.sand.r<=0 or data.sand.cy+data.sand.r>=data.height:
        data.sand.unmoveY()
    data.sand.dy+=data.gravity

def mousePressed(event, data):
    print(event.x, event.y)
    if data.isPaused==False:
        for button in data.buttons:
            if button.isClicked(event.x, event.y):
                button.clicked=True
            else:
                button.clicked=False
            print(button.clicked)
    
def keyPressed(event, data):
    pass


def drawButtonPage(canvas, data, name):
    pass

def redrawAll(canvas, data):
    for wall in data.walls:
        wall.draw(canvas)
    for button in data.buttons:
        button.draw(canvas) 
    data.sand.draw(canvas)

## Run Functions
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
    root.title("MONIAC Main")
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