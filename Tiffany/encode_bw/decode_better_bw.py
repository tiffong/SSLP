import numpy as np
import scipy as misc
from scipy.misc import imsave
from PIL import Image

np.set_printoptions(threshold = 'nan')
#packet is 720.0, 1280.0, and 240 numbers
packet_size = 240

#create an array that is 720 by 1280
bw_values = np.zeros((720,1280)) #row, col

#OPEN FILE HERE
with open('bwtest.txt', 'r') as f: 
#with open('test2.txt', 'r') as f:
    raw_img = f.readlines() 
    shape = np.shape(raw_img)

    #print(shape)

    length = shape[0] #num of lines in text file

    #print(length) #make sure it's the number of numbers in the txt file

    #for image recreation
    h=720 #gets height, 720
    w=1280 #gets wideth, 1280

    row = 0 
    col = 0
    # print(raw_img[2])
    # print(raw_img[3])
    # print(raw_img[4])
    start = 0
    for i in range(0,length):  #for all packets that were sent  
        
        if row == 720:
            break

        #group every 3 values into an array (R,G,B)
        
        bw_values[row,col] = raw_img[start]
        start=start+1
        #print(row,col)

        col = col + 1

        if col %1280 == 0 :
            row = row + 1   
            col = 0 

#Save image onto desktop
imsave('STUPID.png', bw_values)