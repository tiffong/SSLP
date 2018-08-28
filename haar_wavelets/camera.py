print "initializing..."
from subprocess import call
from SimpleCV import Image, Display
import RPi.GPIO as GPIO
import serial
import time
import os

## set up transmission hardware and PIR sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # aux
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # PIR
GPIO.output(13,GPIO.LOW)
GPIO.output(15,GPIO.LOW)

ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

try:
    # open display
    display = Display()
    print "Display opening..."

    while display.isNotDone():
        pir_output=GPIO.input(37)
        num_imgs=0

        if pir_output:
            num_imgs=num_imgs+1
            print "capturing image..."
            os.system('raspistill -n -w 500 -h 500 -o cam.jpg')
            img = Image("cam.jpg")
            
            print 'searching for features...'
            profile_features = img.findHaarFeatures('profile.xml')
            lower_features = img.findHaarFeatures('lower_body.xml')	
            upper_features = img.findHaarFeatures('upper_body.xml')	
            face_features = img.findHaarFeatures('face.xml')	
            if (face_features is not None and len(face_features) != 0): 
                    img.show()	
                    print 'Face features found at:'
                    for f in face_features:
                            coord = f.coordinates
                            print coord
                    string1 = b'Face detected! \n'
                    string1_encode = string1.encode()
                    ser.write(string1)#string1_encode)
            elif (profile_features is not None and len(profile_features) != 0): 
                    img.show()	
                    print 'Profile features found at:'
                    for f in profile_features:
                            coord = f.coordinates
                            print coord
                    string1 = b'Profile detected! \n'
                    string1_encode = string1.encode()
                    ser.write(string1)
            elif (lower_features is not None and len(lower_features) != 0): 
                    img.show()	
                    print 'Lower features found at:'
                    for f in lower_features:
                            coord = f.coordinates
                            print coord
                    string1 = b'Lower body detected! \n'
                    string1_encode = string1.encode()
                    ser.write(string1)
            elif (upper_features is not None and len(upper_features) != 0): 
                    img.show()	
                    print 'Upper features found at:'
                    for f in upper_features:
                            coord = f.coordinates
                            print coord
                    string1 = b'Upper body detected! \n'
                    string1_encode = string1.encode()
                    ser.write(string1)
            else:
                    print 'No features found.'	
                    #call("raspistill -o cam.jpg", shell=True)
##            if num_imgs>3:
##                break
except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()