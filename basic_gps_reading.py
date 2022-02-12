from machine import Pin, UART, I2C 

import utime, time 

#gps UART connection
gps_module = UART(1, baudrate =9600, tx = Pin(12), rx = Pin (11))

# checking whether it is connected
print(gps_module)

while True: 
    print(str(gps_module.readlines())) # should just read out junk data 