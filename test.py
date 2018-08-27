import RPi.GPIO as GPIO
import serial
import time

GPIO.setmode(GPIO.BOARD)

# pin setup
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # aux
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1

ser = serial.Serial('/dev/ttyUSB0', 9600)

try:

    ser.write(b'3')
    ser.write(b'5')
    ser.write(b'7')
    GPIO.cleanup()
    ser.close()


except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()

