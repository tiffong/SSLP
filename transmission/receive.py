import RPi.GPIO as GPIO
import serial
import time

GPIO.setmode(GPIO.BOARD)

# pin setup
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # aux
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1

ser = serial.Serial('/dev/ttyUSB0', 9600)

try:
    int r = 1;
    void setup(){
        Serial.begin(9600);
    }
    void loop(){
        if(Serial.available()){         //From RPi to Arduino
            r = r * (Serial.read() - '0');  //conveting the value of chars to integer
            Serial.println(r);
        }
    }
    GPIO.cleanup()
    ser.close()


except KeyboardInterrupt:
        GPIO.cleanup()
        ser.close()



