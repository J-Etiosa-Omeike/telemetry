from machine import Pin, UART, I2C

from micropyGPS import MicropyGPS

#Import utime library to implement delay
import utime, time

gps_decoder = MicropyGPS()

#GPS Module UART Connection
gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

#print gps module connection details
print(gps_module)

#Used to Store NMEA Sentences
buff = bytearray(255)

TIMEOUT = False

#store the status of satellite is fixed or not
FIX_STATUS = False


while True:
    
    gps_module.readline()
    buff = str(gps_module.readline())
    print(buff)
    for x in buff: 
        gps_decoder.update(x)
    print("Latitude" + gps_decoder.latitude_string())
    print("Longitude" + gps_decoder.longitude_string())

    utime.sleep_ms(500)