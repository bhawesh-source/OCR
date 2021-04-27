"""
@file: charclf.py Character Classification Module
@author: Himanshu Mishra

This module classifies the different character images into one of the
26 English Uppercase Alphabets. This module has used a pretrained
model as a classifier and classifying is as simple as calling the
`predict` method of the model.
"""
# ---------- Necessary Libraries - Begin ----------
import os
import sys
import util
import cv2 as cv
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
# ---------- Necessary Libraries - End ----------

# ---------- Initializing MetaData - Begin ----------
IMG_SIZE = 224
BATCH_SIZE = 32
# ---------- Initializing MetaData - End ----------



# ---------- Loading the model - Begin ----------
def loadModel(modelPath, custom_objects):
    """
    This method loads the model from the given model path with the given
    custom objects.

    :param modelPath: {string} Path of model (model's location)
    :param custom_objects: {dictionary} Custom objects associated with the model
    :return: model object
    """
    print(f"Loading saved model from: {modelPath}")
    model = tf.keras.models.load_model(modelPath, custom_objects=custom_objects)
    return model
# ---------- Loading the model - End ----------

# ---------- Preprocessing Image - Begin ----------
def preprocess(imageFile):
    """
    This method converts image into tensors. It also performs GrayScale Conversion,
    Rescaling, Noise Reduction and Image thresholding.
    :param image:
    :return:
    """
    image = cv.imread(imageFile)
    image = cv.resize(image, (IMG_SIZE, IMG_SIZE))
    util.displayImage(image)

    image = tf.convert_to_tensor(image, dtype=tf.float32)
    image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])
    return image

# ---------- Preprocessing Image - End ----------

# ---------- Creating Data Batches - Begin ----------
def createBatches(data, batchSize = BATCH_SIZE):
    """
    This method creates batches from the data. Creating batches is necessary
    for efficient performance. It reduces the chances of server crashing.

    :param data: Data to batchify
    :param batchSize: Size of the batch
    :return: data batch
    """
    data = tf.data.Dataset.from_tensor_slices(tf.constant(data))
    dataBatch = data.map(preprocess).batch(batchSize)
    return dataBatch
# ---------- Creating Data Batches - End ----------

# ---------- Wrapper Function - Begin ----------
def main(imageList):
    """
    A wrapper function for all the methods of the module. This function
    performs text classification on the given image list.

    :param imageList: {list} List of images to classify
    :return: {string} String representation of the classified image text
    """
    print(f"Data Tensor: {tf.constant(imageList)}")
    data_batch = createBatches(imageList)
    print(f"Data Batch Summary: {data_batch.element_spec}")

    a = np.arange(10)
    data = tf.data.Dataset.from_tensor_slices(tf.constant(a))
    data_batch = data.batch(32)



# ---------- Wrapper Function - End ----------

# ---------- Standalone Usage ----------
if __name__ == "__main__":
    """
    This module when used as a standalone application, displays the text of the image
    as a string on the terminal.
    """
    print(f"Caution: Standalone usage of the module!!!")
    # If ImageLocation not passed as an argument to the module call.
    if len(sys.argv) != 2:
        print(f"Critical Error: Argument Error!")
        print(f"Usage: {sys.argv[0]} <image_location>")
        exit(1)

    imageDir = sys.argv[1]
    imageFiles = [imageDir + "/" + imFile for imFile in os.listdir(imageDir)]

    # images = [util.readImage(imFile) for imFile in imageFiles]

    print(f"Images: {imageFiles}")
    print(f"File Tensors: {tf.constant(imageFiles)}")
    print(f"Image Tensors: {tf.constant(cv.imread(imageFiles[0]))}")


    # text = main(images)


