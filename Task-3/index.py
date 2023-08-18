
from tkinter import *
import random, string


root = Tk()
root.geometry("400x280")
root.title("Password Generator APP")

title = StringVar()
label = Label(root, textvariable=title).pack()
title.set("CHOOSE AN OPTION")


def selection():
    global selection
    selection = choice.get()



choice = IntVar()
R1 = Radiobutton(root, text="WEAK", variable=choice, value=1, command=selection).pack(anchor=CENTER)
R2 = Radiobutton(root, text="AVERAGE", variable=choice, value=2, command=selection).pack(anchor=CENTER)
R3 = Radiobutton(root, text="STRONG", variable=choice, value=3, command=selection).pack(anchor=CENTER)
labelchoice = Label(root)
labelchoice.pack()


lenlabel = StringVar()
lenlabel.set("Password length:")
lentitle = Label(root, textvariable=lenlabel).pack()


val = IntVar()
spinlenght = Spinbox(root, from_=4, to_=24, textvariable=val, width=13).pack()



def callback():
    lsum.config(text=passgen())



passgenButton = Button(root, text="Generate Password", bd=5, command=callback)
passgenButton.pack(pady=20)
password = str(callback)


lsum = Label(root, text="Password here", font=("arial", 20))
lsum.pack(side=BOTTOM, anchor="n")


poor= string.ascii_uppercase + string.ascii_lowercase
average= string.ascii_uppercase + string.ascii_lowercase + string.digits
symbols = """`~!@#$%^&*()_-+={}[]\|:;"'<>,.?/"""
advance = poor+ average + symbols


def passgen():
    if choice.get() == 1:
        return "".join(random.sample(poor, val.get()))
    elif choice.get() == 2:
        return "".join(random.sample(average, val.get()))
    elif choice.get() == 3:
        return "".join(random.sample(advance, val.get()))


root.mainloop()
