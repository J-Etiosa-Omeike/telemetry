import machine 
import math
from ustruct import pack 
from array import array 

# gain values, basically in order to increase precision, we can increase the gain of the output, but we might increase the noise
__gain__= {
        '0.88': (0 << 5, 0.73),
        '1.3':  (1 << 5, 0.92),
        '1.9':  (2 << 5, 1.22),
        '2.5':  (3 << 5, 1.52),
        '4.0':  (4 << 5, 2.27),
        '4.7':  (5 << 5, 2.56),
        '5.6':  (6 << 5, 3.03),
        '8.1':  (7 << 5, 4.35)
}

# corrections potentially unnecessary (idk)
xs=1
ys=1
xb=0
yb=0
scl = 10
sda = 12
gauss = "1.9"

data = array("B",[0] *6)
i2c = machine.SoftI2C(scl=machine.Pin(scl),sda=machine.Pin(sda), address = 0x1e, gauss='1.9', freq=15000)
reg_value, gain = __gain__[gauss]
declination = (-12 + 65 / 60) * math.pi / 180

def init(): 

    # initialize the I2C controller 
    # initialize sensor 
    i2c.start()
    # Configuration register A: (configure sampling and measurement)
    #   0bx11xxxxx  -> 8 samples averaged per measurement
    #   0bxxx100xx  -> 15 Hz, rate at which data is written to output registers
    #   0bxxxxxx00  -> Normal measurement mode
    i2c.writeto_mem(0x1e, 0x00, pack('B', 0b111000))

    # Configuration register B: (configure gain)
    
    i2c.writeto_mem(0x1e, 0x01, pack('B', reg_value))

    # Set mode register to continuous mode (otherwise the device will measure once and sleep)
    i2c.writeto_mem(0x1e, 0x02, pack('B', 0x00))
    i2c.stop()


def read(): 
    i2c.readfrom_mem_into(0x1e, 0x03, data)
    # reading and converting from twos complements
    x = (data[0] << 8) | data[1]
    y = (data[4] << 8) | data[5]
    z = (data[2] << 8) | data[3]
    
    x = x - (1 << 16) if x & (1 << 15) else x
    y = y - (1 << 16) if y & (1 << 15) else y
    z = z - (1 << 16) if z & (1 << 15) else z

    x = x * gain
    y = y * gain
    z = z * gain
    
    # Apply calibration corrections
    x = x * xs + xb
    y = y * ys + yb

    return x, y, z

init() 
while True: 
    x,y,z = read() 
    print(f"X:{x}, Y: {y}, Z: {z}")
