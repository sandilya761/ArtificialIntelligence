# This file contains all the helper functions that will be used while creating the network
# This file will be imported in all other files --> from ops import *

import tensorflow as tf
import numpy as np


# helper function to initialize weights
def init_weight(shape, stddev):
    return tf.Variable(tf.random_normal(shape=shape, stddev=stddev))


# helper function to initialize biases
def init_bias(shape):
    return tf.Variable(tf.zeros(shape=shape))


# helper function to create convolutional layer
def conv2d(X, filter, strides, padding):
    return tf.nn.conv2d(input=X, filter=filter, strides=strides, padding=padding)


# helper function to calculate the cost function
def cost(labels, logits):
    return tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits))




