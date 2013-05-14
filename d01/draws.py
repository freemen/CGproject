#-*- coding: utf-8 -*-
#! encoding:utf-8
from Tkinter import *
from copy import deepcopy
import time
from math import *

def initView(tk):
    tk.title("本来应该是non_Chinese，但是现在加了encoding就可以了")
    tk.minsize(800,500)
    tk.maxsize(1000,600)

class VertexGroup:
    class EdgeTable:
        def __init__(self, canvas):
            self.canvas = canvas
            self.edgeList = {}
        def insert(self, y, x0, dx, ymax):
            if not y in self.edgeList:
                self.edgeList[y] = []

            #MUST! insert by sort
            newE = {'x': x0, 'dx': dx, 'ymax': ymax}
            if newE in self.edgeList[y]:
                self.edgeList[y].remove(newE)
                #print 'delete', y
            else:
                for i in self.edgeList[y]:
                    if i['x'] > x0:
                        self.edgeList[y].insert(self.edgeList[y].index(i), newE)
                        #print 'herre', newE
                        break
                else:
                    self.edgeList[y].append(newE)
                 
                if self.edgeList[y] == []:
                    self.edgeList[y].append({'x': x0, 'dx': dx, 'ymax': ymax})
            #print 'insert y:', y,' the ',newE, "\nis ", self.edgeList[y]

        def calcDx(self, v1, v2):
            return ((v1[0]-v2[0]) / float(v1[1]-v2[1]))
        def updateN(self, lastV, newV, firstV):
            #print 'before:',self.edgeList
            #here should the [1] should add 0.5
            if newV[1] < lastV[1]:#mode 1: judge by if-else
                dx = self.calcDx(newV, lastV)
                self.insert(newV[1], (newV[0]+0.5*dx), dx, lastV[1])
            elif newV[1] > lastV[1]:
                dx = self.calcDx(newV, lastV)
                self.insert(lastV[1], (lastV[0]+0.5*dx), dx, newV[1])
                
            if firstV[1] < lastV[1]:#mode 1: judge by if-else
                dx = self.calcDx(firstV, lastV)
                #print 'first',firstV
                #print 'dx', dx
                self.insert(firstV[1], (firstV[0]+0.5*dx), dx, lastV[1])
            elif firstV[1] > lastV[1]:
                dx = self.calcDx(firstV, lastV)
                self.insert(lastV[1], (lastV[0]+0.5*dx), dx, firstV[1])
                
            if newV[1] < firstV[1]:#mode 1: judge by if-else
                dx = self.calcDx(newV, firstV)
                self.insert(newV[1], (newV[0]+0.5*dx), dx, firstV[1])
            elif newV[1] > firstV[1]:
                dx = self.calcDx(newV, firstV)
                self.insert(firstV[1], (firstV[0]+0.5*dx), dx, newV[1])                
                
        def generateAET(self, NET, vertexs):         #edge:{'x': x0, 'dx': dx, 'ymax': ymax}
            miny = min(NET.edgeList.keys())
            maxy = vertexs[0][1]
            maxx = 0
            for xy in vertexs:
                if xy[1]>maxy:
                    maxy = xy[1]
                if xy[0]>maxx:
                    maxx = xy[0]

            self.canvas.show.create_rectangle(0,miny, maxx, maxy, outline = '#fff',fill= '#fff')
            self.edgeList[miny] = NET.edgeList[miny]
            self.fillin(self.edgeList[miny], miny)
            miny += 1
            for y in range(miny, maxy):
                self.edgeList[y] = []
                #update the edge
                for edge in self.edgeList[y-1]:
                    edgex = edge['x']
                    if edge['ymax'] > y:
                        edgex = edgex + edge['dx']
                        self.insert(y, edgex, edge['dx'], edge['ymax'])
                #insert new edges
                if y in NET.edgeList:
                    for newedge in NET.edgeList[y]:
                        self.insert(y, newedge['x'], newedge['dx'], newedge['ymax'])
                        
                self.fillin(self.edgeList[y], y)
                
        def fillin(self, elist, y):
        #draw!

            for i in range(0, len(elist), 2):
                for x in range(int(floor(elist[i]['x'])), int(ceil(elist[i+1]['x']))) :
                    self.canvas.drawMyPoint(x, y, self.canvas.fillcolor)
              
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.clear()

    def clearEdgeTable(self):
        self.NET = self.EdgeTable(self.canvas)
        self.AET = self.EdgeTable(self.canvas)
    def clear(self):
        self.vertexs = []
        self.clearEdgeTable()

    def addPoint(self, x, y):
        #print 'x:', x, ' y:', y
        if self.vertexs:
            self.lastVertex = self.vertexs[-1]
            if len(self.vertexs) >= 2:
                self.NET.updateN(self.lastVertex, [x, y], self.vertexs[0])
                #print 'NET',self.NET.edgeList
            #if len(self.vertexs) >= 3:
             #   self.NET.updateN(self.lastVertex, [x, y], self.vertexs[0])#TODOnext 
        else:           # the first point! and should not update the NET
            self.lastVertex = []
        self.vertexs.append([x,y])
        
        return self.lastVertex
    def close(self):
        return self.vertexs[-1], self.vertexs[0]

    def genAET(self):
        #self.AET = self.EdgeTable(self.canvas)
        self.AET.edgeList = {}
        self.AET.generateAET(self.NET, self.vertexs)

class Bresenham:
    def __init__(self, canvas):
        self.canvas = canvas
        
    def draw(self, x1, y1, x2, y2):
        x = x1
        y = y1
        self.canvas.drawPoint(x, y)
        dx = x2 - x1
        dy = y2 - y1
        ddx = abs(dx)
        ddy = abs(dy)
        if dx >= 0:
            sx = 1
        else:
            sx = -1
        if dy >= 0:
            sy = 1
        else:
            sy = -1
        if ddy <= ddx:
            wucha = (ddy<<1) - ddx
            for i in range(0, ddx):
                x += sx
                if wucha < 0:
                    wucha += (ddy<<1)
                else:
                    y += sy
                    wucha += ((ddy<<1) - (ddx<<1))
                self.canvas.drawPoint(x, y)
        else:
            wucha = (ddx<<1) - ddy
            for i in range(0, ddy):
                y += sy
                if wucha <0:
                    wucha += (ddx<<1)
                else:
                    x += sx
                    wucha += ((ddx<<1) -(ddy<<1))
                self.canvas.drawPoint(x, y)
    
class Showing:
    def __init__(self, tk):
        self.root = tk
        self.show = Canvas(tk,bg="#fbf4f4",height=500,width=600)
        self.show.grid(row=0, rowspan = 100, column=1)#, columnspan = 2)
        self.show.bind('<Button-1>',self.press)
        self.show.bind('<Button-3>', self.rightclick)

        self.color = "#222"
        self.pointcolor = "#d44"
        self.fillcolor = "#259"
        self.state = 'nothing'
	self.animationState = 'stop'

        self.vGroup = VertexGroup(self)
        self.originT = [[1,0,0],[0,1,0],[0,0,1]]
	self.transT = deepcopy(self.originT)
        self.xymark = []
	self.leftorright = 'none'
        self.forLine = Bresenham(self)
        
    def press(self, event):
        returnValue = self.functions[self.state](self, event)
    def rightclick(self, event):
        returnValue = self.rightfunctions[self.state](self, event)
                
    def drawMyPoint(self, x, y, color):
        self.show.create_line(x, y ,x+1 ,y+1 , fill=color)
    def drawPoint(self, x, y):
        self.drawMyPoint(x, y, self.color)        

    def doNothing(self, event):
        size = 2
        for i in range(-size,size+1):
            for j in range(-size,size+1):
                self.drawMyPoint(event.x+i, event.y+j, self.pointcolor)        

    def drawDot(self, event):
        self.drawPoint(event.x, event.y)
    
    def drawLine(self, event):
        firstV = self.vGroup.addPoint(event.x, event.y)
        if firstV:
            self.forLine.draw(firstV[0], firstV[1], event.x, event.y)
            self.vGroup.clear()

    def drawPolygon(self, event):
        lastV = self.vGroup.addPoint(event.x, event.y)
        if lastV:
            self.forLine.draw(lastV[0], lastV[1], event.x, event.y)
            if [event.x, event.y] == self.vGroup.vertexs[0]:
                self.vGroup.clear()
        else:
            self.doNothing(event)
    def closePolygon(self, event):
        endV, beginV = self.vGroup.close()
        self.forLine.draw(endV[0], endV[1], beginV[0], beginV[1])
        self.vGroup.clear()        

    def fillPolygon(self, event):
        self.drawPolygon(event)
        #print '\n\n\n\n\n\n'
        if len(self.vGroup.vertexs) >=3:
            self.vGroup.genAET()

    def matrixMul(self, M1, M2):
	M3 = []
	if len(M1) == 0 or len(M2) == 0 or (not len(M1[0]) == len(M2)):
	    return M3
	for row1 in M1:
	    newrow = []
	    for column2 in range(0, len(M2[0])):
		newitem = 0
		for c1r2 in range(0, len(row1)):
		    newitem += (row1[c1r2]*(M2[c1r2][column2]))
		newrow.append(newitem)
	    M3.append(newrow)
	return M3

    def dotrans(self):
        newv = []
	self.vGroup.clearEdgeTable()
        for i in self.vGroup.vertexs:
            newvv = []
            for column in range(0, 3):
               newvv.append(int((self.transT[0][column]*i[0]) + (self.transT[1][column]*i[1]) + (self.transT[2][column]*1)))
	    if len(newv) >=2:
      	        self.vGroup.NET.updateN(newv[-1], newvv, newv[0])
            newv.append(newvv)
	self.vGroup.vertexs = newv	
	self.vGroup.genAET()
	print 'vertexs',self.vGroup.vertexs
        
    def trans(self, event):
        if len(self.xymark) == 0:
            self.xymark.append([event.x, event.y]) #translation or symmetry
	    self.leftorright = 'left'
        else:
            self.xymark.append([event.x, event.y])
	    if self.leftorright == 'left':	#two left click is translation
		self.transT[2][0] = self.xymark[1][0] - self.xymark[0][0]
		self.transT[2][1] = self.xymark[1][1] - self.xymark[0][1]
	    elif self.leftorright == 'right':	#left click after right is zoom
	    	self.leftorright = 'zoom'
		print 'zoom'
		return
	    elif self.leftorright == 'zoom':	#first left click is reference
		print 'zoom!'
		moveT = deepcopy(self.originT)
		moveT[2][0] = -self.xymark[0][0]
		moveT[2][1] = -self.xymark[0][1]
		ref = hypot(abs(self.xymark[1][0] - self.xymark[0][0]),abs(self.xymark[1][1] - self.xymark[0][1]))
		self.transT[0][0] = (float(abs(self.xymark[2][0] - self.xymark[0][0]))/ref)
		self.transT[1][1] = (float(abs(self.xymark[2][1] - self.xymark[0][1]))/ref)
		print 'transT',self.transT
		self.transT = self.matrixMul(moveT, self.transT)
		moveT[2][0] = self.xymark[0][0]
		moveT[2][1] = self.xymark[0][1]
		print '2transT',self.transT
		self.transT = self.matrixMul(self.transT, moveT)
		print '3transT',self.transT
	    else:
		self.xymark = []
		self.leftorright = 'none'
		self.transT = deepcopy(self.originT)
		return
	    self.dotrans()
	    self.xymark = []
	    self.leftorright = 'none'
	    self.transT = deepcopy(self.originT)

    def rtrans(self, event):
        if len(self.xymark) == 0:
            self.xymark.append([event.x, event.y]) #rotate or zoom
	    self.leftorright = 'right'
        else:
            self.xymark.append([event.x, event.y])
	    if self.leftorright == 'right':	#two right click is rotate
		moveT = deepcopy(self.originT)
		moveT[2][0] = -self.xymark[0][0]
		moveT[2][1] = -self.xymark[0][1]
		x = (self.xymark[1][0] - self.xymark[0][0])
		y = (self.xymark[1][1] - self.xymark[0][1])
		self.transT[0][0] = (x/hypot(x,y)) 
		self.transT[0][1] = (y/hypot(x,y)) 
		self.transT[1][0] = -(y/hypot(x,y))
		self.transT[1][1] = (x/hypot(x,y))
		self.transT = self.matrixMul(moveT, self.transT)
		moveT[2][0] = self.xymark[0][0]
		moveT[2][1] = self.xymark[0][1]
		self.transT = self.matrixMul(self.transT, moveT)
	    elif self.leftorright == 'left':	#right click after left is symmetry 
		moveT = deepcopy(self.originT)
		ddx = (self.xymark[1][0] - self.xymark[0][0])
		ddy = (self.xymark[1][1] - self.xymark[0][1])
		dx = abs(ddx)
		dy = abs(ddy)
		#print "dx, dy: ", ddx, " ", ddy
		moveT[2][0] = -self.vGroup.vertexs[0][0]
		moveT[2][1] = -self.vGroup.vertexs[0][1]
		if (dx/2) >= dy:	#bd
		    self.transT[0][0] = -1
		    moveT[2][0] -= (ddx/2)
		elif (dy/2) >= dx:	#bp
		    self.transT[1][1] = -1
		    moveT[2][1] -= (ddy/2)
		else:
		    if not((ddx > 0 and ddy > 0) or (ddx < 0 and ddy < 0)):	#CU
			self.transT[0][0] = 0
			self.transT[0][1] = 1
			self.transT[1][0] = 1
			self.transT[1][1] = 0
		    else:						#Cn
			self.transT[0][0] = 0
			self.transT[0][1] = -1
			self.transT[1][0] = -1
			self.transT[1][1] = 0
		    moveT[2][0] -= (ddx/2)
		    moveT[2][1] -= (ddy/2)
		self.transT = self.matrixMul(moveT, self.transT)
		moveT[2][0] = -moveT[2][0] 
		moveT[2][1] = -moveT[2][1]
		self.transT = self.matrixMul(self.transT, moveT)
	    else:
		self.xymark = []
		self.leftorright = 'none'
		self.transT = deepcopy(self.originT)
		return
	    self.dotrans()
	    self.xymark = []
	    self.leftorright = 'none'
	    self.transT = deepcopy(self.originT)

    def beginAnimation(self, event):
	if self.animationState == 'stop':
	    self.animationState = 'begin'


    functions = {
        'nothing': doNothing,
        'dot': drawDot,
        'line': drawLine,
        'polygon': drawPolygon,
        'filledpolygon': fillPolygon,
        'twoDtrans': trans,
        'cut': doNothing,
        'animation': beginAnimation,
        }
    rightfunctions = {
        'polygon': closePolygon,
        'filledpolygon': closePolygon, #fillPolygon,        
	'twoDtrans': rtrans,
        }
        
class Choice:
    def __init__(self, tk, target):
        self.root = tk
        self.target = target
        
        self.nowcolor = "#60a090"
        self.defaultcolor = "#b0e0d0"
        mlabel = Label(tk, text = "选项")
        mlabel.grid(row=0,column=0, sticky=N)

        self.dotB = Button(tk,text="画点",command = self.dot, width = 20, height=2, bg = self.defaultcolor)
        self.dotB.grid(row=2,column=0, sticky=N)        
        self.lineB = Button(tk,text="画线",command = self.line, width = 20, height=2, bg = self.defaultcolor)
        self.lineB.grid(row=3,column=0, sticky=N)
        self.polygonB = Button(tk,text="画多边形",command = self.polygon, width = 20, height=2, bg = self.defaultcolor)
        self.polygonB.grid(row=4,column=0, sticky=N)
        self.filledpolygonB = Button(tk,text="填充的多边形",command = self.filledpolygon, width = 20, height=2, bg = self.defaultcolor)
        self.filledpolygonB.grid(row=5,column=0, sticky=N)
        self.twoDtransB = Button(tk,text="二维变换",command = self.twoDtrans, width = 20, height=2, bg = self.defaultcolor)
        self.twoDtransB.grid(row=6,column=0, sticky=N)
        self.cutB = Button(tk,text="裁剪",command = self.cut, width = 20, height=2, bg = self.defaultcolor)
        self.cutB.grid(row=7,column=0, sticky=N)
        self.animationB = Button(tk,text="关键帧动画",command = self.animation, width = 20, height=2, bg = self.defaultcolor)
        self.animationB.grid(row=8,column=0, sticky=N)

        self.byeB = Button(tk,text="say GoodBye~",command = tk.quit, width = 20, height=2, bg = self.defaultcolor)
        self.byeB.grid(row=90,column=0, sticky=N) 
        self.buttons = {
            'dot': self.dotB,
            'line': self.lineB,
            'polygon': self.polygonB,
            'filledpolygon': self.filledpolygonB,
            'twoDtrans': self.twoDtransB,
            'cut': self.cutB,
            'animation': self.animationB,
            
            'bye': self.byeB,
            }    

    def dot(self):
        self.target.state = 'dot'
        self.setFocus()
        
    def line(self):
        self.target.state = 'line'
        self.setFocus()

    def polygon(self):
        self.target.state = 'polygon'
        self.setFocus()

    def filledpolygon(self):
        self.target.state = 'filledpolygon'
        self.setFocus()

    def twoDtrans(self):
        self.target.state = 'twoDtrans'
        self.setFocus()

    def cut(self):
        self.target.state = 'cut'
        self.setFocus()
        
    def animation(self):
        self.target.state = 'animation'
        self.setFocus()

    def setFocus(self):
        for i in self.buttons:
            self.buttons[i].configure(bg = self.defaultcolor)
        self.buttons[self.target.state].configure(bg = self.nowcolor)

if __name__ == '__main__':
    tk = Tk()
    initView(tk)
    my = Showing(tk)
    your = Choice(tk, my)
    tk.mainloop()
