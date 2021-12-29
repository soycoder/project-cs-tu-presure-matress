import tkinter as tk
from tkinter import *
import serial
# needs Python Image Library (PIL)
from PIL import Image, ImageDraw

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# create the application
myapp = App()
width=160
height=480

# Set Board
arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

#
image_mat = Image.new("RGB", (width, height), (255, 255, 255))
draw_mat = ImageDraw.Draw(image_mat)


#
# here are method calls to the window manager class
#
myapp.master.title("Presure Matress Application")
myapp.master.maxsize(245, 485)
myapp.master.minsize(245, 485)

w = Canvas(myapp, width=240, height=480)

height = 16
width = 16
firstContact = False

while True:
    inByte = arduino.readline()
    if firstContact: 
        if inByte[0] == 'A':
            # arduino.clea      # clear the serial port buffer
            firstContact = True;     # you've had first contact from the microcontroller
            arduino.write('A');       # ask for more
    
    else:
        res = inByte.decode(encoding='Ascii', errors='ignore')
        # print(inByte.decode(encoding='Ascii', errors='ignore'))
        arduino.write(b'A')

        data = res.split()
        # print(len(data))
        if len(data) == height*width:
            for i in range(height): #Rows
                for j in range(width): #Columns
                    # print(data[(i*16)+j] ,end=' ')

                    if int(data[(i*16)+j]) > 230:
                        w.create_rectangle(15*j, 30*i, 15*(j+1), 30*(i+1), fill="red", outline = 'red')
                    elif int(data[(i*16)+j]) > 200:
                        w.create_rectangle(15*j, 30*i, 15*(j+1), 30*(i+1), fill="orange", outline = 'red')
                    elif int(data[(i*16)+j]) > 120:
                        w.create_rectangle(15*j, 30*i, 15*(j+1), 30*(i+1), fill="yellow", outline = 'red')
                    else:
                        w.create_rectangle(15*j, 30*i, 15*(j+1), 30*(i+1), fill="gray", outline = 'red')
                        # w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')     
            #     print('')
            # print('')

            w.pack()
            myapp.update()
#     draw_mat.rectangle()
# filename = "mat.jpg"
# image_mat.save(filename)

# start the program            
myapp.mainloop()