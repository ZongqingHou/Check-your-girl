import tensorflow as tf
import numpy as np
import glob
import json
import threading
import math
import sys

image = glob.glob(r'../data/*.jpg')
file_path = open('path_collection.txt', 'w')
index = 0

def view_bar(message, num, total):
    rate = num / total
    rate_num = int(rate * 40)
    rate_nums = math.ceil(rate * 100)
    r = '\r%s:[%s%s]%d%%\t%d/%d' % (message, ">" * rate_num, " " * (40 - rate_num), rate_nums, num, total,)
    sys.stdout.write(r)
    sys.stdout.flush()

def process_thread(coord, tr_id):
	global image
	global file_path
	global index

	while not coord.should_stop():
		if index < len(image):
			temp = image[index]
			index += 1
			image_raw_data = tf.gfile.FastGFile(temp, 'rb').read()

			with tf.Session() as sess:
				img_data = tf.image.decode_jpeg(image_raw_data)
				img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
				padded = tf.image.resize_image_with_crop_or_pad(img_data, 500, 500).eval()

			data = {
				temp: padded.tolist()
			}

			with open('tempdata.json', 'w') as f:
				json.dump(data, f)

			file_path.write(temp + ' ')
			view_bar("processing image of " ,index, 3000)
		else:
			coord.request_stop()

coord = tf.train.Coordinator()
threads = [threading.Thread(target=process_thread, args=(coord, i, )) for i in range(5)]
for tr in threads: tr.start()
coord.join(threads)
file_path.close()