#given a text file with headers (from 300 to 359) will create an image and 
#save it to desktop

import numpy as np
import scipy as misc
from scipy.misc import imsave
from PIL import Image

#set so you print all of the numbers
np.set_printoptions(threshold = 'nan')

#SET PACKET SIZE HERE 
#packet is 720.0, 1280.0, and 240 numbers
#packet_size = 257
packet_size = 241

#OPEN TEXT FILE HERE
with open('serial_list.txt', 'r') as f: 
#with open('test2.txt', 'r') as f:
    raw_img = f.readlines() 
    shape = np.shape(raw_img)

    #print(shape)
    length = shape[0] #num of lines in text file

    #print(length) #make sure it's the number of numbers in the txt file
    #print(raw_img[0])
    #print(raw_img[1])

    #for image recreation
    h=90 #gets height, 720
    w=160 #gets width, 1280

    #bw_values = np.zeros((720,1280)) #row, col of image
    bw_values = np.zeros((h,w)) #row, col of image

    row = 0 
    col = 0

    header = 0 #value of header
    start = 0
    for i in range(0,length):  #for all packets that were sent  
        
        #if you've reached a header, skip over it
        if start % packet_size == 0:
            header = start
            start = start + 1

        if row == h:
            break
        
        bw_values[row,col] = raw_img[start]
        start=start+1
        #print(row,col)

        col = col + 1

        if col %w == 0 :
            row = row + 1   
            col = 0 

#Save image onto desktop
#TODO: get to save it as the time and date
imsave('recreation.png', bw_values)