from cnn import inference
import tensorflow as tf
import numpy as np
import util

NODE_SIZE = 300
LEARNING_RATE_BASE = 0.01
LEARNING_RATE_DECAY = 0.99
REGULARIZATRION_RATE = 0.0001
MOVING_AVERAGE_DECAY = 0.99
NUM_CHANNELS = 3
TRAINING_STEPS = 1000

def train(img_x, label_y, check_path):
	image_raw_data = tf.gfile.FastGFile(check_path, 'rb').read()

	x = tf.placeholder(tf.float32, [len(img_x), NODE_SIZE, NODE_SIZE, NUM_CHANNELS], name='x-input')
	# x_ = tf.placeholder(tf.float32, [1, NODE_SIZE, NODE_SIZE, NUM_CHANNELS], name='check-input')
	y_ = tf.placeholder(tf.float32, [None, 1], name='y-input')

	regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATRION_RATE)

	y = inference(x, False, regularizer)

	global_step = tf.Variable(0, trainable=False)

	variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
	variable_averages_op = variable_averages.apply(tf.trainable_variables())
	cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
	cross_entropy_mean = tf.reduce_mean(cross_entropy)
	loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
	learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, TRAINING_STEPS, LEARNING_RATE_DECAY, staircase=True)

	train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

	with tf.control_dependencies([train_step, variable_averages_op]):
		train_op = tf.no_op(name='train')

	saver = tf.train.Saver()

	with tf.Session() as sess:
		tf.global_variables_initializer().run()

		for step in range(TRAINING_STEPS):
			test, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: img_x, y_: label_y})
			util.view_bar("processing step of " , step, 1000)

			# img_data = tf.image.decode_jpeg(image_raw_data)
			# img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
			# padded = tf.reshape(tf.image.resize_image_with_crop_or_pad(img_data, 300, 300), [1, NODE_SIZE, NODE_SIZE, NUM_CHANNELS]).eval()

			# print(sess.run(y, feed_dict={x_: padded}))