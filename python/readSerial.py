# Importing Libraries
from tkinter.constants import FALSE
import serial
import time

# Declare variable
ROWS = 10
COLS = 10
mat_size = ROWS * COLS

#  The serial port
arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
serialInArray = [0] * mat_size
serialCount = 0
firstContact = False
    
while True:
    inByte = arduino.readline()
    # print(inByte.decode(encoding='Ascii', errors='ignore'))

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
        if len(data) == 100:
            print(data)
            size = 10
            for c in range(size):
                for r in range(size):
                    print(data[(c*size)+r] ,end=' ')
                print('')


        # # Add the latest byte from the serial port to array:
        
        # serialInArray[serialCount] = inByte
        # serialCount = serialCount + 1

        # # If we have 3 bytes:
        # if (serialCount > 10 ):
        #     # print(millis()-tiempoant)
        #     # tiempoant = millis()
      
        #     render = 1
        #     for i in range(10):
        #         res = serialInArray[i]
        #         if res != "":
        #             print(serialInArray[i])

        #     #  Send a capital A to request new sensor readings:
        #     arduino.write(b'A')
        #     #  Reset serialCount:
        #     serialCount = 0
    

