import numpy as np

strr = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,166,166,171,200,0,0,0,0,0,0,0,0,0,0,167,0,254,243,245,252,176,0,0,0,0,0,0,0,0,0,0,0,163,187,179,169,0,0,0,0,0,0,0,0,0,164,0,0,183,241,197,184,0,0,0,0,0,0,0,0,0,178,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,157,174,0,252,254,254,243,194,0,0,0,0,0,0,0,0,0,155,0,216,225,247,216,179,0,0,0,0,0,0,0,0,0,0,0,220,210,183,182,153,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,254,0,0,0,0,207,0,0,0,0,0,0,0,0,0,226,170,0,0,0,0,211,0,0,0,0,0,0,0,0,0,184,0,0,0,0,0,160,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,188,0,0,0,0,201,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'

data = np.fromstring(strr, dtype=int, sep=',')

# a=np.load('test.npy')
# b=np.flip(a, 0)
# print(a)
# print(b)

# data = b.tolist()
print(data)

import tkinter as tk
from tkinter import *
# needs Python Image Library (PIL)
from PIL import Image, ImageDraw

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

import time 

# create the application
myapp = App()
width=240
height=480

#
image_mat = Image.new("RGBA", (width, height), (255, 255, 255, 0))
draw_mat = ImageDraw.Draw(image_mat)

#
# here are method calls to the window manager class
#
myapp.master.title("Presure Matress Application")
# myapp.master.maxsize(245+10, 485+10)
myapp.master.minsize(245, 485)

w = Canvas(myapp, width=240, height=480)

height = 32
width = 16

while True:
    for i in range(height): #Rows
        for j in range(width): #Columns

            if int(data[(i*16)+j]) > 230:
                w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="red", outline="red")
                w.create_text((15*j)+5,(15*i)+5,fill="black",font="Times 6 bold", text=str((i*16)+j))
                # draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="red", outline="red")
            elif int(data[(i*16)+j]) > 200:
                w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="orange", outline="red")
                w.create_text((15*j)+5,(15*i)+5,fill="black",font="Times 6 bold", text=str((i*16)+j))
                # draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="orange", outline="red")
            elif int(data[(i*16)+j]) > 120:
                w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="yellow", outline="red")
                w.create_text((15*j)+5,(15*i)+5,fill="black",font="Times 6 bold", text=str((i*16)+j))
                # draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="yellow", outline="red")
            else:
                w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="gray", outline="red")
                w.create_text((15*j)+5,(15*i)+5,fill="black",font="Times 6 bold", text=str((i*16)+j))
                # w.create_rectangle(50, 50, 100, 100, fill="gray", outline="red")     
    #     print('')
    # print('')
    
            

    w.pack()
    myapp.update()
    # break

# image_mat.save('test.gif', 'GIF', transparency=0)
# image_mat.show()

# start the program            
myapp.mainloop()
# exit()