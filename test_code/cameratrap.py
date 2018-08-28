import RPi.GPIO as GPIO
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # aux


try:
    while True:
        print(GPIO.input(7))
    GPIO.cleanup()
    ser.close()

except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()

##
##from gpiozero import MotionSensor
##from picamera import PiCamera
##
##camera = PiCamera()
##
##pir = MotionSensor(4)
##
##pir.wait_for_motion()
##    
##print('Motion detected')
##
##
##    
###camera.start_preview()
###camera.capture('pi/Desktop/selfie.png')
##
###pir.wait_for_no_motion()
###print('no motion')
###camera.close()
