from cnn import inference

x = tf.placeholder(tf.float32, [1, NODE_SIZE, NODE_SIZE, NUM_CHANNELS], name='x-input')
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
	test, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x: x_input_, y_: y_input_})