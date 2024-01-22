#
#           main.py
#
#           by Hulupus
#

import pycom as p
from network import Sigfox
from machine import Pin, I2C
import socket
import time


# Initialize I2C Bus
i2c = I2C(0)
i2c.init(I2C.MASTER, baudrate=200000)

## LED Blink with Lopy
p.heartbeat(False)
p.rgbled(0xFF0000)  ## Rot
time.sleep(1)
p.rgbled(0x00FF00)  ## Grün
time.sleep(1)
p.rgbled(0xFF0000)  ## Rot
time.sleep(1)
p.rgbled(0x000000)  ## Schwarz

# LED Blink with Sensors
i2c.writeto(0x66, "L,0")
time.sleep(0.3)
i2c.writeto(0x66, "L,1")
i2c.writeto(0x64, "L,0")
time.sleep(0.3)
i2c.writeto(0x64, "L,1")
i2c.writeto(0x63, "L,0")
time.sleep(0.3)
i2c.writeto(0x63, "L,1")
time.sleep(0.3)

# Initialize Sigfox
# Sigfox is censored


# Convert from bytestring to dezimal
def convert(bytestring):
    try:
        string = bytestring.decode("utf-8")
    except UnicodeError:
        return 0
    cleansed_string = "".join(c for c in string if c.isdigit() or c == ".")
    dezimal = float(cleansed_string)
    return dezimal


# Mainloop
while True:
    # Read temperature
    i2c.writeto(0x66, "R")
    time.sleep(0.7)
    temp_temperatur = convert(i2c.readfrom(0x66, 8))
    c01_hb = int(((temp_temperatur + 26) * 900) / 256)
    c01_lb = int(((temp_temperatur + 26) * 900) - 256 * c01_hb)

    # Read electric conductivity
    i2c.writeto(0x64, "R")
    time.sleep(0.7)
    temp_ec = convert(i2c.readfrom(0x64, 5))
    c02_hb = int((temp_ec * 6.5536) / 256)
    c02_lb = int((temp_ec * 6.5536) - 256 * c02_hb)

    # Read pH
    i2c.writeto(0x63, "R")
    time.sleep(0.9)
    temp_ph = convert(i2c.readfrom(0x63, 8))
    c03_hb = int((temp_ph * 4096) / 256)
    c03_lb = int((temp_ph * 4096) - 256 * c03_hb)

    # Send to Sigfox
    s.send(bytes([c01_hb, c01_lb, c02_hb, c02_lb, c03_hb, c03_lb, 0, 0, 0, 0, 0, 0]))
    time.sleep(900)
