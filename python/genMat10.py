import time
from csv import writer
import numpy as np
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
width = 240
height = 240

# Set Board
arduino = serial.Serial(port='COM3', baudrate=19200, timeout=.1)

#
image_mat = Image.new("RGBA", (width, height), (255, 255, 255, 0))
draw_mat = ImageDraw.Draw(image_mat)


#
# here are method calls to the window manager class
#
myapp.master.title("Presure Matress Application")
myapp.master.maxsize(245, 245)
myapp.master.minsize(245, 245)

w = Canvas(myapp, width=240, height=240)

height = 10
width = 10
firstContact = False

print("=== Program Let's start ====")

while True:
    inByte = arduino.readline()
    if firstContact:
        print("Initializing ...........")
        if inByte[0] == 'A':
            # arduino.clear      # clear the serial port buffer
            firstContact = True     # you've had first contact from the microcontroller
            arduino.write('A')       # ask for more

    else:
        # print("Running .............")
        res = inByte.decode(encoding='Ascii', errors='ignore')
        # print(inByte.decode(encoding='Ascii', errors='ignore'))

        arduino.write(b'A')

        data = res.split()

        dt = time.strftime('%H-%M-%S')

        # print(len(data))
        if len(data) == height*width:
            dat = np.array(data)
            x = dat.astype(int)
            b = np.flip(x, 0)
            data = b.tolist()

            # loop
            for i in range(height):  # Rows
                for j in range(width):  # Columns
                    print(data[(i*10)+j], end=' ')

                    if int(data[(i*10)+j]) > 230:
                        w.create_rectangle(9*j, 9*i, 9*(j+1), 9*(i+1), fill="red", outline="")
                        # draw_mat.rectangle(
                        #     [(9*j, 9*i), (9*(j+1), 9*(i+1))], fill="red", outline=None)
                    elif int(data[(i*10)+j]) > 90:
                        w.create_rectangle(9*j, 9*i, 9*(j+1), 9*(i+1), fill="orange", outline="")
                        # draw_mat.rectangle(
                        #     [(9*j, 9*i), (9*(j+1), 9*(i+1))], fill="orange", outline=None)
                    elif int(data[(i*10)+j]) > 100:
                        w.create_rectangle(9*j, 9*i, 9*(j+1), 9*(i+1), fill="yellow", outline="")
                        # draw_mat.rectangle(
                        #     [(9*j, 9*i), (9*(j+1), 9*(i+1))], fill="yellow", outline=None)
                    else:
                        # draw_mat.rectangle(
                        #     [(9*j, 9*i), (9*(j+1), 9*(i+1))], fill="#e6f5f6", outline=None)
                        w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')
                print('')
            print('')

            # if dt[6:8] == '00':
            #     # print(dt[6:8])
            #     image_mat.save('../../presure-matress-dashboard/static/temp/' +
            #                    str(dt)+'-test.gif', 'GIF', transparency=0)
            # image_mat.save(
            #     '../../presure-matress-dashboard/static/temp/test.gif', 'GIF', transparency=0)
            # time.sleep(5) # Sleep for 5 seconds

            w.pack()
            myapp.update()
        # if int(dt[6:8]) == 30:
        #     print(dt[6:8])
            # image_mat = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            # draw_mat = ImageDraw.Draw(image_mat)
            # image_mat.show()

# start the program
    myapp.mainloop()
