import os

ret = os.system('python check_dropped_bits.py > dropped.txt')
ret = os.system('python serial_to_list.py > serial_list.txt')
ret = os.system('python produce_image.py')