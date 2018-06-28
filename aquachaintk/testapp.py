#!/usr/bin/env python3
from aquachain.aquakeys import Keystore
from aquachain.aquatool import AquaTool
from tkinter import Frame
from tkinter import IntVar, Tk, PhotoImage
from aquachaintk.toolbar import Toolbar, NoButton
from aquachaintk.scenes import StartPage, ThemedFrame, LogoPath
from aquachaintk.scenes import PageNone, PageAbout, PageReceive, PageWallets
import os
LogoPath = os.path.join(os.path.dirname(__file__), 'aquachain.png')
class TestApplication(Tk):
    def __init__(self):
        Tk.__init__(self)

        # self.wm_geometry(newGeometry='800x400-100+100')
        self.version = 'Aquachain TK v0.0.3'
        self.configure(background='black')
        self.logo = PhotoImage(file=LogoPath)
        self.head_difficulty = IntVar()
        self.head_number = IntVar()
        self.head_timing = IntVar()
        self.head_timestamp = IntVar()
        self.total_supply = IntVar()

        self.head_difficulty.set(0)
        self.head_number.set(0)
        self.head_timing.set(0)
        self.head_timestamp.set(0)
        self.total_supply.set(0)

        # connect to aquachain node
        self.aqua = None
        self.aqua = AquaTool(rpchost='https://c.onical.org')

        # get latest block from aquachain node
        self.head = self.aqua.gethead()

        # keys
        self.keystore = Keystore()
        self.hdkeys = []
        self.addresses = []

        # TK
        self._mainframe = Frame(self, background='green')
        self._mainframe.pack(side='top', anchor='n', expand=True, fill='both')
        self._framename = ''


        self.buttons = btns = {
            'Quit': NoButton(text='Quit',
                command=self.quit, width=13),
            'Lock': NoButton(text='Lock',
                command=self.lock, width=13),
            'PageWallets': NoButton(text='Wallets',
                command=self.switch_frame, arg=PageWallets, width=13),
            'PageAbout': NoButton(text='About',
                command=self.switch_frame, arg=PageAbout, width=13),
            'PageAbout': NoButton(text='Recv',
                command=self.switch_frame, arg=PageReceive, width=13),
        }
        self._toolbar = Toolbar(self._mainframe, app=self, logo=self.logo)
        self._toolbar.addbtns(btns)
        self._toolbar.grid(sticky='nw', columnspan=1, column=0, row=0)

        # take it away
        # self._leftcol = Frame(self, background='blue')
        self._frame = ThemedFrame(self._mainframe, app=self, background='teal', height='100')

        self.homepage()
    def quit(self):
        quit()
    def lock(self):
        quit()
    def homepage(self):
        # self.switch_frame(/StartPage)
        self.switch_frame(StartPage)
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        self._framename = frame_class.__name__
        new_frame = frame_class(parent=self._mainframe,app=self)
        if self._frame is not None:
            print('deleting:',self._frame)
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(sticky='ne',ipadx=100, column=1, row=0)
        print('switchin to framename:', self._framename)


if __name__ == '__main__':
    win = TestApplication()
    win.switch_frame(StartPage)
    win.mainloop()
