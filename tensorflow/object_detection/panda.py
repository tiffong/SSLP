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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function 

import argparse

import numpy as np
import tensorflow as tf

print("initializing...")
# Import packages
import os
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
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
ser.write(b"initializing...")

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

def load_graph(model_file):
	graph = tf.Graph()
	graph_def = tf.GraphDef()
	
	with open(model_file, "rb") as f:
		graph_def.ParseFromString(f.read())
	with graph.as_default():
		tf.import_graph_def(graph_def)
	return graph

def read_tensor_from_image_file(file_name,
				input_height=299,
				input_width=299,
				input_mean=0,
				input_std=255):
	input_name = "file_reader"
	output_name = "normalized"
	file_reader = tf.read_file(file_name, input_name)
	if file_name.endswith(".png"):
		image_reader = tf.image.decode_png(
			file_reader, channels=3, name="png_reader")
	elif file_name.endswith(".gif"):
		image_reader = tf.squeeze(
			tf.image.decode_gif(file_reader, name="gif_reader"))
	elif file_name.endswith(".bmp"):
		image_reader = tf.image.decode_bmp(file_reader, name="bmp reader")
	else:
                image_reader = tf.image.decode_jpeg(
			file_reader, channels=3, name="jpeg_reader")
	float_caster = tf.cast(image_reader, tf.float32)
	dims_expander = tf.expand_dims(float_caster, 0)
	resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
	normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
	sess = tf.Session()
	result = sess.run(normalized)

	return result

def load_labels(label_file):
	label = []
	proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
	for l in proto_as_ascii_lines:
		label.append(l.rstrip())
	return label

print("loading Tensorflow model...")
ser.write(b"loading Tensorflow model...")
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

# Initialize animal classification model
print("loading animal classification model...")
ser.write(b"loading animal classification model...")
file_name = "temp.jpg"
model_file = "./output_graph"
label_file = "./output_labels/output_labels.txt"
input_layer = "Placeholder"
output_layer = "final_result"
graph = load_graph(model_file)

input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation = graph.get_operation_by_name(input_name)
output_operation = graph.get_operation_by_name(output_name)

# Initialize camera and perform object detection.
# The camera has to be set up and used differently depending on if it's a
# Picamera or USB webcam.
# Initialize Picamera and grab reference to the raw capture
print("setting up camera...")
ser.write(b"setting up camera...")
camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

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

# system status message
msg=b' SYSTEM: NORMAL; STATUS: RUNNING '
print(msg)
ser.write(msg)
time0=time.time()

print("beginning PIR scan...")
ser.write(b" beginning PIR scan... ")
try:
    while True:
        # check PIR
        pir_out=GPIO.input(37)
        # send a message back confirming functionality after 30 min has passed.
        time1=time.time()
        time_lapsed=time1-time0
        if time_lapsed>1800:
            msg=b' SYSTEM: NORMAL; STATUS: RUNNING '
            print(msg)
            ser.write(msg)
            time0=time1
        if pir_out == 1:
            GPIO.output(36,GPIO.HIGH)
            counter=0
            rawCapture.truncate(0)
            camera.capture(file_name, quality=30) 
            for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
                
                camera.capture('/home/pi/Desktop/saved-images/'+time.strftime("%y%m%d_%H%M%S")+'_human.jpg', quality=6)
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
               
                found_human = False
                score = 0.0	
                print("MS2")
                for idx,value in enumerate(classes[0]):
                    object_name=(category_index.get(value)).get('name')
                    if scores[0,idx]>threshold and object_name=='person':
                       	found_human = True 
			#camera.capture('/home/pi/Desktop/saved-images/image%s.jpg' %counter, quality=6)
                        print((category_index.get(value)).get('name'))
                        print(scores[0,idx])
                        score = scores[0,idx]	
                
                print("MS3")
                if found_human:
                        camera.capture('/home/pi/Desktop/saved-images/'+time.strftime("%y%m%d_%H%M%S")+'_human.jpg', quality=6)
                        msg=b' person found @ '+time.strftime("%y%m%d_%H%M%S") + str(score) 
                        print('person found @ '+time.strftime("%y%m%d_%H%M%S"))
                        ser.write(msg)
                else:
                        t = read_tensor_from_image_file(
                                file_name)
                        print("MS3.5") 
                        with tf.Session(graph=graph) as sess:
                                 results = sess.run(output_operation.outputs[0], {
                                         input_operation.outputs[0]: t
                                 })
                        results = np.squeeze(results)
                        print("MS4")
                        top_k = results.argsort()[-5:][::-1]
                        labels = load_labels(label_file)
                        cutoff_satisfied = False
                        animal_name = ""
                        max_likelihood = 0.0 
                        for i in top_k:
                               print(labels[i], results[i])
                               if results[i] > max_likelihood:
                                       max_likelihood = results[i]
                                       animal_name = labels[i]	
                               if results[i] > animal_cutoff:
                                       cutoff_satisfied = True	

                        if cutoff_satisfied:
                                msg=b' animal found @ '+time.strftime("%y%m%d_%H%M%S") + str(score) + ' and it appears to be a ' + animal_name 
                                camera.capture('/home/pi/Desktop/saved-images/'+time.strftime("%y%m%d_%H%M%S")+'_'+animal_name+'.jpg', quality=6)
                                ser.write(msg)	

#                # Draw the results of the detection (aka 'visualize the results')
#                vis_util.visualize_boxes_and_labels_on_image_array(
#                    frame,
#                    np.squeeze(boxes),
#                    np.squeeze(classes).astype(np.int32),
#                    np.squeeze(scores),
#                    category_index,
#                    use_normalized_coordinates=True,
#                    line_thickness=8,
#                    min_score_thresh=0.40)
#                cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
#
#                # All the results have been drawn on the frame, so it's time to display it.
#                cv2.imshow('Object detector', frame)

                t2 = cv2.getTickCount()
                time1 = (t2-t1)/freq
                frame_rate_calc = 1/time1

                rawCapture.truncate(0)

                if counter>25:
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
