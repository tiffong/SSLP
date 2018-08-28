print "initializing..."
from subprocess import call
import numpy as np
import cv2
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
	print "capturing image..."
	os.system('raspistill -n -w 500 -h 500 -o cam.jpg')
	img = cv2.imread("cam.jpg")
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color=img[y:y+h,x:x+w]
	
	if len(faces) != 0:		
		"faces detected!"	
		cv2.imshow('img',img)
		cv2.waitKey(0)
	else:
		cv2.imshow('img',img)	
		cv2.waitKey()	
		print "no faces detected"

