from picamera import PiCamera
from time import sleep

camera = PiCamera()

#camera.rotation = 180
##camera.start_preview()
##sleep(10)
##camera.stop_preview()

camera.capture('/home/pi/Desktop/test.bmp', quality=6)
camera.close()


