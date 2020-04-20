# -*- coding:utf-8 -*-
import serial
import time
ser = serial.Serial("/dev/ttyAMA0", 9600)  # 位置1
ser.flushInput()  # 位置2
ser.write("begin".encode("utf-8"))  # 位置3
def main():
    while True:
        count = ser.inWaiting()  # 位置4
        if count != 0:
            recv = ser.read(count)  # 位置5
            ser.write("Recv some data is : ".encode("utf-8"))  # 位置6
            ser.write(recv)  # 位置7
            ser.flushInput()
        time.sleep(0.1)  # 位置8
 
if __name__ == '__main__':
    main()

