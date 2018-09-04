######## Picamera Object Detection Using Tensorflow Classifier #########
#
# Author: Evan Juras
# Date: 4/15/18
# Description: 
# This program uses a TensorFlow classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a Picamera feed.
# It draws boxes and scores around the objects of interest in each frame from
# the Picamera. It also can be used with a webcam by adding "--usbcam"
# when executing this script from the terminal.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.

print("initializing...")
# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import tensorflow as tf
import argparse
import RPi.GPIO as GPIO
import serial
import sys
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT) # M0
GPIO.setup(15,GPIO.OUT) # M1
GPIO.setup(36,GPIO.OUT) # infrared light
GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) # pir
GPIO.output(13,GPIO.LOW)
GPIO.output(15,GPIO.LOW)
GPIO.output(36,GPIO.LOW)

# Set up serial communication
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Set up camera constants
IM_WIDTH = 1280
IM_HEIGHT = 720
#IM_WIDTH = 640    Use smaller resolution for
#IM_HEIGHT = 480   slightly faster framerate

# Select camera type (if user enters --usbcam when calling this script,
# a USB webcam will be used)
camera_type = 'picamera'
parser = argparse.ArgumentParser()
parser.add_argument('--usbcam', help='Use a USB webcam instead of picamera',
                    action='store_true')
args = parser.parse_args()
if args.usbcam:
    camera_type = 'usb'

# This is needed since the working directory is the object_detection folder.
sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 90

## Load the label map.
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

print("loading Tensorflow model...")

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize camera and perform object detection.
# The camera has to be set up and used differently depending on if it's a
# Picamera or USB webcam.
# Initialize Picamera and grab reference to the raw capture
print("setting up camera...")
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

# set up the image classification so it will run faster later
idx=0
for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    idx=idx+1
    frame = frame1.array
    frame.setflags(write=1)
    frame_expanded = np.expand_dims(frame, axis=0)
    (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: frame_expanded})
    if idx>0:
        break
rawCapture.truncate(0)

# check starting time
time0=time.time()
# img xmit flags
img_taken=0
img_xmit=0
img_xmitting=0
img_done=0
print("beginning PIR scan...")
try:
    while True:
        # check PIR
        pir_out=GPIO.input(37)
        # check time
        time1=time.time()
        time_lapsed=time1-time0

        if time_lapsed>10:#1800:
            time0=time1
            print('img_taken '+str(img_taken))
            # if there are any images, start sending the latest one.
            if img_taken and img_xmitting != 1:
                img_xmit=1
                img_xmitting=1
                # load latest image
                all_imgs=os.listdir('/home/pi/Desktop/saved-images/')
                img_to_send='/home/pi/Desktop/saved-images/'+all_imgs[-1]
                print('img to send '+img_to_send)
                # load latest image in packets and start sending
                img=Image.open(img_to_send)
                img=img.resize((160,90)) # resize for transmission
                img=img.convert("L")
                img_array=np.array(img)
                h=img_array.shape[0]
                w=img_array.shape[1]
                size=241
                data_buff=np.zeros(size) # create a buffer to send in packets
                # start the iteration over every pixel
                iteration_sent=300
                pixel_count=h*w
                packet=1
                for counter in range(1,int(size)):
                    row2=int(packet/w)
                    col2=packet%w
                    data_buff[0]=iteration_sent # the header of each packet sent
                    data_buff[counter]=img_array[row2][col2]
                    ser.write(str(data_buff[counter]).encode())
                print('sending packet '+str(packet))
                iteration_sent=iteration_sent+1
                packet=packet+1

        # if image not done sending and pir hasn't been triggered yet
        if pir_out!=1 and img_xmitting==1 and img_done!=1:
            for counter in range(0,int(size)):
                row2=int(packet/w)
                col=packet%w
                data_buff[0]=iteration_sent
                data_buff[counter]=img_array[row2][col2]
                ser.write(str(data_buff[counter]).encode())
            print('sending packet '+str(packet))
            iteration_sent=iteration_sent+1
            packet=packet+1
            if packet == pixel_count:
                img_done=1

        # if image done sending
        if img_done==1:
            # reset variables
            img_xmitting=0
            img_done=0

        if pir_out == 1:
            GPIO.output(36,GPIO.HIGH)
            counter=0
            rawCapture.truncate(0)
            for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
                counter=counter+1
                print(counter)
                t1 = cv2.getTickCount()
                
                # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
                # i.e. a single-column array, where each item in the column has the pixel RGB value
                frame = frame1.array
                frame.setflags(write=1)
                frame_expanded = np.expand_dims(frame, axis=0)
                
                # Perform the actual detection by running the model with the image as input
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: frame_expanded})
                threshold = 0.1
                # Print detected objects and scores
                objects=[]
                for idx,value in enumerate(classes[0]):
                    object_name=(category_index.get(value)).get('name')
                    if scores[0,idx]>threshold and object_name=='person':
                        camera.capture('/home/pi/Desktop/saved-images/'+time.strftime("%y%m%d_%H%M%S")+'.jpg', quality=6)
                        img_taken=1
                        print('img taken')
                        
                t2 = cv2.getTickCount()
                time1 = (t2-t1)/freq
                frame_rate_calc = 1/time1

                rawCapture.truncate(0)

                if counter>1:
                    # turn off infrared lighting
                    GPIO.output(36,GPIO.LOW)
                    break

except KeyboardInterrupt: 
    camera.close()        
    GPIO.cleanup()
    ser.close()
    cv2.destroyAllWindows()
    
except Exception as e:
    print(e)
    camera.close()        
    GPIO.cleanup()
    ser.close()
    cv2.destroyAllWindows()
##    # restart program
##    cmd='python3 /home/pi/Desktop/SSLP/tensorflow/object_detection/panda.py'
##    print(cmd)
##    ret=os.system(cmd)
