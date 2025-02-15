#MONIAC.py game
import math
import random
from tkinter import *
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation

import numpy as np


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

def roundUp(x):
    if x%1==0:
        return int(x)
    else:
        return int(x)+1


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
        #self.dx *= self.boing
    def unmoveY(self):
        self.dy = - self.dy
        self.cy += math.sin(math.radians(self.angle))*self.dy
        self.dy *= self.boing
    def collides(self, other):
        #Check if sand collides with a wall
        smallX=min([other.x1, other.x2])
        largeX=max([other.x1, other.x2])
        smallY=min([other.y1, other.y2])
        largeY=max([other.y1, other.y2])
        if (smallX>self.cx+self.r or largeX<self.cx-self.r or 
            smallY>self.cy+self.r or largeY<self.cy-self.r):
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
    '''
    def __eq__(self, other):
        return (isinstance(other, Sand) and self.cx==other.cx and 
                self.cy==other.cy and self.dx==other.dx and self.dy==other.dy
                and self.angle==other.angle)
    def __hash__(self):
        return hash(self.cx)
    '''
    
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
        else: self.slope=(y2-y1)/(x2-x1)
        #Calculate angle
        if x2-x1==0:
            self.angle=3*math.pi/2
        else:
            self.angle=math.atan((y2-y1)/(x2-x1))
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2)

## Button objects, change drawPage and isClicked functions to take in data
#isclicked-->modify data.isPaused and data.clickedButton
#drawPage-->simply to one functio that can intake data.drawAgain
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
    def draw(self, canvas, data):
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
    def draw(self, canvas, data):
        super().draw(canvas, data)
        canvas.create_text(self.cx, self.cy, text='%s: %0.2f'%(self.name, self.value))
    def drawPage(self, canvas, datax, datay, curInput):
        canvas.create_text(datax/2, datay/2, text='Input New %s'%(self.name))
        canvas.create_text(datax/2, datay*6/11, text=curInput)
    def drawPageAgain(self, canvas, datax, datay, curInput):
        canvas.create_text(datax/2, datay*5/11, text="Try again")
        canvas.create_text(datax/2, datay/2, text='Input New %s'%(self.name))
        canvas.create_text(datax/2, datay*6/11, text=curInput)
    def updateValue(self, input):
        assert(0<=float(input)<=1)
        self.value=float(input)
    
class GraphButton(Button):
    def draw(self, canvas, data):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2)
        if self.clicked:
            canvas.create_text(self.cx, self.cy, text='Graph Showing')
        else:
            canvas.create_text(self.cx, self.cy, text='Show Graph')


class Valve(object):
    def __init__(self, rate, x1, y1, x2, y2):
        self.rate=rate
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.value=0
    def draw(self, canvas):
        x1=self.x1
        y1=self.y1
        x2=self.x2
        y2=self.y2
        canvas.create_rectangle(x1, y1, x2, y2, fill='green')
        canvas.create_text((x1+x2)/2, (y1+y2)/2, text=self.value)
    def releaseBalls(self, r, dx, dy, boing):
        ballsReleased=roundUp(self.value/10*self.rate)
        sandL=[]
        ballGrid=createSandGrid(3, ballsReleased)
        startX=(self.x1+self.x2)/2
        startY=self.y2
        for row in range(len(ballGrid)):
            for col in range(len(ballGrid[row])):
                if ballGrid[row][col]!=None:
                    sand=Sand(10, startX+r*2*col, startY+r*(2*row+1), r, dx, dy, boing)
                    sandL.append(sand)
        self.value-=ballsReleased*10
        return sandL
    def collides(self, cy, cx, r):
        return cy+r>=self.y1 and cy-r<=self.y2 and cx-r<=self.x2 and cx+r>=self.x1

class SumValve(Valve):
    def __init__(self, rate, x1, y1, x2, y2, spendingRate):
        super().__init__(rate, x1, y1, x2, y2)
        self.spendingRate=spendingRate
    def releaseBalls(self, r, dx, dy, boing):
        ballsReleased1=roundUp(self.value*(1-self.rate)/10*self.spendingRate)
        ballsReleased2=int(self.value*self.rate/10*self.spendingRate)
        sandL=[]
        ballGrid1=createSandGrid(10, ballsReleased1)
        ballGrid2=createSandGrid(10, ballsReleased2)
        startX1=self.x1+(self.x2-self.x1)/4
        startX2=self.x1+(self.x2-self.x1)*2/3
        startY=self.y2
        for row in range(len(ballGrid1)):
            for col in range(len(ballGrid1[row])):
                if ballGrid1[row][col]!=None:
                    sand=Sand(10, startX1+r*2*col, startY+r*(2*row+1), r, -dx, dy, boing)
                    sandL.append(sand)
        for row in range(len(ballGrid2)):
            for col in range(len(ballGrid2[row])):
                if ballGrid2[row][col]!=None:
                    sand=Sand(10, startX2+r*2*col, startY+r*(2*row+1), r, dx, dy, boing)
                    sandL.append(sand)
        self.value-=(ballsReleased1+ballsReleased2)*10
        return sandL


class HorizontalValve(Valve):
    def releaseBalls(self, r, dx, dy, boing):
        ballsReleased=roundUp(self.value/10*self.rate)
        sandL=[]
        ballGrid=createSandGrid(3, ballsReleased)
        startX=self.x1-r
        startY=(self.y1+self.y2)/2
        for row in range(len(ballGrid)):
            for col in range(len(ballGrid[row])):
                if ballGrid[row][col]!=None:
                    sand=Sand(10, startX-r*2*col, startY+r*(2*row+1), r, -abs(dx), dy, boing)
                    sandL.append(sand)
        self.value-=ballsReleased*10
        return sandL

## MVC
def init(data):
    #initialize macroeconomic variables
    #data.GDP=5000
    data.ballValue=10
    data.GDP=500
    data.interestRate=0.02
    data.lendingRate=0.5
    data.taxRate=0.05
    data.importRate=0.5
    data.exportRate=0.5
    data.govSpendingRate=0.5
    data.spendingRate=0.5
    
    #graph stuff
    data.cValues=[0]
    data.gValues=[0]
    data.timerFiredCount=0
    
    
    #initialize background objects
    data.newX=data.width*2/3
    data.walls=initializeWalls(data)
    data.buttons=initializeButtons(data)
    data.valves=initializeValves(data)
    
    #pausing
    data.isPaused=False
    data.buttonOn=False
    data.clickedButton=None
    data.buttonInput=''
    data.drawAgain=False
    
    data.timerDelay = 10

    #initialize sand
    data.dx = 0.5
    data.dy = 1
    data.gravity=2
    data.boing = 0.3
    data.xboing=0.7
    data.radius=3
    data.sand=initializeConSand(data)+initializeSavingSand(data)+initializeGovSand(data)

def initializeGovSand(data):
    sandL=[]
    govGrid=createSandGrid(8, int(data.GDP*data.taxRate))
    startX=data.newX/20
    startY=data.newX/20
    for row in range(len(govGrid)):
        for col in range(len(govGrid[row])):
            if govGrid[row][col]!=None:
                sand=Sand(10, startX+data.radius*2*col, startY+data.radius*2*row, data.radius, 
                          data.dx, data.dy, data.boing)
                sandL.append(sand)
    return sandL

def initializeConSand(data):
    sandL=[]
    consumptionGrid=createSandGrid(16, int(data.GDP*(1-data.taxRate-data.interestRate)))
    startX=data.newX*2/5
    startY=data.newX/20
    for row in range(len(consumptionGrid)):
        for col in range(len(consumptionGrid[row])):
            if consumptionGrid[row][col]!=None:
                sand=Sand(10, startX+data.radius*2*col, startY+data.radius*2*row, data.radius, 
                          data.dx, data.dy, data.boing)
                sandL.append(sand)
    return sandL
    
def initializeSavingSand(data):
    sandL=[]
    savingGrid=createSandGrid(4, int(data.GDP*data.interestRate))
    startX=data.newX*7/10
    startY=data.newX/20
    for row in range(len(savingGrid)):
        for col in range(len(savingGrid[row])):
            if savingGrid[row][col]!=None:
                sand=Sand(10, startX+data.radius*2*col, startY+data.radius*2*row, data.radius, 
                          data.dx, data.dy, data.boing)
                sandL.append(sand)
    return sandL

def createSandGrid(cols, balls):
    L=[]
    while balls>0:
        if balls>=cols:
            L.extend([[0]*(cols)])
            balls-=cols
        else:
            L.extend([[0]*(balls%cols)+[None]*(cols-balls%cols)])
            balls-=balls%cols
    return L

def initializeValves(data):
    #Creates valves
    govValve=Valve(data.govSpendingRate, 0, data.height/3, data.newX/6, data.height*4/9)
    bankValve=Valve(data.lendingRate, data.newX*5/6, data.height*7/18, data.newX, data.height/2)
    foreignValve=HorizontalValve(data.exportRate, data.newX*3/4, data.height*14/18*11/10,
                       data.newX*17/18, data.height*14/18*11/10*16/15)
    spendingValve=SumValve(data.importRate, data.newX/3, data.height/2, 
                           data.newX*2/3, data.height*12/18, data.spendingRate)
    return [govValve, bankValve, foreignValve, spendingValve]

def initializeWalls(data):
    #creates walls with amazing hard code
    #border wall
    wall0=Wall(data.newX, 0, data.newX, data.height)
    #G trapezoid
    wall1=Wall(data.newX/3, data.height/18, data.newX/3, data.height/2)
    wall2=Wall(data.newX/6, data.height/3, data.newX/3, data.height/9)
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
    wall12=Wall(data.newX*17/18, data.height*15/18, data.newX*2/3, data.height*12/18)
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
    pauseButton=Button("Pause Button", xPos, data.height*3/11, bWidth, bHeight)
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
    graphButton=GraphButton("Graph Button", xPos, data.height*5/11, bWidth, bHeight)
    return [pauseButton, interestRateButton, taxRateButton, importRateButton, 
            exportRateButton, govSpendingButton, graphButton]

def timerFired(data):
    if (not data.isPaused):
        newDoStep(data)
        releaseValves(data)
        data.timerFiredCount+=1

def newDoStep(data):
    i=0
    while i<(len(data.sand)):
        data.sand[i].move()
        data.sand[i].updateAngle()
        #wall collisions and bouncing
        for wall in data.walls:
            if data.sand[i].collides(wall):
                if wall.slope==0:
                    #reverse x if collides with vertical wall
                    if data.sand[i].dx>0:
                        data.sand[i].cx=wall.x1-data.sand[i].r
                    else:
                        data.sand[i].cx=wall.x1+data.sand[i].r
                    data.sand[i].unmoveX()
                else:
                    #set height to line and reverse dy
                    data.sand[i].cy=wall.slope*(data.sand[i].cx-wall.x1)+wall.y1
                    if data.sand[i].dy<0:
                        data.sand[i].cy+=data.sand[i].r
                    else:
                        data.sand[i].cy-=data.sand[i].r
                    
                    #modify angle
                    data.sand[i].angle=(wall.angle-math.pi+data.sand[i].angle)
                    data.sand[i].angle%=(2*math.pi)
                    
                    #modify dx
                    if data.sand[i].dx==0:
                        if (0<data.sand[i].angle<math.pi/2 or 
                            math.pi<data.sand[i].angle<3*math.pi/2):
                            data.sand[i].dx=1
                        else:
                            data.sand[i].dx=-1
                    else:
                        data.sand[i].dx/=data.xboing
                    '''
                    if data.sand[i].dy<0:
                        if (0<data.sand[i].angle<math.pi/2 or 
                            math.pi<data.sand[i].angle<3*math.pi/2):
                            print(1)
                            if data.sand[i].dx==0:
                                data.sand[i].dx=1
                            elif data.sand[i].dx>0:
                                data.sand[i].dx/=-data.boing
                            else:
                                data.sand[i].dx/=data.boing
                        else:
                            print(2)
                            if data.sand[i].dx==0:
                                data.sand[i].dx=1
                            elif data.sand[i].dx>0:
                                data.sand[i].dx/=data.boing
                            else:
                                data.sand[i].dx/=-data.boing
                    else:
                        if (0<data.sand[i].angle<math.pi/2 or 
                            math.pi<data.sand[i].angle<3*math.pi/2):
                            print(3)
                            if data.sand[i].dx==0:
                                data.sand[i].dx=1
                            elif data.sand[i].dx>0:
                                data.sand[i].dx*=-data.boing
                            else:
                                data.sand[i].dx*=data.boing
                        else:
                            print(4)
                            if data.sand[i].dx==0:
                                data.sand[i].dx=-1
                            elif data.sand[i].dx>0:
                                data.sand[i].dx*=data.boing
                            else:
                                data.sand[i].dx*=-data.boing
                    '''
                    #move
                    data.sand[i].unmoveY()
                    data.sand[i].moveX()
                    
                #stop moving
                if abs(data.sand[i].dy)<2:
                    data.sand[i].dx*=data.xboing
        
        #boundary bouncing
        if data.sand[i].cx-data.sand[i].r<=0 or data.sand[i].cx+data.sand[i].r>=data.width:
            data.sand[i].unmoveX()
            #stop dy
            if abs(data.sand[i].dy)<2:
                data.sand[i].dx=0
        if data.sand[i].cy-data.sand[i].r<=0 or data.sand[i].cy+data.sand[i].r>=data.height:
            data.sand[i].unmoveY()
            #stop dy
            if abs(data.sand[i].dy)<2:
                data.sand[i].dx=0
        data.sand[i].dy+=data.gravity
        
        #valve reactions
        collided=False
        for valve in data.valves:
            if valve.collides(data.sand[i].cy, data.sand[i].cx, data.sand[i].r):
                valve.value+=data.sand[i].value
                data.sand.pop(i)
                collided=True
                break
        if collided==False:
            i+=1

def releaseValves(data):
    for valve in data.valves:
        result=valve.releaseBalls(data.radius, 0.5, 1, data.boing)
        if valve.rate==data.govSpendingRate:
            data.cValues.append(len(result))
        elif valve.rate==data.importRate:
            data.gValues.append(len(result))
        data.sand.extend(result)
        

def mousePressed(event, data):
    #mouse and button interactions will mainly be here
    if data.clickedButton==None:
        for button in data.buttons:
            if button.isClicked(event.x, event.y):
                button.clicked=True
                data.isPaused=not data.isPaused
                data.clickedButton=button
                if not isinstance(data.clickedButton, VariableButton):
                    data.clickedButton=None
                break
            else:
                button.clicked=False
        if not data.isPaused:
            data.clickedButton=None

def keyPressed(event, data):
    if data.clickedButton!=None:
        if event.keysym=="Return":
            try:
                data.clickedButton.updateValue(data.buttonInput)
                data.clickedButton=None
                data.isPaused=False
                data.buttonInput=''
                data.drawAgain=False
            except:
                data.drawAgain=True
                data.buttonInput=''
        else:
            data.buttonInput+=str(event.char)

def redrawAll(canvas, data):
    if data.clickedButton==None:
        for wall in data.walls:
            wall.draw(canvas)
        for button in data.buttons:
            button.draw(canvas, data) 
        for valve in data.valves:
            valve.draw(canvas)
        for sand in data.sand:
            sand.draw(canvas)
    else:
        if data.drawAgain:
            data.clickedButton.drawPageAgain(canvas, data.width, data.height, data.buttonInput)
        else:
            try:               
                data.clickedButton.drawPage(canvas, data.width, data.height, data.buttonInput)
            except:
                for wall in data.walls:
                    wall.draw(canvas)
                for button in data.buttons:
                    button.draw(canvas, data) 
                for valve in data.valves:
                    valve.draw(canvas)
                for sand in data.sand:
                    sand.draw(canvas)

## Graph functions
def runGraph(data):
    #from https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_sgskip.html
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")
    style.use('fivethirtyeight')
    fig = Figure(figsize=(5, 4), dpi=100)
    #t1 = np.arange(0, data.timerFiredCount, .1)
    graph1=fig.add_subplot(211)
    graph2=fig.add_subplot(212)
    time1=np.array([i for i in range(len(data.cValues))])
    time2=np.array([i for i in range(len(data.gValues))])
    graph1.plot(time1, np.array(data.cValues))
    graph2.plot(time2, np.array(data.gValues))
    
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
    
    def on_key_press(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, canvas, toolbar)
    
    canvas.mpl_connect("key_press_event", on_key_press)
    
    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)
    
    tkinter.mainloop()
    # If you put root.destroy() here, it will cause an error if the window is
    # closed with the window manager.

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
    #runGraph(data)
    root.mainloop()  # blocks until window is closed
    print("bye!")

runAnimation()