import smbus
import time
 
__DEV_ADDR=0x10
 
 
bus=smbus.SMBus(1)
#bus.write_byte(__DEV_ADDR,__CMD_PWR_ON)
#bus.write_byte(__DEV_ADDR,__CMD_THRES2)
#time.sleep(0.2)
res=bus.read_word_data(__DEV_ADDR,0)
print res
#read_word_data
res=((res>>8)&0xff)|(res<<8)&0xff00
print res
