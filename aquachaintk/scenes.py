#!/usr/bin/env python3
'''
scenes.py unique to this project
'''
from tkinter import Frame, Canvas, Text, messagebox
from aquachaintk.toolbar import Toolbar, NoButton
from aquachaintk.vsframe import VSFrame
from aquachaintk.themed import ThemedFrame, ThemedLabel, ThemedButton, ThemedEntry

import os
scriptDir = os.path.dirname(__file__)
LogoPath = os.path.join(scriptDir, 'aquachain.png')

lorem='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

class StartPage(ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        ThemedLabel(self.container, text='Aquachain TK', fontsize=24).pack()
        ThemedLabel(self.container, text='https://github.com/aquachain').pack()

class PageNone(ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        ThemedLabel(self.container, text='lol cool').pack()

class PageAbout(ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        infos = ['Learn more by going to our website.',
                lorem, '\n\n', lorem + lorem.replace('a', 'b'), '\n', lorem,
                '\n\n' + lorem + lorem.replace('a', 'b') + '\n']
        t = Text(self.container)
        t.insert('1.0', ''.join(infos))
        t.pack(side='top')

class PageWallets(ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        ThemedLabel(self.container, text='Aquachain Wallets').pack()
        self.brow1 = Frame(self, bg='black')

        self.brow2 = Frame(self, bg='black')
        self.brow2.pack(side='top', fill='x')

        ThemedLabel(self.container, text='Password for unlock phrase', fontsize=12).pack(side='top', fill='x')
        self.pwentry = ThemedEntry(self.container, show='*', fontsize=12)
        self.pwentry.pack(side='bottom', fill='x')
        if not app is None:
            ThemedButton(self.brow1, text='Lock Wallets', command=app.lock).pack(anchor='w', side='left')
        ThemedButton(self.brow1, text='Load Phrases', command=self.load_wallets).pack(anchor='w', side='left')
        ThemedButton(self.brow1, text='Generate New Phrase', command=self.keygen).pack(anchor='w', side='left')
        ThemedButton(self.brow1, text='Import Existing Phrase', command=self.get_phrase_entry).pack(anchor='w', side='left')
        self.brow1.pack(side='top', fill='x')
	
        self.seedentry = ThemedEntry(self.brow2, text='', fontsize=12)
        self.seedentry.pack(side='top', fill='x')
        self.btnframe = Frame(self.container)
        self.btnframe.pack()
        self.reload()

    def get_phrase_entry(self):
        phrase = self.seedentry.get().strip()
        l = len(phrase.strip().split(' '))
        try:
            valid = self.app.keystore.is_valid(phrase)
            if valid:
                self.app.keystore.save_phrase(phrase)
                messagebox.showinfo(message='Saved phrase')
        except ValueError as e:
            messagebox.showerror(message=f'{e}')

    def load_wallets(self):
        print('loading wallets')
        btnpack = Frame(self.container, background='aqua')
        btnpack.pack(side='top')
        column = -1
        row = 0
        for i in self.app.keystore.listphrases():
            column += 1
            if column > 3:
                column = 0
                row += 1
            action = lambda x = i: self.unlockphrase(x)
            ThemedButton(btnpack, text='unlock: ' + i.split(' ')[0], command=action).grid(column=column, row=row)

    def unlockphrase(self, phrase):
        print('unlock phrase')
        pw = self.pwentry.get()
        self.app.hdkeys.append(self.app.keystore.load_phrase(phrase, pw))
        self.reload()

    def reload(self):
        if self.app and hasattr(self.app, 'hdkeys'):
#            for i in self.btnframe.pack_slaves():
#                i.destroy()
            for i in range(len(self.app.hdkeys)):
                for y in range(10):
                    address = self.app.keystore.from_parent_key(self.app.hdkeys[i], y)._key.public_key.address()
                    bal = self.app.aqua.getbalance(address)
                    fmt = '%s: %s'  % (address, bal)
                    action = lambda x = [i, y]: self.paywindow(x)
                    NoButton(text=fmt, command=action).Btn(self.btnframe).pack(side='top')


    def keygen(self):
        phrase = self.app.aqua.generate_phrase()
        if messagebox.askyesno(title='Write this down', message=phrase):
            self.app.keystore.save_phrase(phrase)
            self.app.switch_frame(PageWallets)
    def paywindow(self, data):
        if len(data) != 2:
            print(fatal)
            quit()
        print('paying!')
        x = data[0]
        y = data[1]
        address = self.app.keystore.from_parent_key(self.app.hdkeys[x], y)._key.public_key.address()
        bal = self.app.aqua.getbalance(address)
        fmt = '%s: %s'  % (address, bal)
        for i in self.container.pack_slaves():
            i.destroy()
        ThemedLabel(self.container, text=fmt, font=('verdana', 24)).pack()
        action = lambda: self.app.switch_frame(PageWallets)
        ThemedButton(self.container, text='return', command=action).pack(side='left')
        ThemedButton(self.container, text='lock wallets', command=self.app.lock).pack(side='left')

        _dest = ThemedEntry(self.container, text='Destination Address')
        _val = ThemedEntry(self.container, text='Amount (in AQUA)')
        _gasprice = ThemedEntry(self.container, text='Gas Price (in GWEI)')

        ThemedLabel(self.container, text='Destination Address').pack(side='top')
        _dest.pack(side='top')
        ThemedLabel(self.container, text='Amount (in AQUA)').pack(side='top')
        _val.pack(side='top')
        ThemedLabel(self.container, text='Gas Price (in GWEI)').pack(side='top')
        _gasprice.pack(side='top')

        def getall():
            return [x, y, _dest.get().strip(), _val.get().strip(), _gasprice.get().strip()]
        NoButton(text='Send', command=self.pay, arg=getall).Btn(self.container).pack(side='top')

    def pay(self, args):
        data = args()
        x = data[0]
        y = data[1]
        checksum = self.app.aqua.checksum_encode
        fromacct = checksum(self.app.keystore.from_parent_key(self.app.hdkeys[x], y)._key.public_key.address())

        tx = {
            'from': fromacct,
            'nonce': self.app.aqua.getnonce(fromacct),
            'gas': 21000,
            'to': checksum(data[2]),
            'value': self.app.aqua.to_wei(data[3]),
            'gasPrice': self.app.aqua.to_wei(data[4], denom='gwei'),
        }

        # sign and send
        signed = self.app.aqua.sign_tx(self.app.keystore.from_parent_key(self.app.hdkeys[x], y)._key.to_hex(), tx)
        print('signed:', signed.hex())
        if messagebox.askokcancel(title=f'Send Transaction of {data[3]} AQUA?', message=f'{tx}'):
            tx_hash = self.app.aqua.send_raw_tx(signed)
            print(tx_hash)
            messagebox.showinfo(message=f'Sent: {tx_hash}')

class PageReceive (ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        self.btnframe = Frame(self.container)
        self.btnframe.pack()
        if self.app and hasattr(self.app, 'hdkeys'):
            for i in range(len(self.app.hdkeys)):
                for y in range(10):
                    address = self.app.keystore.from_parent_key(self.app.hdkeys[i], y)._key.public_key.address()
                    bal = self.app.aqua.getbalance(address)
                    fmt = '%s: %s'  % (address, bal)
                    action = lambda x = [i, y]: self.textarea(x)
                    NoButton(text=fmt, command=action).Btn(self.btnframe).pack()
    def textarea(self, data):
        if len(data) != 2:
            print(fatal)
            quit()
        print('recv!')
        x = data[0]
        y = data[1]
        address = self.app.keystore.from_parent_key(self.app.hdkeys[x], y)._key.public_key.address()
        bal = self.app.aqua.getbalance(address)
        fmt = '%s' % (address)
        for i in self.container.pack_slaves():
            i.destroy()

        t = Text(self.container, bg='black', fg='lime', font=('mono', 28))
        t.insert('1.0', fmt)
        t.pack()

if __name__ == '__main__':
    from aquachaintk.testapp import TestApplication
    win = TestApplication()
    win.switch_frame(StartPage)
    win.mainloop()
