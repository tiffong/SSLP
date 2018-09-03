# For drone: receive message then send it out again.

import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BOARD)

# pin setup
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # aux
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1
# set transmitter/receiver mode
GPIO.output(13,GPIO.HIGH)
GPIO.output(15,GPIO.HIGH)

ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

try:
    while True:
        if ser.in_waiting:
            msg=str(ser.readline()).encode()
            ser.write(msg)
        
except Exception as e:
    print(e)
    GPIO.cleanup()
    ser.close()