from tkinter import Frame, Canvas, Label, Text, Button, Entry, messagebox
from aquachaintk.toolbar import Toolbar, NoButton
from aquachaintk.vsframe import VSFrame

lorem='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

class ThemedFrame(Frame):
    def __init__(self, parent, app=None, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.app = app
        self._container = VSFrame(self)
        self.container = self._container.interior
        self._container.pack(side='top', fill='both', expand=True)
        # self._populate_dummybuttons(100)
    # def _populate_dummybuttons(self, lim):
    #     for i in range(lim):
    #         NoButton(text='a %d' % i).Btn(self.container).pack()

class StartPage(ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        ThemedLabel(self.container, text='lol StartPage').pack()
        ThemedLabel(self.container, text='lol cool').pack()

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
        ThemedLabel(self.container, text='lol PageWallets').pack()
        Button(self, text='Load Phrases', command=self.load_wallets).pack(side='right')
        Button(self, text='Generate New Phrase', command=self.keygen).pack(side='right')
        Button(self, text='Import Existing Phrase', command=self.getkey).pack(side='right')
        self.seedentry = Entry(self, text='')
        self.seedentry.pack(side='right')
        self.btnframe = Frame(self.container)
        self.btnframe.pack()

    def getkey(self):
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
        for i in self.app.keystore.listphrases():
            action = lambda x = i: self.unlockphrase(x)
            Button(self.container, text='unlock: ' + i.split(' ')[0], command=action).pack()

    def unlockphrase(self, phrase):
        print('unlock phrase')
        self.app.hdkeys.append(self.app.keystore.load_phrase(phrase, ''))
        self.reload()

    def reload(self):
        if self.app and hasattr(self.app, 'hdkeys'):
            for i in range(len(self.app.hdkeys)):
                for y in range(10):
                    address = self.app.keystore.from_parent_key(self.app.hdkeys[i], y)._key.public_key.address()
                    bal = self.app.aqua.getbalance(address)
                    fmt = '%s: %s'  % (address, bal)
                    action = lambda x = [i, y]: self.paywindow(x)
                    NoButton(text=fmt, command=action).Btn(self.btnframe).pack()


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
        Button(self.container, text='return', command=action).pack(side='left')
        Button(self.container, text='lock wallets', command=self.app.lock).pack(side='left')

        _dest = Entry(self.container, text='Destination Address')
        _val = Entry(self.container, text='Amount (in AQUA)')
        _gasprice = Entry(self.container, text='Gas Price (in GWEI)')

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



class PageSend(ThemedFrame):
    def __init__(self, app=None, *args, **kw):
        ThemedFrame.__init__(self, app=app, *args, **kw)
        ThemedLabel(self.container, text='lol cokdsfkdjsfdskfjol').pack()

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


class ThemedLabel(Label):
    def __init__(self, master=None, cnf={}, **kw):
        Label.__init__(self, master=master, cnf=cnf, **kw)
        self.configure(bg='black', fg='teal', font=('verdana', 8))
