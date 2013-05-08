#-*- coding: utf-8 -*-
#! encoding:utf-8
from Tkinter import *
def initView(tk):
    tk.title("本来应该是non_Chinese，但是现在加了encoding就可以了")
    tk.minsize(800,500)
    tk.maxsize(1000,600)
    
class Showing:
    def __init__(self, tk):
        self.root = tk
        self.show = Canvas(tk,bg="#fbf4f4",height=500,width=600)
        self.show.grid(row=0, rowspan = 100, column=1)#, columnspan = 2)
        self.show.bind('<Button-1>',self.press)

        self.color = "#222"
        self.state = 'nothing'
        
    def drawPoint(self, x, y):
        self.show.create_line(x, y ,x+1 ,y+1 , fill=self.color)

    def press(self, event):
        returnValue = self.functions[self.state](self, event)
        
    def doNothing(self, event):
        for i in range(-4,5):
            for j in range(-4,5):
                self.drawPoint(event.x+i, event.y+j)        

    def drawDot(self, event):
        self.drawPoint(event.x, event.y)
    
    def drawLine(self, event):
        self.show.create_line(0,10,event.x,event.y,fill=self.color)


    functions = {
        'nothing': doNothing,
        'dot': drawDot,
        'line': drawLine,
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

        self.byeB = Button(tk,text="说Bye!",command = tk.quit, width = 20, height=2, bg = self.nowcolor)
        self.byeB.grid(row=90,column=0, sticky=N)

        self.buttons = {
            'dot': self.dotB,
            'line': self.lineB,
            
            'bye': self.byeB,
            }    

    def dot(self):
        self.target.state = 'dot'
        self.setFocus()
        
    def line(self):
        self.target.state = 'line'
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
