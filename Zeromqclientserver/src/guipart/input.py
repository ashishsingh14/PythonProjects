
from Tkinter import *;
import tkMessageBox

def sendtoserver():
    tkMessageBox.showinfo( "Hello Python", "Hello World")

def create():
    root = Tk()
    S = Scrollbar(root)
    T = Text(root)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(END, "Just a text Widget\nin two lines\n")
    B = Button(root, text ="Send", command = sendtoserver)
    B.pack()
    mainloop()
    

if __name__ == '__main__':
    create()