#given a text file containing which headers are corrupted and how many are 
#bytes are needed to be added, just adds random values, let's make them white
#make the added values 0

import numpy as np
from scipy.misc import imsave
#these are the header numbers and num of bytes missing

h=90 #gets height, 720
w=160 #gets width, 1280

with open('emtpy.txt', 'r') as z: 
#with open('test2.txt', 'r') as f:
	values = z.readlines() 
	values = map(lambda s: s.strip(), values)  
	values = map(float, values)
	values = map(int, values)

	length = np.shape(values)[0]
	#print(length)

headers = list()
num_missing = list()

for i in range(0,length):
	if i%2 == 0:
		headers.append(values[i])
	else:
		num_missing.append(values[i])

#print(headers)
#print(num_missing)
missing = length/2
#print(missing)

#this is the actual corrupted file, with bytes missing
with open('corrupted.txt', 'r') as f: 
#with open('test2.txt', 'r') as f:
	values2 = f.readlines() 
	values2 = map(lambda s: s.strip(), values2)  
	values2 = map(float, values2)
	values2 = map(int, values2) #integers containing corrupted headers and values

	length2 = np.shape(values2)[0]

	#print(values2)
	#print(length2)

#print(values2)
#print(values2[0])


dummy_value = 0


indices = list()
for i in range(0,missing):
#find index of missing header
	index = values2.index(headers[i])
	indices.append(index)
	#print(index)


for j in range(0,missing):
	index_to_fix = indices[j]
	add_this_many = num_missing[j]

	for k in range(0, add_this_many):
		values2.insert(index_to_fix, dummy_value)

#make sure this is 14660 long
#print(np.shape(values2)[0])
#print(values2)


bw_values = np.zeros((h,w)) #row, col of image

#final_array = np.asarray(values2)
#print(final_array)

#SAVE THE FUCKING IMAGE
#imsave('recreation2.png', values2)

#bw_values = np.zeros((720,1280)) #row, col of image
bw_values = np.zeros((h,w)) #row, col of image

row = 0 
col = 0

header = 0 #value of header
start = 0
packet_size = 241
for i in range(0,length2):  #for all packets that were sent  
    
    #if you've reached a header, skip over it
    if start % packet_size == 0:
        header = start
        start = start + 1

    if row == h:
        break
    
    bw_values[row,col] = values2[start]
    start=start+1
    #print(row,col)

    col = col + 1

    if col %w == 0 :
        row = row + 1   
        col = 0 

#Save image onto desktop
#TODO: get to save it as the time and date
imsave('recreation.png', bw_values)














