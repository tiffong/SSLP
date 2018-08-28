#captures 5 images and saves to folder on desktop

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation = 180
camera.start_preview()

for i in range(5):
    sleep(2)
    camera.capture('/home/pi/Desktop/saved-images/image%s.jpg' %i)
camera.stop_preview()

