import RPi.GPIO as GPIO
from scipy import ndimage
from scipy import misc
import numpy as np
import serial
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
    img=ndimage.imread('image8.jpg',mode='RGB')
    print(img.shape)
    buf_size=242
    data_buff=np.zeros(buf_size)
    h=img.shape[0]
    w=img.shape[1]
    data_buff[0]=h
    data_buff[1]=w
    buf_ct=2;
    for i in range(0,h*w):
        h_pix=int(i/h)
        w_pix=h_pix+i%h
        colors=img[h_pix,w_pix,:]
        data_buff[buf_ct]=colors[0]
        data_buff[buf_ct+1]=colors[1]
        data_buff[buf_ct+2]=colors[2]
        buf_ct=buf_ct+3
        if buf_ct==buf_size:
            for j in range(0,int(buf_size)):
                dat_enc=(str(data_buff[j])+' ').encode()
                ser.write(dat_enc)
            buf_ct=2  
        if i==h*w-1:
            for j in range(0,buf_ct):
                dat_enc=(str(data_buff[j])+' ').encode()
                ser.write(dat_enc)                
            for j in range(buf_ct,buf_size):
                ser.write(b'0')
    GPIO.cleanup()
    ser.close()

except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()

