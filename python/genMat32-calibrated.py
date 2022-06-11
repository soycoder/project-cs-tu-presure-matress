import tkinter as tk
from tkinter import *
import serial

import time
import numpy as np
import pandas as pd
from csv import writer
import pickle
import os


if not os.path.exists("images"):
    os.mkdir("images")

import plotly.express as px
import plotly.graph_objects as go

# ! Arduino Port
PORT = 'COM7'

# ! (function) Get a predict
def get_posture(dat):
    # ! Read Dataset and Re-format
    # raw_data = pd.read_csv(file_name, header=None)

    # raw_pressure = raw_data[0]
    # index = raw_pressure.index
    # number_of_rows = len(index)

    # pressure = np.zeros((1,512), dtype=int)
    # pressure = np.fromstring(str(raw_pressure[0][1:-1]), dtype=int, sep=' ')

    # load the model from disk
    loaded_model = pickle.load(open('../model/weight/knn_n3', 'rb'))
    result = loaded_model.predict([dat])
    sum_ = np.sum(dat)
    # print("SUM: " ,[sum_])
    if sum_ < 256:
        result = [0]

    posture = ["Non","Supine","Right","Left"]

    return result[0]


# ! (function) Save a Pressure Image 
def get_PressureImage(data, file_name):
    print("Saving a Pressure Image!", end='\t')

    dcolorsc = [
        [0.0, "rgb(255,255,255)"],
        [0.1111111111111111, "rgb(255,190,200)"],
        [0.2222222222222222, "rgb(255,140,150)"],
        [0.3333333333333333, "rgb(255,120,120)"],
        [0.4444444444444444, "rgb(255,100,100)"],
        [0.5555555555555555, "rgb(255,85,85)"],
        [0.6666666666666666, "rgb(255,70,70)"],
        [0.7777777777777777, "rgb(255,50,20)"],
        [0.888888888888888, "rgb(255,20,20)"],
        [1.0, "rgb(250,0,0)"]
    ]

    # heatmap = go.Heatmap(z=data, colorscale = dcolorsc, colorbar = dict(title="mmHg"))
    # fig2 = go.Figure(data=[heatmap])
    fig2 = go.Figure()
    fig2.add_trace(go.Heatmap(
        z=data,
        colorscale=dcolorsc,
        colorbar = dict(title="mmHg")))
    fig2.data[0].update(zmin=5, zmax=70)
    fig2.update_layout(width=300, height=400, margin=dict(l=10, r=10, b=10, t=10))
    fig2.update_yaxes(autorange="reversed")
    fig2.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    fig2.write_image("images/"+file_name)
    print("Complete!")

width=240
height=480

# ! (#)  Set Board
arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)

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
        if len(data) == (height*width)+1:
            _file = data[0]
            print('FILE -> ',end='')
            print(_file)
            data = data[1:len(data)]
            # print(data)
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

            # # weight = "1.0"
            # _range = "x1x5-y2y5"

            # x = _range.split("-")[0]
            # y = _range.split("-")[1]
            # # x - axis
            # x1 = int(x.split("x")[1])
            # x2 = int(x.split("x")[2])
            # # y - axis
            # y1 = int(y.split("y")[1])
            # y2 = int(y.split("y")[2])
            
            _data = np.zeros((height,width), dtype=float)

            if _file=='1':
                for yi in range(height):
                    for xi in range(width):
                        Pkl_Filename = "./calibrated_sensors/model/x"+str(xi)+"-y"+str(yi)+".pkl"
                        with open(Pkl_Filename, 'rb') as file:  
                            Pickled_LR_Model = pickle.load(file)
                        
                        # print("raw: ",data[(yi*16)+xi])
                        result = Pickled_LR_Model.predict([[data[(yi*16)+xi]]]) 
                        if result[0] < 0:
                            result[0] = 0
                        if yi == 0 or yi == 31:
                            result[0] = 0
                        # print("kg: ", result[0]/735.55914)
                        # print(int(result[0]) ,end="\t")
                        _data[yi][xi] = result[0]
                        # print("\t", end="")
                    # print()
                # print(_data)

                # ! (#) dataset collecting
                # dataset_file_name = "../python/dataset.csv"
                # with open(dataset_file_name, 'a+', newline='') as write_obj0:
                #     # Create a writer object from csv module
                #     csv_writer = writer(write_obj0)
                #     # Add contents of list as last row in the csv file
                #     data_1d = _data.flatten()
                #     # print(data_1d)
                #     # posture = { 1 : "Supine", 2 : "Right", 3 : "Left"}
                #     csv_writer.writerow([datetime, data_1d, 3])

                # ! (#) realtime data
                # realtime_file_name = "../python/realtime.csv"
                # with open(realtime_file_name, 'w', newline='') as write_obj2:
                #     # Create a writer object from csv module
                #     csv_writer = writer(write_obj2)
                #     # Add contents of list as last row in the csv file
                #     csv_writer.writerow([data])

                # ! (Save an image)
                get_PressureImage(data=_data,file_name="fig1.png")
                
                # !! 
                if dt[6:7] == '0' or dt[6:7] == '1' or dt[6:7] == '2'or dt[6:7] == '3' or dt[6:7] == '4' or dt[6:7] == '5':
                    # ! (Save an image history)
                    # image_mat.save('../../presure-matress-dashboard/static/temp/'+str(dt)+'-test.gif', 'GIF', transparency=0)
                    # ! (Collecting the data)
                    file_name = "./history/history-"+date+".csv"
                    with open(file_name, 'a+', newline='') as write_obj:
                        # Create a writer object from csv module
                        csv_writer = writer(write_obj)
                        # Add contents of list as last row in the csv file
                        data_1d = _data.flatten()
                        now_posture = get_posture(data_1d)
                        # print('>>>>> ', now_posture)
                        # if now_posture != 0:
                        csv_writer.writerow([datetime,data_1d,now_posture])

            # time.sleep(5) # Sleep for 5 seconds

            # w.pack()
            # myapp.update()
        # image_mat.show()

# start the program            
# myapp.mainloop()