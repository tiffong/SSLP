#used to formal text block received from Serial transmission from RPI
#text block should have all headers

#USAGE: python serial_to_txt_file.py > decode.txt

#IMPORTANT: REMEMBER TO ADD 0 TO THE BEGINNING OF THE 300 OR THIS WILL NOT WORK

from decimal import Decimal
import numpy as np

with open('corrupted_serial.txt', 'r') as f: 
#with open('test2.txt', 'r') as f:
	raw_img = f.readlines() 
	array = raw_img[0].split(".") #split by decimal
	leading_removed = [s.lstrip("0") for s in array] #remove leading 0
	leading_removed.pop() #remove new line character at end

	#print(leading_removed)

	#for serial
	final_array = map(int, leading_removed) #convert to integer
	#print(final_array)

	#for testing
	#raw_img = map(lambda s: s.strip(), raw_img)   
	#raw_img = map(float, raw_img)
	#raw_img = map(int, raw_img)
	#print(raw_img)

	length = np.shape(final_array)[0]
	#print(length)

for i in range(0,length):
	print final_array[i]
