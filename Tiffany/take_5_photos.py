#FIELD TEST: test to take images and save them to desktop
import os

#captures 5 photos in a row
camera.start_preview()
for i in range(5):
    sleep(10)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()


#os.chdir('/home/pi/Desktop')
