import RPi.GPIO as GPIO
import serial
import time

GPIO.setmode(GPIO.BOARD)

# pin setup
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # aux
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
# set transmitter/receiver mode
GPIO.output(13,GPIO.LOW)
GPIO.output(15,GPIO.LOW)

try:
    while True:
##        aux = GPIO.input(12)-
##        print('aux val '+str(aux))
        
        ser.write(b'3')
#        num="3"
#        ser.write(bytes(num.encode("ascii")))
##        if ser.in_waiting:
##            print('rxd val '+str(ser.readline()))
                
    GPIO.cleanup()
    ser.close()

except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()
