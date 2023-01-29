import serial

import time
import numpy as np
import pandas as pd
from csv import writer
import pickle
import os

if not os.path.exists("images"):
    os.mkdir("images")

import plotly.graph_objects as go

# ! Arduino Port
PORT = 'COM3'

# ! (function) Get a predict
def get_posture(dat):
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

width=480
height=480

# ! (#)  Set Board
arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)

# ! (#) Set size of sensor
height = 10
width = 10
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


            
            _data = np.zeros((height,width), dtype=float)

            if _file=='1':
                for yi in range(height):
                    for xi in range(width):
                        Pkl_Filename = "./calibrated_sensors/model/x"+str(xi)+"-y"+str(yi)+".pkl"
                        with open(Pkl_Filename, 'rb') as file:  
                            Pickled_LR_Model = pickle.load(file)
                        
                        # print("raw: ",data[(yi*10)+xi])
                        result = Pickled_LR_Model.predict([[data[(yi*10)+xi]]]) 
                        if result[0] < 0:
                            result[0] = 0
                        if yi == 0 or yi == 9:
                            result[0] = 0
                        _data[yi][xi] = result[0]


                # ! (Save an image)
                get_PressureImage(data=_data,file_name="fig1.png")
                
                # !! 
                if dt[6:7] == '0' or dt[6:7] == '1' or dt[6:7] == '2'or dt[6:7] == '3' or dt[6:7] == '4' or dt[6:7] == '5':
                    # ! (Collecting the data)
                    file_name = "./history/dataset.csv"
                    with open(file_name, 'a+', newline='') as write_obj:
                        # Create a writer object from csv module
                        csv_writer = writer(write_obj)
                        # Add contents of list as last row in the csv file
                        data_1d = _data.flatten()
                        # now_posture = get_posture(data_1d)
                        # print('>>>>> ', now_posture)
                        # if now_posture != 0:
                        csv_writer.writerow([datetime,data_1d,"0"])