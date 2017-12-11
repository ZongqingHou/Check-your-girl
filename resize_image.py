import tensorflow as tf
import numpy as np
import glob
import json
import threading

import util

image = glob.glob(r'../Test/data/*.jpg')
img_dict = {}
index = 0

def process_thread(coord, tr_id):
	global image
	global index

	while not coord.should_stop():
		if index < len(image):
			temp = image[index]
			index += 1
			image_raw_data = tf.gfile.FastGFile(temp, 'rb').read()

			with tf.Session() as sess:
				img_data = tf.image.decode_jpeg(image_raw_data)
				img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
				padded = tf.image.resize_image_with_crop_or_pad(img_data, 300, 300).eval()

			img_dict[temp] = padded.tolist()

			# file_path.write(temp + ' ')
			util.view_bar("processing image of " ,index, 10)
		else:
			coord.request_stop()

def resize_():
	global img_dict
	# file_path = open('path_collection.txt', 'w')
	coord = tf.train.Coordinator()
	threads = [threading.Thread(target=process_thread, args=(coord, i, )) for i in range(5)]
	for tr in threads: tr.start()
	coord.join(threads)

	return img_dict
	# file_path.close()

if __name__ == '__main__':
	resize_()