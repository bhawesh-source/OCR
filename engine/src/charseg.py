"""
@file: charseg.py Module used to segment the characters of a word image.
@author: Himanshu Mishra

This module segments a word image into its components characters. This module is an
implementation of the `Efficient Character Segmentation` Algorithm proposed in

`https://www.researchgate.net/publication/
334239408_An_Efficient_Character_Segmentation_Algorithm_for_Connected_Handwritten_Documents`
"""
# ---------- Necessary Imports - Begin ----------
import os
import sys
import util
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
# ---------- Necessary Imports - Ends ----------

# ---------- PreProcessing Image - Begin ----------
def preprocess(image):
    """
    Preprocesses image for clarity and proper distinction of characters.
    This method performs: GrayScale Conversion, Rescaling, Noise Reduction,
    Image Thresholding and Skeletonization.

    :param image: {numpy array} Image to preprocess
    :return: {numpy array} PreProcessed image
    """
    # ColorSpace Conversion
    if len(image.shape) > 2:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray = image

    # Rescaling
    rescaled = util.rescaleImage(gray, util.reshape(gray, height=512),\
                                 interpolation=cv.INTER_CUBIC)
    # Noise Reduction
    blur = cv.GaussianBlur(rescaled, (5, 5), 0)
    # Image Thresholding
    thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                  cv.THRESH_BINARY_INV, 11, 2)
    # Skeletonization
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv.erode(thresh, kernel, iterations=1)

    dilation = cv.dilate(erosion, kernel, iterations=1)

    return thresh
# ---------- PreProcessing Image - End ----------


# ---------- Pixel Count Graph Formation - Begin ----------
def pixelCount(image, axis = 0):
    """
    Finds the pixel count of the image along the given axis.
    Axis 0: Vertical, Axis 1: Horizontal

    :param image: {numpy array} image to find the pixel count of
    :param axis: {integer} direction of finding the pixel count
    :return: {numpy array} pixel count along the given direction
    """
    return np.sum(image, axis= axis)

def binarizeCount(pixels, min=0, max=1000, threshold=20):
    """
    Binarizes the given pixel count to reduce minor fluctuations of the peak.
    This method is used to get consistency in the peak values in the image.

    :param pixels: {numpy array} pixel count to binarize
    :param min: {integer} lower limit of the binary value
    :param max: {integer} upper limit of the binary value
    :param threshold: {integer} threshold to use for binarization

    :return: {numpy array} binarized pixel count of the image
    """
    binary = np.zeros(len(pixels))
    for i, px in enumerate(pixels):
        if px > threshold:
            binary[i] = max
        else:
            binary[i] = min

    return binary
# ---------- Pixel Count Graph Formation - End ----------

# ---------- Peak Extraction & Flagging - Begin ----------
def getPeaks(binary):
    """
    Finds out each peaks x coordinate (start, end) given the binary
    pixel count of the image

    :param binary: {numpy array} Binary pixel count of the given image
    :return: {tuple} (All peaks {list}, Peak Widths {list})
    """
    peaks, widths, found, leftEnd = [], [], False, -1
    max = np.max(binary)
    for i in range(len(binary)):
        if binary[i] == max:
            if found == True:
                continue
            found = True
            leftEnd = i
        else:
            if found == True:
                peaks.append((leftEnd, i))
                widths.append(i-leftEnd)
                found = False

    return (peaks, widths)

def flagged(widths, k = 0.5):
    """
    Finds the flags for each peak to identify the false peaks. This method uses the
    mean width comparision technique.

    :param widths: {numpy array} Widths of each peaks
    :return: {numpy array} Flags for each of the corresponding peaks
    """
    flags, avg = [], np.mean(widths)
    for w in widths:
        if w > avg * k:
            flags.append(1)
        else:
            flags.append(0)

    return flags
# ---------- Peak Extraction & Flagging - End ----------

# ---------- Merging Peaks - Begin ----------
def enumeration(peaks, flags):
    """
    Enumerates flags to find the potential peaks to be merged together.
    This method is called as a solution to the oversegmentation
    problem.

    :param peaks: {list of tuples} Peaks of pixel values in the image
    :param flags: {list} Flags corresponding to each peak
    :return: {list} Candidates qualifying for merge
    """
    candidates = []
    for i, f in enumerate(flags):
        if i >= len(flags) - 1 or f == 1:
            continue
        fnext = flags[i + 1]
        # Case 1: Next flag is marked 0
        if fnext == 0:
            candidates.append((i, i + 1))
            flags[i + 1] = 1
            continue

        # Case 2: Adjacent flags are 1
        d1, d2 = 1000, peaks[i + 1][0] - peaks[i][1]
        if i - 1 >= 0:
            d1 = peaks[i][0] - peaks[i - 1][1]
        if d1 < d2:
            candidates.append((i - 1, i))
        else:
            candidates.append((i, i + 1))

    return candidates

def merge(candidates, peaks, binary):
    """
    Merges the peaks that qualifies for merge. This method is the continuation
    to the solution of the oversegmentation problem.

    :param candidates: {list} Candidates qualifying for merge
    :param peaks: {list of tuples} List of peaks end coordinates
    :param binary: {numpy array} Binarized pixel count graph

    :return: {numpy array} new binary pixel graph
    """
    max = np.max(binary)
    for i, j in candidates:
        x1, x2 = peaks[i][1], peaks[j][0]
        for x in range(x1, x2 + 1):
            binary[x] = max
    return binary
# ---------- Merging Peaks - End ----------

# ---------- PSC Extraction - Begin ----------
def troughs(peaks):
    """
    Finds out the trough values given the peaks end points.
    This method finds the centre coordinate between two peaks.

    :param peaks: {list of tuples} List of end points for each peak
    :return: {list} List of troughs centre coordinate in the image
    """
    troughs = []
    for i in range(len(peaks) - 1):
        x1, x2 = peaks[i][1], peaks[i + 1][0]
        troughs.append(int((x1 + x2) / 2))
    return troughs

def ridFalsePSC(troughs, pixels, threshold = 1):
    """
    Finds out the true Potentially Segmented Column (PSC) given the troughs
    and the original pixel count in the image. This method is used to
    eliminate the false PSC values and obtain the true ones.

    :param troughs: {list} List of trough centre coordinates in the image
    :param pixels: {numpy array} Array of pixel count for the image
    :param threshold: {integer} Threshold value for true PSC

    :return: {list} A list of true PSC values which could be used for image segmentation
    """
    psc = []
    for v in troughs:
        if pixels[int(v)] > threshold:
            continue
        psc.append(int(v))
    return psc
# ---------- PSC Extraction - End ----------

# ---------- Segmentation - Begin ----------
def charSeg(image, psc):
    """
    Segments the given image by the psc values.

    :param psc: {list} List of PSC values
    :return: {list} List of segmented characters as image
    """
    begin, end = 0, image.shape[1]
    print(end)

    psc.append(end)
    chars = []
    for i in range(len(psc)):
        if i == 0:
            chars.append(image[:,begin:psc[i]])
        else:
            chars.append(image[:,psc[i-1]:psc[i]])

    return chars

# ---------- Segmentation - End ----------

# ---------- Wrapper - Begin ----------
def main(image):
    """
    A Wrapper function for all the methods in the module. Performs all the
    character segmentation steps sequentially.

    :param image: {numpy array} Image for which to segment characters
    :return: {list} List of segmented character images
    """
    # Preprocessing the image for better clarity
    preprocessed = preprocess(image)
    ## Displaying the preprocessed image
    util.displayImage(preprocessed, "Preprocessed Image")

    # Finding the vertical pixel count of the image
    pixels = pixelCount(preprocessed)
    # Binarizing the vertical pixel count of the image
    binary = binarizeCount(pixels)
    # Finding the peaks and widths from the binary graph
    peaks, widths = getPeaks(binary)
    # Marking the flag values for the peaks
    flags = flagged(widths)
    # Finding the qualified peak candidates for merging together
    candidates = enumeration(peaks, flags)
    # Obtaining the new binary pixel count graph
    n_binary = merge(candidates, peaks, binary)
    # Obtaining peaks and widths of the new binary graph
    n_peaks, n_widths = getPeaks(n_binary)
    # Obtaining the trough centres for the graph
    trough = troughs(n_peaks)
    # Eliminating the false PSC and obtaining the true values
    psc = ridFalsePSC(trough, pixels)

    ## Displaying the image to be segmented with their positions
    image_seg = util.rescaleImage(image, util.reshape(image, height=512), interpolation=cv.INTER_CUBIC)
    util.segmentImage(image_seg, psc)

    # Segmenting the image into individual characters
    chars  = charSeg(image_seg, psc)
    return chars

# ---------- Wrapper - End ----------

if __name__ == "__main__":
    """
    This module when used as a standalone application, displays the word image with 
    potential segmentation lines. As a parameter it accepts a word image location.
    """
    print(f"Caution: Standalone usage of the module!!!")
    # If ImageLocation not passed as an argument to the module call.
    if len(sys.argv) != 2:
        print(f"Critical Error: Argument Error!")
        print(f"Usage: {sys.argv[0]} <image_location>")
        exit(1)

    imageLocation = sys.argv[1]

    # Reading Image from file
    image = util.readImage(imageLocation)
    # Finding all the different characters in the image
    characters = main(image)

    # Displaying all the characters one by one
    for i, c in enumerate(characters):
        util.displayImage(c, str(i))

    # charDir = "../images/chars/test_sample/case"
    # util.saveAllChars(characters, charDir)
    exit(0)