import tkinter as tk

root = tk.Tk()


HEIGHT = 700
WIDTH = 800

Var301 = tk.IntVar()
Var501 = tk.IntVar()
Var601 = tk.IntVar()

VarP1 = tk.IntVar()
VarP2 = tk.IntVar()
VarP3 = tk.IntVar()
VarP4 = tk.IntVar()

VarStraightOut = tk.IntVar()
VarDoubleOut = tk.IntVar()
VarTripleOut = tk.IntVar()

VarMastersIn = tk.IntVar()
VarDoubleIn = tk.IntVar()


def Standard():
    C2.select()
    b2.select()
    a2.select()
    z1.select()

def c1u2():
    C1.deselect()
    C2.deselect()

def c2u3():
    C2.deselect()
    C3.deselect()

def c1u3():
    C1.deselect()
    C3.deselect()

def b1u2u3():
    b1.deselect()
    b2.deselect()
    b3.deselect()

def b2u3u4():
    b2.deselect()
    b3.deselect()
    b4.deselect()

def b1u3u4():
    b1.deselect()
    b3.deselect()
    b4.deselect()   

def b1u2u4():
    b1.deselect()
    b2.deselect()  
    b4.deselect()

def a1u2():
    a1.deselect()
    a2.deselect()

def a2u3():
    a2.deselect()
    a3.deselect()

def a1u3():
    a1.deselect()
    a3.deselect()

def z1():
    z1.deselect()

def z2():
    z2.deselect()




def nextPage():
    
    
    canvas1.destroy()
    
    canvas2 = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas2.pack()

    frame2 = tk.Frame(root, bg='#23ad99')   
    frame2.place(relx=0, rely=0,relwidth = 1, relheight=1)

    if (VarP1.get() == 1):
        labelp1 = tk.Label(root, text = "klappt")
        labelp1.pack()
    elif (VarP2.get() == 1):
        labelp2 = tk.Label(root, text = "funzt")
        labelp2.pack()
    elif (VarP3.get() == 1):
        labelp3 = tk.Label(root, text = "joa")
        labelp3.pack()
    elif (VarP4.get() == 1):
        labelp4 = tk.Label(root, text = "jup")
        labelp4.pack()
    else:
        labelp5 = tk.Label(root, text = int(VarP2))
        labelp5.pack()

    root.mainloop()



    

canvas1 = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas1.pack()

frame1 = tk.Frame(root, bg='#23ad99')
frame1.place(relx=0, rely=0,relwidth = 1, relheight=1)



C1 = tk.Checkbutton(frame1, text = "301", variable = Var301, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = c2u3)
C1.place(relwidth=0.1, relheight=0.1, rely=0.1, relx=0.2)

C2 = tk.Checkbutton(frame1, text = "501", variable = Var501, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = c1u3)
C2.place(relwidth=0.1, relheight=0.1, rely=0.1, relx=0.3)

C3 = tk.Checkbutton(frame1, text = "601", variable = Var601, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = c1u2)
C3.place(relwidth=0.1, relheight=0.1, rely=0.1, relx=0.4)

b1 = tk.Checkbutton(frame1, text = "1 Player", variable = VarP1, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = b2u3u4)
b1.place(relwidth=0.1, relheight=0.1, rely=0.3, relx=0.2)

b2 = tk.Checkbutton(frame1, text = "2 Player", variable = VarP2, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = b1u3u4)
b2.place(relwidth=0.1, relheight=0.1, rely=0.3, relx=0.3)

b3 = tk.Checkbutton(frame1, text = "3 Player", variable = VarP3, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = b1u2u4)
b3.place(relwidth=0.1, relheight=0.1, rely=0.3, relx=0.4)

b4 = tk.Checkbutton(frame1, text = "4 Player", variable = VarP4, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = b1u2u3)
b4.place(relwidth=0.1, relheight=0.1, rely=0.3, relx=0.5)

a1 = tk.Checkbutton(frame1, text = "Straight Out", variable = VarStraightOut, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = a2u3)
a1.place(relwidth=0.1, relheight=0.1, rely=0.5, relx=0.2)

a2 = tk.Checkbutton(frame1, text = "Double Out", variable = VarDoubleOut, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = a1u3)
a2.place(relwidth=0.1, relheight=0.1, rely=0.5, relx=0.35)

a3 = tk.Checkbutton(frame1, text = "Triple Out", variable = VarTripleOut, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = a1u2)
a3.place(relwidth=0.1, relheight=0.1, rely=0.5, relx=0.5)

z1 = tk.Checkbutton(frame1, text = "Double In", variable = VarDoubleIn, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = z2)
z1.place(relwidth=0.1, relheight=0.1, rely=0.7, relx=0.2)

z2 = tk.Checkbutton(frame1, text = "Masters In", variable = VarMastersIn, \
                 onvalue = 1, offvalue = 0, height=5, \
                 width = 20, bg='#23ad99', command = z1.deselect)
z2.place(relwidth=0.1, relheight=0.1, rely=0.7, relx=0.35)

Standard()

button = tk.Button(frame1, text="Next", command = nextPage)
button.place(relwidth=0.1, relheight=0.05, rely=0.9, relx=0.85)

#entry = tk.Entry(frame1,bg='red')
#entry.grid(row=3, column=9)

#label = tk.Label(frame1, text="A label", bg='cyan')
#label.grid(row=4, column=5)



















root.mainloop()