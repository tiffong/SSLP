import RPi.GPIO as GPIO
import serial
import base64
import reedsolo
import time

GPIO.setmode(GPIO.BOARD)

# pin setup
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1
# set transmitter/receiver mode
GPIO.output(13,GPIO.LOW)
GPIO.output(15,GPIO.LOW)

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS,
    timeout=1
)

try:
#read image into file as array   
    with open('image8.jpg','rb') as f:
        img=f.read()
    img_enc=base64.encodestring(img)
    #rs=reedsolo.RSCodec(12)
    #img_enc=rs.encode(img)
    
    chunksize=64
    numchunks=int(len(img_enc)/chunksize)
    ser.write(img_enc[0:chunksize])
    for i in range(0,numchunks):
        ser.write(img_enc[0+i*chunksize:chunksize+i*chunksize])
        time.sleep(1)
    ser.write(img_enc[numchunks*chunksize:-1])
##    i=1
##    while True:
##        num_bytes_buf=ser.out_waiting
##        if num_bytes_buf==0 and i<numchunks:
##            ser.write(img_enc[0+i*chunksize:chunksize+i*chunksize])
##            i=i+1
##        elif num_bytes_buf>8:
##            time.sleep(0.5)
##        elif i==numchunks:
##            ser.write(img_enc[numchunks*chunksize:-1])
##            i=i+1
##        elif i>numchunks:
##            break
            
    GPIO.cleanup()
    ser.close()

except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()

