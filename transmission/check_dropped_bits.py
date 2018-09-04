#used to format text block received from Serial transmission from RPI
#text block should have all headers included

#USAGE: python format_serial.py > edited.txt

from decimal import Decimal
import numpy as np

with open('Serial.txt', 'r') as f: 
#with open('test2.txt', 'r') as f:
	raw_img = f.readlines() 
	array = raw_img[0].split(".") #split by decimal
	leading_removed = [s.lstrip("0") for s in array] #remove leading 0
	leading_removed.pop() #remove new line character at end


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

sixty = np.arange(300,360)
#print(sixty)

headers = list() #contains indexes of all headers 
#add these headers to a list
for header in range(300,360):
	headers.append(final_array.index(header)) 

#print(headers)
#print(len(headers))

#put differences between consecutive headers in a list
differences = list()
for i in range(0,59):
	differences.append(headers[i+1] - headers[i])
differences.append(length - headers[59])
#print(differences)
#print(len(differences))

#testing program by changing differences
# differences[0] = 231
# differences[9]  = 239
# differences[10] = 240

#print(differences)

buf_size = 241
for i in range(0,60):
	if differences[i] != buf_size:
		print(i+300)
		print(buf_size - differences[i])
