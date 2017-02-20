import os
import sys
from datetime import datetime

import numpy as np

import scipy.io
import scipy.misc

import tensorflow as tf

import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

from PIL import Image, ImageDraw

from images2gif import writeGif
from glob import glob

STYLE_IMAGE = 'images/a.jpg'
CONTENT_IMAGE = 'images/b.jpg'

IMAGE_WIDTH = 436
IMAGE_HEIGHT = 300
COLOR_CHANNELS = 3

VGG_MODEL = 'imagenet-vgg-verydeep-19.mat'
MEAN_VALUES = np.array([123.68, 116.779, 103.939]).reshape((1,1,1,3))

NOISE_RATIO = 0.6

ALPHA = 1
BETA = 1000

STYLE_LAYERS = [
    ('conv1_1', 0.3),
    ('conv2_1', 0.25),
    ('conv3_1', 0.2),
    ('conv4_1', 0.15),
    ('conv5_1', 0.1),
]

CONTENT_LAYERS = [
    ('conv4_2', 1.0)
]

ITERATIONS = 5000

def log(file, now):
    file.write('Recorded at: %s\n\n' %now.strftime("%Y-%m-%d_%H:%M:%S"))
    file.write("-----------------------------------------------\n\n")
    file.write('Noise Ratio : %.1f\n\n' %NOISE_RATIO)
    file.write('Alpha : %d\n' %ALPHA)
    file.write('Beta  : %d\n\n' %BETA)
    file.write('Alpha/Beta : %.3f\n\n' %(float(ALPHA)/float(BETA)))
    file.write('Style layers & weights\n')
    for l in STYLE_LAYERS:
        file.write(str(l)+"\n")
    file.write("\n")
    file.write('Content layers & weights\n')
    for l in CONTENT_LAYERS:
        file.write(str(l)+"\n")
    file.write("\n")
    file.write("Iteratioln : %d\n\n" %(ITERATIONS))
    file.write("-----------------------------------------------\n\n")
    
def content_loss_func(sess, model):

    def _content_loss(p, x):
        N = p.shape[3]
        M = p.shape[1] * p.shape[2]
        return (1 / 2) * tf.reduce_sum(tf.pow(x - p, 2))
    
    E = [_content_loss(sess.run(model[layer_name]), model[layer_name]) for layer_name, _ in CONTENT_LAYERS]
    W = [w for _, w in CONTENT_LAYERS]
    loss = sum([W[l] * E[l] for l in range(len(CONTENT_LAYERS))])
    return loss

def style_loss_func(sess, model):

    def _gram_matrix(F, N, M):
        Ft = tf.reshape(F, (M, N))
        return tf.matmul(tf.transpose(Ft), Ft)

    def _style_loss(a, x):
        N = a.shape[3]
        M = a.shape[1] * a.shape[2]
    
        A = _gram_matrix(a, N, M)
        G = _gram_matrix(x, N, M)
        result = (1 / (4 * N**2 * M**2)) * tf.reduce_sum(tf.pow(G - A, 2))
        return result

    E = [_style_loss(sess.run(model[layer_name]), model[layer_name]) for layer_name, _ in STYLE_LAYERS]
    W = [w for _, w in STYLE_LAYERS]
    loss = sum([W[l] * E[l] for l in range(len(STYLE_LAYERS))])
    return loss


def generate_noise_image(content_image, noise_ratio = NOISE_RATIO):
    noise_image = np.random.uniform(-20, 20, (1, IMAGE_HEIGHT, IMAGE_WIDTH, COLOR_CHANNELS)).astype('float32')
    input_image = noise_image * noise_ratio + content_image * (1 - noise_ratio)
    return input_image

def load_image(path):
    image = scipy.misc.imread(path, mode='RGB')
    image = np.reshape(image, ((1,) + image.shape))
    image = image - MEAN_VALUES
    return image

def save_image(path, image):
    image = image + MEAN_VALUES
    image = image[0]
    image = np.clip(image, 0, 255).astype('uint8')
    scipy.misc.imsave(path, image)
    
    
def load_vgg_model(path):

    vgg = scipy.io.loadmat(path)

    vgg_layers = vgg['layers']
    
    def _weights(layer, expected_layer_name):

        W = vgg_layers[0][layer][0][0][2][0][0]
        b = vgg_layers[0][layer][0][0][2][0][1]
        layer_name = vgg_layers[0][layer][0][0][0][0]
        
        if expected_layer_name != layer_name:
            print("Warning : layer %s is not matched" % expected_layer_name)
        
        return W, b

    def _relu(conv2d_layer):
        return tf.nn.relu(conv2d_layer)

    def _conv2d(prev_layer, layer, layer_name):
        W, b = _weights(layer, layer_name)
        W = tf.constant(W)
        b = tf.constant(np.reshape(b, (b.size)))
        return tf.nn.conv2d(
            prev_layer, filter=W, strides=[1, 1, 1, 1], padding='SAME') + b

    def _conv2d_relu(prev_layer, layer, layer_name):
        return _relu(_conv2d(prev_layer, layer, layer_name))

    def _avgpool(prev_layer):
        return tf.nn.avg_pool(prev_layer, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    graph = {}
    graph['input']   = tf.Variable(np.zeros((1, IMAGE_HEIGHT, IMAGE_WIDTH, COLOR_CHANNELS)), dtype = 'float32')
    graph['conv1_1']  = _conv2d_relu(graph['input'], 0, 'conv1_1')
    graph['conv1_2']  = _conv2d_relu(graph['conv1_1'], 2, 'conv1_2')
    graph['avgpool1'] = _avgpool(graph['conv1_2'])
    graph['conv2_1']  = _conv2d_relu(graph['avgpool1'], 5, 'conv2_1')
    graph['conv2_2']  = _conv2d_relu(graph['conv2_1'], 7, 'conv2_2')
    graph['avgpool2'] = _avgpool(graph['conv2_2'])
    graph['conv3_1']  = _conv2d_relu(graph['avgpool2'], 10, 'conv3_1')
    graph['conv3_2']  = _conv2d_relu(graph['conv3_1'], 12, 'conv3_2')
    graph['conv3_3']  = _conv2d_relu(graph['conv3_2'], 14, 'conv3_3')
    graph['conv3_4']  = _conv2d_relu(graph['conv3_3'], 16, 'conv3_4')
    graph['avgpool3'] = _avgpool(graph['conv3_4'])
    graph['conv4_1']  = _conv2d_relu(graph['avgpool3'], 19, 'conv4_1')
    graph['conv4_2']  = _conv2d_relu(graph['conv4_1'], 21, 'conv4_2')
    graph['conv4_3']  = _conv2d_relu(graph['conv4_2'], 23, 'conv4_3')
    graph['conv4_4']  = _conv2d_relu(graph['conv4_3'], 25, 'conv4_4')
    graph['avgpool4'] = _avgpool(graph['conv4_4'])
    graph['conv5_1']  = _conv2d_relu(graph['avgpool4'], 28, 'conv5_1')
    graph['conv5_2']  = _conv2d_relu(graph['conv5_1'], 30, 'conv5_2')
    graph['conv5_3']  = _conv2d_relu(graph['conv5_2'], 32, 'conv5_3')
    graph['conv5_4']  = _conv2d_relu(graph['conv5_3'], 34, 'conv5_4')
    graph['avgpool5'] = _avgpool(graph['conv5_4'])
    return graph


def run():
    sess = tf.InteractiveSession()

    content_image = load_image(CONTENT_IMAGE)
    style_image = load_image(STYLE_IMAGE)
    input_image = generate_noise_image(content_image)

    model = load_vgg_model(VGG_MODEL)


    sess.run(tf.global_variables_initializer())

    sess.run(model['input'].assign(content_image))
    content_loss = content_loss_func(sess, model)

    sess.run(model['input'].assign(style_image))
    style_loss = style_loss_func(sess, model)

    total_loss = ALPHA * content_loss + BETA * style_loss


    sess.run(model['input'].assign(input_image))

    optimizer = tf.train.AdamOptimizer(2.0)
    train_step = optimizer.minimize(total_loss)

    sess.run(tf.global_variables_initializer())
    sess.run(model['input'].assign(input_image))

    now = datetime.now()
    case = "result/{:.3f}".format(ALPHA/BETA)+"_"+str(ITERATIONS)+"_"+now.strftime("%Y%m%d_%H%M%S")

    if not os.path.exists("result"):
        os.mkdir("result")

    if not os.path.exists(case):
        os.mkdir(case)

    if not os.path.exists(case+"/output"):
        os.mkdir(case+"/output")

    save_image(case+"/1.content"+CONTENT_IMAGE[CONTENT_IMAGE.rfind('.'):], content_image)
    save_image(case+"/2.style"+STYLE_IMAGE[STYLE_IMAGE.rfind('.'):], style_image)

    file = open(case+"/Log.txt", "a")
    log(file, now)

    for it in range(ITERATIONS+1):
        sess.run(train_step)
        save_it = 1

        if it<10 :
            save_it = 1
        elif it<100 :
            save_it = 5
        elif it<1000 :
            save_it = 10
        else :
            save_it = 100

        if it%save_it == 0:
            mixed_image = sess.run(model['input'])
            file.write('Iteration %d\n' % (it))
            file.write('sum : ' + str(sess.run(tf.reduce_sum(mixed_image))) + "\n")
            file.write('cost: ' + str(sess.run(total_loss)) + "\n\n")

            filename = case+'/output/%04d.png' % (it)
            save_image(filename, mixed_image)

    save_image(case+"/3.result.png", mixed_image)
    file.close()
    sess.close()
    return case



def makeAnimatedGif(case):

    """
    image files must be sorted

    """
    
    imgFiles = glob(case+"/output/*.png")
    images = [Image.open(fn) for fn in imgFiles]
    
    global filename
    filename = case + "/4.out.gif"
    writeGif(filename, images, duration=0.2)
    print("%s has been created at %s." % (filename, os.path.realpath(filename)))

def start(case):
    print("Creating animated gif....")
    makeAnimatedGif(case)
