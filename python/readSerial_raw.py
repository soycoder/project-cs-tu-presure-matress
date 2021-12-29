import serial

serialPort = serial.Serial("COM7", 115200)
if not serialPort.isOpen():
    serialPort.open()
print('com3 is open', serialPort.isOpen())



serialString = ""                           # Used to hold data coming over UART


while(1):
    
    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        print(serialString.decode('Ascii'))

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        serialPort.write(b"Thank you for sending data \r\n")