#-*- coding: utf-8 -*-
#! encoding:utf-8
from Tkinter import *
def initView(tk):
    tk.title("本来应该是non_Chinese，但是现在加了encoding就可以了")
    tk.minsize(800,500)
    tk.maxsize(1000,600)

class VertexGroup:
    def __init__(self):
        self.clear()

    def clear(self):
        self.vertexs = []
        #self.state = 'noPoint'

    def addPoint(self, x, y):
        if self.vertexs:
            self.lastVertex = self.vertexs[-1]
        else:
            self.lastVertex = []
        self.vertexs.append([x,y])
        return self.lastVertex

class Bresenham:
    def __init__(self, canvas):
        self.canvas = canvas
        

    def draw(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        
        
    
class Showing:
    def __init__(self, tk):
        self.root = tk
        self.show = Canvas(tk,bg="#fbf4f4",height=500,width=600)
        self.show.grid(row=0, rowspan = 100, column=1)#, columnspan = 2)
        self.show.bind('<Button-1>',self.press)

        self.color = "#222"
        self.fillcolor = "#259"
        self.state = 'nothing'

        self.vGroup = VertexGroup()
        self.forLine = Bresenham(self)
        
    def press(self, event):
        returnValue = self.functions[self.state](self, event)
                
    def drawPoint(self, x, y):
        self.show.create_line(x, y ,x+1 ,y+1 , fill=self.color)

    def doNothing(self, event):
        for i in range(-4,5):
            for j in range(-4,5):
                self.drawPoint(event.x+i, event.y+j)        

    def drawDot(self, event):
        self.drawPoint(event.x, event.y)
    
    def drawLine(self, event):
        firstV = self.vGroup.addPoint(event.x, event.y)
        if firstV:
            self.forLine.draw(firstV[0], firstV[1], event.x, event.y)
            self.vGroup.clear()


    functions = {
        'nothing': doNothing,
        'dot': drawDot,
        'line': drawLine,
        'polygon': doNothing,
        'filledpolygon': doNothing,
        'twoDtrans': doNothing,
        'cut': doNothing,
        'animation': doNothing,
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
