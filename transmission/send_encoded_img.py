#USAGE: python i_bw.py > 'text.txt'

from PIL import Image
import numpy as np
import RPi.GPIO as GPIO
import serial

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
GPIO.output(13,GPIO.HIGH)
GPIO.output(15,GPIO.HIGH)

#makes it so you print all things
np.set_printoptions(threshold = 'nan')

#image to array
img_filename = "9.jpg" #eventually get this to iterate through the directory
img = Image.open(img_filename)
img = img.resize((160,90)) #resize to desired image
img = img.convert("L") #L is black and white, RGB is color

#img.show()

aa  = np.array(img) 
#print(aa)

h=aa.shape[0] #height
w=aa.shape[1] #width
#print(h)s
#print(w) #test to check correct picture dimensions

#COMMENT OUT IF USING RPI
# for row in range(0,h):
# 	for col in range(0,w):
# 		print(aa[row][col])
	
#FOR TESTING - to show image that has been converted into an array
#alpha = Image.fromarray(aa,"L")
#alpha.save('my.png')
#alpha.show()

#########FOR USE WITH RASPBERRY PI############

#initialize variables
size = 241
#size = 257
data_buff=np.zeros(size) #create a buffer of whatever size to send in packets

#iterate over every pixel
iteration_sent = 300 #what packet number youv'e sent so far, sent as a header
pixel_count = h*w #how many pixels are in the image
counter = 1

#counter = 1 #start at 1 to skip over the header (iteration)


for i in range (0, pixel_count):
	row2=int(i/w)
	col2=i%w

	data_buff[0] = iteration_sent #the header of each packet sent	
	#print(row2,col2)
	data_buff[counter] = aa[row2][col2]
	counter = counter + 1

	if counter == size: #if you've reached the buffer size, send buffer to the RPi/Arduino
		#print('buffer size reached', counter, iteration_sent)
		iteration_sent = iteration_sent + 1
		for j in range (0, int(size)):
			#dat_enc=(str(data_buff[j])+' ').encode() #is this how to concantenate strings?
			dat_enc=data_buff[j]  #is this how to concantenate strings?
			ser.write(str(dat_enc).encode())	
			#print(dat_enc)
		
		#after you send the packet, increase iteration_sent	
		counter = 1
		#counter = 1

	# if counter == size-1: #if you've reached the buffer size, send it through to the RPi/Arduino
	# 	for j in range (0, counter):
	# 		dat_enc=(str(data_buff[j])+' ').encode() #is this how to concantenate strings
	# 		#ser.write(dat_enc)
	# 		print(dat_enc)
 #        for j in range(counter,size):
 #        	print('0')
 #        	#ser.write(b'0')


	# 	#after you send the packet, increase iteration_sent	
	# 	iteration_sent = iteration_sent + 1
	# 	counter = 0
	# 	#counter = 1	#reset counter
