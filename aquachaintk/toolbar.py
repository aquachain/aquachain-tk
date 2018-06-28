from tkinter import Frame, Label, Button

class NoButton:
    def __init__(self, text='foobtn', command=None, arg=None, relief='raised', font=('verdana', 8), width=0):
        self.text = text
        self.command= command
        self.arg=arg
        self.relief = relief
        self.font = font
        self.width = width
    def Btn(self, parent):
        if self.arg != None:
            def doit():
                command(arg)
        return self._newbutton(parent, self.text, self.command, self.arg, self.relief, self.font, self.width)
    def _newbutton(self, parent, text='', command=None, arg=None, relief='raised', font=None, width=0):
        if arg != None:
            def doit():
                command(arg)
            return Button(parent, command=doit, text=text, width=width, bg='black', fg='teal', font=font, relief=relief)
        else:
            return Button(parent, text=text,command=command, width=width, bg='black', fg='teal', font=font, relief=relief)


class Toolbar(Frame):
    def __init__(self, parent, app=None, logo=None, btns=[]):
        Frame.__init__(self, parent)
        print("building toolbar under parent:", parent)
        self.app = app
        self.configure(bg='black')
        Button(self, command=self.app.homepage, image=logo,bg='black').pack()
        for bwl in btns:
            if self.app._framename == bwl:
                btns[bwl]['relief'] = 'sunken'
            else:
                btns[bwl]['relief'] = 'raised'
            btns[bwl].pack()

        # self.grid()

    def addbtns(self,btns):
        for bwl in btns:
            bwl = btns[bwl].Btn(self)
            if self.app._framename == bwl:
                bwl['relief'] = 'sunken'
            else:
                bwl['relief'] = 'raised'
            bwl.pack()
