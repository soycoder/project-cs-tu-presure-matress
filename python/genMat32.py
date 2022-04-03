import tkinter as tk
from tkinter import *
import serial
# needs Python Image Library (PIL)
from PIL import Image, ImageDraw

import time
import numpy as np
import pandas as pd
from csv import writer
import pickle 

# ! (function) Get a predict
def get_posture(file_name):
    # ! Read Dataset and Re-format
    raw_data = pd.read_csv(file_name, header=None)

    raw_pressure = raw_data[0]
    index = raw_pressure.index
    number_of_rows = len(index)

    pressure = np.zeros((1,512), dtype=int)
    pressure = np.fromstring(str(raw_pressure[0][1:-1]), dtype=int, sep=' ')

    # load the model from disk
    loaded_model = pickle.load(open('../model/weight/knn_n3', 'rb'))
    result = loaded_model.predict([pressure])
    sum_ = np.sum(pressure)

    if sum_ < (254 * 5):
        result = [0]

    posture = ["Non","Supine","Right","Left"]

    return result[0]

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

# ! (#)  create the application
myapp = App()
width=240
height=480

# ! (#)  Set Board
arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

# ! (#) Set a canvas
image_mat = Image.new("RGBA", (width, height), (255, 255, 255, 0))
draw_mat = ImageDraw.Draw(image_mat)


#
# here are method calls to the window manager class
#
myapp.master.title("Presure Matress Application")
myapp.master.maxsize(245, 485)
myapp.master.minsize(245, 485)

w = Canvas(myapp, width=240, height=480)

# ! (#) Set size of sensor
height = 32
width = 16
firstContact = False

print("=== Program Let's start ====")

while True:
    inByte = arduino.readline()
    if firstContact: 
        print("Initializing ...........")
        if inByte[0] == 'A':
            # arduino.clear             # clear the serial port buffer
            firstContact = True;        # you've had first contact from the microcontroller
            arduino.write('A');         # ask for more
    
    else:
        # print("Running .............")
        res = inByte.decode(encoding='Ascii', errors='ignore')
        # print(inByte.decode(encoding='Ascii', errors='ignore'))

        arduino.write(b'A')

        data = res.split()

        datetime = time.strftime('%Y-%m-%d %H-%M-%S')
        date = time.strftime('%Y%m%d')
        dt = time.strftime('%H-%M-%S') 
        

        # print(len(data))
        if len(data) == height*width:
            dat = np.array(data)
            x = dat.astype(int)
            b = np.flip(x, 0)
            raw_data = b.tolist()

            # ! (#) Isolate part of raw data
            wrong_top = raw_data[0:width]                                                   # 0-15
            top = raw_data[width:int((height*width)/2)]                                     # 16-255
            wrong_bottom = raw_data[int((height*width)/2):int((height*width)/2)+width]      # 256-272
            bottom = raw_data[int((height*width)/2)+width:height*width]                     # 273-511

            _wrong_top = np.array(wrong_top)
            # ? (T) Top part
            _top = np.array(top)
            _top2d = _top.reshape(15,16)
                # ? Rotate
            _top2d = np.fliplr(_top2d)
            _top1d = _top2d.flatten()

            # ? (B) Bottom part
            _bottom = np.array(bottom)
            _bottom2d = _bottom.reshape(15,16)
                # ? Rotate
            _bottom2d = np.flipud(_bottom2d)
            _bottom2d = np.fliplr(_bottom2d)
            _bottom1d = _bottom2d.flatten()

            _wrong_bottom = np.array(wrong_bottom)


            # ? (Concatenate)
            data = np.concatenate((_wrong_top, _top1d))
            data = np.concatenate((data, _bottom1d))
            data = np.concatenate((data, _wrong_bottom))
            # print(len(data))

            # ! (Loop - Processing) 
            for i in range(height): #Rows
                for j in range(width): #Columns
                    # print(data[(i*16)+j] ,end=' ')

                    if int(data[(i*16)+j]) > 230:
                        # w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="red", outline="")
                        draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="red", outline=None)
                    elif int(data[(i*16)+j]) > 150:
                        # w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="orange", outline="")
                        draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="orange", outline=None)
                    elif int(data[(i*16)+j]) > 100:
                        # w.create_rectangle(15*j, 15*i, 15*(j+1), 15*(i+1), fill="yellow", outline="")
                        draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="yellow", outline=None)
                    else:
                        draw_mat.rectangle([(15*j, 15*i), (15*(j+1), 15*(i+1))], fill="#e6f5f6", outline=None)
                        # w.create_rectangle(50, 50, 100, 100, fill="red", outline = 'blue')     
                # print('')
            # print('')
            
            # ! (#) realtime data
            realtime_file_name = "../python/realtime.csv"
            with open(realtime_file_name, 'w', newline='') as write_obj2:
                # Create a writer object from csv module
                csv_writer = writer(write_obj2)
                # Add contents of list as last row in the csv file
                csv_writer.writerow([data])

            # ! (Save an image)
            image_mat.save('../../presure-matress-dashboard/static/temp/test.gif', 'GIF', transparency=0)
            
            # !! 
            if dt[6:8] == '00' or dt[6:8] == '10' or dt[6:8] == '20'or dt[6:8] == '30' or dt[6:8] == '40' or dt[6:8] == '50':
                # ! (Save an image history)
                # image_mat.save('../../presure-matress-dashboard/static/temp/'+str(dt)+'-test.gif', 'GIF', transparency=0)
                # ! (Collecting the data)
                file_name = "./history/history-" + date + ".csv"
                with open(file_name, 'a+', newline='') as write_obj:
                    # Create a writer object from csv module
                    csv_writer = writer(write_obj)
                    # Add contents of list as last row in the csv file
                    now_posture = get_posture(realtime_file_name)
                    if now_posture != 0:
                        csv_writer.writerow([datetime,data,now_posture])
            
            # time.sleep(5) # Sleep for 5 seconds

            # w.pack()
            # myapp.update()
        # image_mat.show()

# start the program            
# myapp.mainloop()