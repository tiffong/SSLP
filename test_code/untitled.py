from scipy import ndimage
from scipy import misc
import numpy as np
import serial
import time

img=ndimage.imread('8.jpg',mode='RGB')
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