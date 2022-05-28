from tkinter import Tk, Button, Label, Entry
from tkinter import messagebox

window = Tk()
window.geometry("350x500")
window.title("EPBot Login")

window.config(bg='lightgray')

lab=Label(window,text='Education Perfect Login',bg='white')
font=('Consolas',18)
lab.config(font=font, bg="lightgray")
lab.place(x=20,y=80)
lab=Label(window,text='  This window remembers your password for future logins, \nchange user by loging out via the main window after login.',bg='white')
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
    email = e1.get()
    password = e2.get()
    print(email)
    print(password)

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