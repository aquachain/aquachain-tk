#!/usr/bin/env python3
from aquachain.aquakeys import Keystore
from aquachain.aquatool import AquaTool
from tkinter import IntVar, Tk
class TestApplication(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.homepage = ''
        self.logo = None
        self.aqua = AquaTool(rpchost='https://c.onical.org')
        self._framename = ''
        self.head_number = IntVar()
        self.head_difficulty = IntVar()
        self.head_timing = IntVar()
        self.total_supply = IntVar()
        self.version = ''
        self.keystore = Keystore(directory='lolbadkeys')
        self.hdkeys = []
        self._frame = None
    def quit(self):
        quit()
    def lock(self):
        quit()
    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        self._framename = frame_class.__name__
        new_frame = frame_class(parent=self._mainframe,app=self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)
        print('switchin to framename:', self._framename)
