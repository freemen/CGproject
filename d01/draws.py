#-*- coding: utf-8 -*-
#! encoding:utf-8
from Tkinter import *
import time

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
            #TODO:should be insert by sort
            newE = {'x': x0, 'dx': dx, 'ymax': ymax}
            if newE in self.edgeList[y]:
                self.edgeList[y].remove(newE)
            else:
                for i in self.edgeList[y]:
                    if i['x']> x0:
                        self.edgeList[y].insert(self.edgeList[y].index(i), newE)
                        break
            #self.edgeList[y].append({'x': x0, 'dx': dx, 'ymax': ymax})

        def calcDx(self, v1, v2):
            return ((v1[0]-v2[0])/(v1[1]-v2[1]))
        def initN(self, lastV, newV, firstV):
            if newV[1] < lastV[1]:
                dx = self.calcDx(newV, lastV)
                self.edgeList(newV[1]+0.5, newV[0], dx, lastV[1])
        def updateN(self, lastV, newV, firstV):
            #here should the [1] should add 0.5
            if newV[1] < lastV[1]:#mode 1: judge by if-else
                dx = self.calcDx(newV, lastV)
                self.insert(newV[1], (min(newV[0], lastV[0])+0.5*dx), dx, lastV[1])
            elif newV[1] > lastV[1]:
                dx = self.calcDx(newV, lastV)
                self.insert(lastV[1], (min(newV[0], lastV[0])+0.5*dx), dx, newV[1])
            if not newV[1] == firstV[1]:#mode 2: judge by the min and max function
                dx = self.calcDx(newV, firstV)
                self.insert(min(newV[1], firstV[1]), (min(newV[0], firstV[0])+0.5*dx), dx, max(newV[1], firstV[1]))
            if not lastV[1] == firstV[1]:
                dx = self.calcDx(lastV, firstV)
                self.insert(min(lastV[1], firstV[1]), (min(lastV[0], firstV[0])+0.5*dx), dx, max(lastV[1], firstV[1]))
        def generateAET(self, NET):
            
            miny = min(NET.edgeList.keys())
            
              
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.clear()

    def clear(self):
        self.vertexs = []
        self.NET = self.EdgeTable(self.canvas)
        self.AET = self.EdgeTable(self.canvas)

    def addPoint(self, x, y):
        print 'x:', x, ' y:', y
        if self.vertexs:
            self.lastVertex = self.vertexs[-1]
            if len(self.vertexs) >= 2:
                self.NET.updateN(self.lastVertex, [x, y], self.vertexs[0])
            #if len(self.vertexs) >= 3:
             #   self.NET.updateN(self.lastVertex, [x, y], self.vertexs[0])#TODOnext 
        else:           # the first point! and should not update the NET
            self.lastVertex = []
        self.vertexs.append([x,y])
        
        return self.lastVertex
    def close(self):
        return self.vertexs[-1], self.vertexs[0]

    def genAET(self):
        self.AET.generate(self.NET)

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

        self.vGroup = VertexGroup(self)
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
        self.vGroup.genAET()

    functions = {
        'nothing': doNothing,
        'dot': drawDot,
        'line': drawLine,
        'polygon': drawPolygon,
        'filledpolygon': fillPolygon,
        'twoDtrans': doNothing,
        'cut': doNothing,
        'animation': doNothing,
        }
    rightfunctions = {
        'polygon': closePolygon,
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
