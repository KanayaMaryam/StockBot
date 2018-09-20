import tensorflow as tf
import keras
import numpy

def main():
    x = tf.placeholder(tf.float32, [None, 3])
    output = neural_network(x)
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        result = session.run(output, feed_dict={x: [[1, 2, 3]]})
        print(result)

def neural_network(tensor):
    return tf.layers.dense(tensor, 1)

def get_data_iterator():
    datapoint = pull

if __name__ == "__main__":
    main()


