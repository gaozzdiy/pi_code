import math
import time
import Adafruit_MCP4725

dac = Adafruit_MCP4725.MCP4725(address=0x60)

i = 0
while True:
    val = (math.sin(i) + 1)*2048
    dac.set_voltage(int(val))
    i = i + 0.1
    #if i>4095 : i = 0
    #time.sleep(0.05)
    print("the val:" , i, val)

