from PIL import Image

import numpy as np

#makes it so you print all things
np.set_printoptions(threshold = 'nan')

#image to array
img_filename = "download.jpg"
img = Image.open(img_filename)
img = img.convert("RGB")

#print(img)
#img.show()

aa  = np.array(img)

h=aa.shape[0]
w=aa.shape[1]

for row in range(0,h):
	for col in range(0,w):
		rgb = aa[row][col]
		
		print(rgb[0])
		print(rgb[1])
		print(rgb[2])
		
