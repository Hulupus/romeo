# main.py -- put your code here!

import pycom as p
import time
from network import Sigfox
import socket
from machine import Pin

from machine import I2C

## Init i2c
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


# Init Sigfox
# Sigfox wird zensiert

calibration_mode = True
runs_without_calibration = 0


def calibrate():
    answer = input("pH, ec, t, help? ")
    if answer == "pH":
        ph_answer = input("Welcher pH-Wert ")
        if ph_answer == "7":
            i2c.writeto(0x63, "Cal,mid,7.00")
        elif ph_answer == "4":
            i2c.writeto(0x63, "Cal,low,4.00")
        elif ph_answer == "10":
            i2c.writeto(0x63, "Cal,high,10.00")
        else:
            print("No response")

    elif answer == "ec":
        ec_answer = input("dry, n, ...")
        if ec_answer == "dry":
            i2c.writeto(0x64, "Cal,dry")
        elif ec_answer == "n":
            i2c.writeto(0x64, "Cal," + input("n? "))
        else:
            print("No response")  # implement safety

    elif answer == "t":
        i2c.writeto(0x66, "Cal," + input("t? "))

    elif answer == "help":
        print(
            "https://files.atlas-scientific.com/EZO_RTD_Datasheet.pdf, https://files.atlas-scientific.com/pH_EZO_Datasheet.pdf, https://files.atlas-scientific.com/EC_EZO_Datasheet.pdf"
        )

    else:
        print("No Response")

    time.sleep(1)


def convert(bytestring):
    string = bytestring.decode("utf-8")
    cleansed_string = "".join(c for c in string if c.isdigit() or c == ".")
    dezimal = float(cleansed_string)
    return dezimal


while True:
    ##Temperatur##
    i2c.writeto(0x66, "R")
    time.sleep(0.7)
    temp_temperatur = i2c.readfrom(0x66, 8)
    print(convert(temp_temperatur))

    ## Leitfähigkeit ## EC-Wert ##
    i2c.writeto(0x64, "R")
    time.sleep(0.7)
    temp_ec = i2c.readfrom(0x64, 5)
    print(convert(temp_ec))

    ## pH ## pH-Wert ##
    i2c.writeto(0x63, "R")
    time.sleep(0.9)
    temp_ph = i2c.readfrom(0x63, 8)
    print(convert(temp_ph))

    ## Calibrieren ##
    if calibration_mode and runs_without_calibration <= 0:
        if input("Möchtest du kalibrieren? ") == "y":
            calibrate()
            runs_without_calibration = 50
        else:
            if input("Möchtest du später kalibrieren? ") == "y":
                runs_without_calibration = 250
            else:
                runs_without_calibration = 25
    if calibration_mode:
        runs_without_calibration = runs_without_calibration - 1
