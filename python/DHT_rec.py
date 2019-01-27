import time

import Adafruit_DHT
from bmp180.BMP180 import BMP180

sensor = Adafruit_DHT.DHT22
sensor_bmp = BMP180()

pin = 4
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
if humidity is not None and temperature is not None:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    chk_time=time.strftime("%Y-%m-%d %H:%M", time.localtime())
    print('{0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(chk_time, temperature, humidity))
    rec_line='{0}  Temp={1:0.1f}*C  Humidity={2:0.1f}%'.format(chk_time, temperature, humidity)
    fileHandle = open ( '/data/record/DHT_temp_humidity_rec.txt', 'a' )
    fileHandle.write(rec_line)
    fileHandle.close
