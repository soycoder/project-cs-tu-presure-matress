import serial

import time
import numpy as np
import pandas as pd
from csv import writer

import pickle

# ! (#)  Set Board
arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)


# ! (#) Set size of sensor
height = 32
width = 16
firstContact = False

print("=== Program Let's start ====")

_data = np.zeros((height,width), dtype=float)
# print(_data.shape)

def matRotateSetup(dat):
    x = dat
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

    return data

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
            dat = dat.astype(float)
            data = matRotateSetup(dat)

            # weight = "1.0"
            # _range = "x1x5-y2y5"
            _range = "x0x15-y0y31"
            # while True:
            #     _range = input("Enter range (Current) : ")
            #     if _range.startswith("x"):
            #         break

            # str_weight_type = input('Enter weight (Current) : ')
            str_weight_type = ""
            str_weight = ""
            if str_weight_type == "0.0":
                str_weight = "0.0"
            elif str_weight_type[-3:] == "box":
                str_weight = str_weight_type.split("-")[0]

            x = _range.split("-")[0]
            y = _range.split("-")[1]
            # x - axis
            x1 = int(x.split("x")[1])
            x2 = int(x.split("x")[2])
            # y - axis
            y1 = int(y.split("y")[1])
            y2 = int(y.split("y")[2])


            areaSensorSize = np.zeros(height*width, dtype=float)
            # area_X = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
            # area_Y = [1.0,1.5,1.0,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.5,1.0,1.0,1.0,1.0]
            # for yi in range(height):
            #     for xi in range(width):
            #         print((yi*16)+xi, end=' ')
            #         areaSensorSize[(yi*16)+xi] = area_Y[yi] * area_X[xi]
            #     print()
            areaSensorSize = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]
            areaSensorSize = matRotateSetup(areaSensorSize)
            
            # for yi in range(height):
            #     for xi in range(width):
            #         print(areaSensorSize[(yi*16)+xi] , end=' ')
            #     print()

            if str_weight_type == '':
                for yi in range(y1,y2+1):
                    for xi in range(x1,x2+1):
                        # print(yi, xi,end='')
                        _data[yi][xi] = data[(yi*16)+xi]
                    # print()
                    
                pass
            elif (str_weight == '0.0' or str_weight == '3.0' or str_weight == '6.0' or str_weight == '9.0'):
                for yi in range(y1,y2+1):
                    for xi in range(x1,x2+1):
                        # print(yi, xi,end='')
                        data[(yi*16)+xi] = _data[yi][xi]
                    # print()

                # ! (1) Fisrt Data : ไม่มีการปรับค่า
                first_file_name = "../python/calibrating_file/withBoxFinal/nonConvert-"+str_weight+"kg.csv"
                with open(first_file_name, 'a+', newline='') as write_obj2:
                    # Create a writer object from csv module
                    csv_writer = writer(write_obj2)
                    # Add contents of list as last row in the csv file
                    csv_writer.writerow([data])       
            
            if _file=='1' and str_weight_type == '':
                
                for yi in range(height):
                    for xi in range(width):
                        # print(yi, xi,end=' ')
                        print(_data[yi][xi], end='\t')
                    print()

            # elif _file=='2':
            #     # print(data)
            #     # ! 2) Second Data : มีการปรับค่า ตามสเกล
            #     first_file_name = "../python/calibrating_file/setWithoutBaseBox/convertScale-"+_range+"-"+str_weight+"kg"+_type+".csv"
            #     with open(first_file_name, 'a+', newline='') as write_obj2:
            #         # Create a writer object from csv module
            #         csv_writer = writer(write_obj2)
            #         # Add contents of list as last row in the csv file
            #         csv_writer.writerow([data])

            # time.sleep(5) # Sleep for 5 seconds

            # w.pack()
            # myapp.update()
        # image_mat.show()

# start the program            
# myapp.mainloop()