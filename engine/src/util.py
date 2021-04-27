"""
@file util.py
@author Himanshu Mishra

This module contains all the utility functions required by other modules.
All the plotting and displaying features are included with this module.
"""
# Necessary libraries
import os
import sys
import string
import cv2 as cv  # OpenCV library used for image processing
import numpy as np  # Numpy used for numerical calculations
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt  # Matplotlib used for plotting

# Define image size
IMG_SIZE = 224
# Define the batch size, 32 is a good default
BATCH_SIZE = 32
true_labels = {}
letters = []

# --- Reading Image ---
def readImage(imageFile):
    """
    Reads Image from a file location using
    OpenCV.

    @params imageFile Image File Location
    @returns image as numpy array
    """
    image = cv.imread(imageFile)
    return image


# --- Displaying Image ---
def displayImage(image, comments="Test Image"):
    """
    Displays image in a window using OpenCV.

    @params image {numpy array} Image to display
    @params comments {string} Sets the title of the image window 
    """
    cv.imshow(comments, image)
    cv.waitKey(0)

    cv.destroyAllWindows()
    return


# --- Plotting Image ---
def plotImage(image, comments="Test Image", col="gray"):
    """
    Plots image using Matplotlib.

    @params image {numpy array} Image to plot
    @params comments {string} Sets the title of the plot
    @params col {string} Color channel of the image (Gray by default)
    """
    if col == "gray":
        plt.imshow(image, cmap=col)
    else:
        plt.imshow(image)

    plt.title(comments)
    plt.axis("off")
    return


############### Preprocessing of Image ###############

# --- GrayScale Conversion ---
def toGray(image):
    """
    Converts the image to grayscale if not. If already gray skips.

    @params image {numpy array} Image to convert to GrayScale
    @returns grayscale image
    """
    if len(image.shape) > 2:
        image = cv.cvtColor(image, cv.BGR2GRAY)
    return image

# --- Rescaling Image ---
def rescaleImage(image, shape, interpolation=cv.INTER_LINEAR):
    """
    Rescales the given image to the given shape using the given interpolation.

    @params image {numpy array} Image to rescale
    @params shape {(h,w) tuple} Shape of the final image
    @params interpolation {OpenCV method} Interpolation to use (LinearInterpolation by default)

    @returns rescaled image
    """
    rescale = cv.resize(image, shape, interpolation)
    return rescale


# --- Aspect Ratio ---
def getAspectRatio(image):
    """
    Finds the aspect ratio (height / width) of the image.

    @params image {numpy array} image to process
    @returns aspect ratio of the given image
    """
    h, w = image.shape[0], image.shape[1]
    return h / w


# --- Reshape Image ---
def reshape(image, height=224):
    """
    Finds the new shape of the image when height is changed to the given height maintaining the aspect ratio.

    @params image {numpy array} image to reshape
    @params height {integer} new height of the image (128 by default)

    @returns new shape of the image
    """
    shape = (height, int(height * getAspectRatio(image)))
    return shape


############### Contours ###############

# --- Draw Contours ---
def drawContour(image, cnt, num):
    """
    Draws a bounded rectangle around the contour passed and puts the given text into the rectangle.

    @params image {numpy array} Image to draw contour on.
    @params cnt {numpy array} Contour to bound
    @params num {string / integer} Text to put in
    """
    M = cv.moments(cnt)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # drawing the contour number on the image
    cv.putText(image, f"{num + 1}", (cX - 20, cY), cv.FONT_HERSHEY_PLAIN, \
               1.0, (255, 128, 0), 1)
    x, y, w, h = cv.boundingRect(cnt)
    cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
    return image

def drawAllContours(image, contours):
    """

    Draws a bounded rectangle around all the contours passed and puts an index to each.

    :param image: {numpy array} image to draw contours on
    :param contours: {list} list of all contours to be drawn
    :return: image with contours drawn on it
    """
    for i, cnt in enumerate(contours):
        M = cv.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # drawing the contour number on the image
        cv.putText(image, f"{i + 1}", (cX - 20, cY), cv.FONT_HERSHEY_PLAIN,\
                   1.0, (255, 128, 0), 1)
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)

    return image


# --- Plot All Lines ---
def plotAllLines(image, lines, comments="All lines"):
    """
    Plots all lines
    """
    image_rect = rescaleImage(image, reshape(image))
    lineCount = 0
    for line in lines:
        for word in line:
            drawContour(image_rect, word, lineCount)
        lineCount += 1

    displayImage(image_rect, comments)

# --- Plot All Words ---
def plotAllWords(image, lines, comments="Final Result"):
    """
    Plots all the words in order.
    """
    wordCount = 0
    image_rect = rescaleImage(image.copy(), reshape(image))

    for words in lines:
        for word in words:
            drawContour(image_rect, word, wordCount)
            wordCount += 1

    # plotImage(image_rect, comments)
    displayImage(image_rect, comments)

# --- Display All Words ---
def displayAllWords(lines, comments="All Words"):
    """
    Displays all the words in reading order one by one.
    """
    wordCount = 0
    for line in lines:
        for word in line:
            displayImage(word, str(wordCount))
            wordCount += 1

    return

# --- Save All Words ---
def saveAllWords(lines, dir):
    """
    Saves all the words in the given directory.
    """
    wordCount = 0
    for line in lines:
        for word in line:
            wordFile = dir + "/" + str(wordCount) + ".png"
            # print(f"Word File: {wordFile}")
            # print(os.listdir(dir + "/.."))

            cv.imwrite(wordFile, word)
            # cv.imwrite()
            wordCount += 1
    return

# --- Save All Characters ---
def saveAllChars(chars, dir):
    """
    Saves all the character images in the given directory.
    """
    for i,c in enumerate(chars):
        charFile = dir + "/" + str(i) + ".png"
        cv.imwrite(charFile, c)

    return


# Plotting the graph obtained
def plotGraph(graph):
    """
    Plots the given graph.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(graph)


def segmentImage(image, segment_array, c='g'):
    """
    Segments the given image at the positions in the given array.
    @param c Color of the segmented lines
    """
    for x in segment_array:
        image[:,x] = (0,255,0)

    displayImage(image, "Segmented Image")


def plotDualGraphs(graph1, graph2, c2='g'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(graph1)
    ax.plot(graph2, color=c2)
    return fig, ax

# ---------- MODEL ----------
# Importing the model
def load_model(model_path):
  """
  Loads a saved model from a specified path.
  """
  print(f"Loading saved model from: {model_path}")
  model = tf.keras.models.load_model(model_path,
                                     custom_objects={"KerasLayer":hub.KerasLayer})
  return model



def process_image(image_path):
    """
    Takes an image file path and turns it into a Tensor.
    """
    # Read in image file
    image = tf.io.read_file(image_path)

    # Preprocess the image
#     image = preprocess_image(image_path)

    # Turn the jpeg image into numerical Tensor with 3 color channels
    image = tf.image.decode_jpeg(image, channels=3)
    # Convert the colour channel values from 0-255 values to 0-1 values
    image = tf.image.convert_image_dtype(image, tf.float32)

    # Resize the image to our desired size (224, 224)
    image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])
    return image

def get_image_label(image_path, label):
    """
    Takes an image file path name and the associated label,
    processes the image and returns a tuple of (image, label).
    """
    image = process_image(image_path)
    return image, label


# Create a function to turn data into batches
def create_data_batches(x, y=None, batch_size=BATCH_SIZE, valid_data=False, test_data=False):
    """
    Create batches of data out of image (x) and label (y) pairs.
    Shuffles the data if it's training data but doesn't shuffle it if it is the validation data.
    Also accepts test data as input (no labels)
    """
    # If the data is a test dataset, we probably don't have labels
    if test_data:
        print("Creating test data batches...")
        data = tf.data.Dataset.from_tensor_slices(tf.constant(x)) # Only file paths
        data_batch = data.map(process_image).batch(batch_size)
        return data_batch

    elif valid_data:
        print("Creating validation data batches...")
        data = tf.data.Dataset.from_tensor_slices((tf.constant(x), # file paths
                                                   tf.constant(y)))# labels
        data_batch = data.map(get_image_label).batch(batch_size)
        return data_batch

    else:
        # If the data is a training dataset, we shuffle it
        print("Creating training data batches...")
        # Turn filepaths and labels into Tensors
        data = tf.data.Dataset.from_tensor_slices((tf.constant(x), # filepaths
                                                   tf.constant(y)))# labels

        # Shuffling pathnames and labels before mapping image processing function,
        # this is done to reduce the time required (less dense data = less time taken).
        data = data.shuffle(buffer_size=len(x))

        # Create (image, label) tuples (this also turns image path into preprocessed image)
        data = data.map(get_image_label)

        # Turn the data into batches
        data_batch = data.batch(batch_size)
    return data_batch

def runparam():
    for i, s in enumerate(string.ascii_uppercase):
        letters.append(s)
        true_labels[s] = np.zeros((26))
        true_labels[s][i] = 1
def unroll_label(label):
    """
    Utility function used to unroll (get letter) from
    the given label
    """
    runparam()
    return letters[np.argmax(label)]

# Turn prediction probabilities into their respective label (easier to understand)
def get_pred_label(prediction_probabilities):
  """
  Turns an array of prediction probabilities into a label.
  """
  return unroll_label([np.argmax(prediction_probabilities) == i for i in range(26)])
