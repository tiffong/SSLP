import RPi.GPIO as GPIO
import sys

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # pir
GPIO.output(13,GPIO.LOW)
GPIO.output(15,GPIO.LOW)

try:
    while True:
        print(GPIO.input(37))
    
except KeyboardInterrupt:
    GPIO.cleanup()