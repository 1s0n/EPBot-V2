import time
import tkinter
from tkinter import Tk, Button, Label, Entry
from tkinter import messagebox
from tkinter import ttk

class funcs:
    # To raise an exception found on https://stackoverflow.com/questions/8294618/define-a-lambda-expression-that-raises-an-exception
    scanfunc = lambda : (_ for _ in ()).throw(NotImplemented("scanfun() is not implemented!"))
    exitfunc = lambda : (_ for _ in ()).throw(NotImplemented("exitfunc() is not implemented!"))
    readingfunc = lambda : (_ for _ in ()).throw(NotImplemented("readingfunc() is not implemented!"))
    writingfunc = lambda : (_ for _ in ()).throw(NotImplemented("writingfunc() is not implemented!"))

def getLogin():
    window = Tk()
    window.geometry("350x500")
    window.title("EPBot Login")

    window.config(bg='lightgray')

    lab=Label(window,text='Education Perfect Login',bg='white')
    font=('Consolas',18)
    lab.config(font=font, bg="lightgray")
    lab.place(x=20,y=80)
    lab=Label(window,text='  This window remembers your password for future logins, \nchange user by loging out via the main window after login.\nAuto login won\' work if central server is offline!',bg='white')
    font=('Consolas',8)
    lab.config(font=font, bg="lightgray")
    lab.place(x=0,y=120)

    l1=Label(window,text='Email',bg='white')
    l=('Consolas',13)
    l1.config(font=l, bg="lightgray")
    l1.place(x=80,y=200)

    #e1 entry for username entry
    e1=Entry(window,width=20,border=0)

    e1.config(font=l)
    e1.place(x=80,y=230)

    #e2 entry for password entry
    e2=Entry(window,width=20,border=0,show='*')
    e2.config(font=l)
    e2.place(x=80,y=310)


    l2=Label(window,text='Password',bg='white')

    l2.config(font=l, bg="lightgray")
    l2.place(x=80,y=280)

    email = None
    password = None

    def cmd():
        nonlocal email, password
        email = e1.get()
        password = e2.get()
        # print(email)
        # print(password)
        window.destroy()

    #Button_with hover effect
    def bttn(x,y,text,ecolor,lcolor):
        def on_entera(e):
            myButton1['background'] = ecolor #ffcc66
            myButton1['foreground']= lcolor  #000d33

        def on_leavea(e):
            myButton1['background'] = lcolor
            myButton1['foreground']= ecolor

        myButton1 = Button(window,text=text,
                    width=20,
                    height=2,
                    fg=ecolor,
                    border=0,
                    bg=lcolor,
                    activeforeground=lcolor,
                    activebackground=ecolor,
                        command=cmd)
                    
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)



    bttn(100,375,'S T A R T','white','#994422')


    window.mainloop()
    return email, password

import threading
import os

LARGEFONT = ("Verdana", 20)
font2 = ("Verdana", 12)
class ChoosePage(tkinter.Frame):
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent, width=500)
        
        self.controller = controller

        # label of frame Layout 2
        label = ttk.Label(self, text ="Go to the page with the vocab list\nand click scan", font = LARGEFONT)
        label.place(x=5, y=10)

        label2 = ttk.Label(self, text ="Note: This only works with tasks with vocab lists.", font = font2)
        label2.place(x=5, y=80)
        # putting the grid in its place by using
        # grid
        #label.grid(row = 0, column = 4, padx = 0, pady = 10)
  
        button1 = ttk.Button(self, text ="Scan",
        command = self.ScanFunc)

        # putting the button in its place by
        # using grid
        button1.place(y=110, x=10)

    def ScanFunc(self):
        funcs.scanfunc()
        self.controller.show_frame(MainPage)

# second window frame page1
class MainPage(tkinter.Frame):
     
    def __init__(self, parent, controller):
         
        tkinter.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Education Perfect Bot\n     Control panel", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Reading",
                            command = self.reading)
     
        # putting the button in its place
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text ="Writing",
                            command = self.writing)
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

    def reading(self):
        funcs.readingfunc()

    def writing(self):
        funcs.writingfunc()

import sys

class MainApp(threading.Thread):

    def __init__(self, exitfunc=sys.exit):
        threading.Thread.__init__(self)
        self.start()
        self.onexit = exitfunc

    def callback(self):
        self.window.quit()
        self.onexit()
        # os._exit(0)

    def run(self):
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.callback)

        self.window.geometry("500x800")
        self.window.title("Education Perfect Bot")

        container = tkinter.Frame(self.window) 
        container.pack(side = "top", fill = "both", expand = True)

        self.frames = {} 

        for F in (MainPage, ChoosePage):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        # self.show_frame(StartPage)

        self.window.mainloop()
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Debug
def onexit():
    os._exit(0)

def fakescan():
    pass

def faker():
    print("Doing reading...")

def fakew():
    print("Doing writing...")


if __name__ == "__main__":
    funcs.scanfunc = fakescan
    funcs.readingfunc = faker
    funcs.writingfunc = fakew

    app = MainApp(exitfunc=onexit)

    while True:
        time.sleep(10)
