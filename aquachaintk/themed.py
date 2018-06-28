#!/usr/bin/env python3
'''
re-usable themed.py
aerth waz here
'''

from tkinter import Frame, Label, Button, Entry
from aquachaintk.vsframe import VSFrame

class ThemedFrame(Frame):
    def __init__(self, parent, noscrollbox=False, app=None, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.configure(bg='black')
        self.app = app
        if not noscrollbox:
            self._container = VSFrame(self, background='black')
            self.container = self._container.interior
            self._container.pack(side='top', fill='both', expand=True)
    def clean_container(self):
        for i in self.container.pack_slaves():
            i.destroy()

        # self._populate_dummybuttons(100)
    # def _populate_dummybuttons(self, lim):
    #     for i in range(lim):
    #         NoButton(text='a %d' % i).Btn(self.container).pack()
class HorizontalRow(Frame):
    def __init__(self, parent, height=2, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.configure(bg='white', width=100, height=height)

class ThemedLabel(Label):
    def __init__(self, master=None, fontsize=8, cnf={}, **kw):
        Label.__init__(self, master=master, cnf=cnf, **kw)
        self.configure(bg='black', fg='teal', font=('verdana', fontsize))

class ThemedButton(Button):
    def __init__(self, master=None, fontsize=8, cnf={}, **kw):
        Button.__init__(self, master=master, cnf=cnf, **kw)
        self.configure(bg='black', fg='teal', font=('verdana', fontsize))

class ThemedEntry(Entry):
    def __init__(self, master=None, fontsize=8, cnf={}, **kw):
        Entry.__init__(self, master=master, cnf=cnf, **kw)
        self.configure(bg='black', fg='teal', font=('verdana', fontsize))

if __name__ == '__main__':
    from tkinter import Tk, Button, messagebox
    win = Tk()
    frame = ThemedFrame(win, noscrollbox=True)
    frame.pack(side='top', fill='both', expand=True)
    ThemedLabel(frame, text=f'This works!', fontsize=24).pack()
    for i in range(4):
        HorizontalRow(frame).pack(padx=10, pady=10)
        ThemedLabel(frame, text=f'Entry #{i}').pack()
        e = ThemedEntry(frame)
        e.pack()
        def action(e=e):
            s = e.get()
            messagebox.showinfo(message=s)
        ThemedButton(frame, command=action, text=f'btn #{i}').pack()
    win.mainloop()
