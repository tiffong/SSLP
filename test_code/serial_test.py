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

try:
    # set transmitter/receiver mode
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(15,GPIO.HIGH)
            
    instr = b'\xC1'
    ser.write(instr)
    ser.write(instr)
    ser.write(instr)
    print('instruction written')
    
    while True:
        print(ser.read())
        
    GPIO.cleanup()
    ser.close()

except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()
