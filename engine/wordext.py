"""
@file wordext.py This module contains the word extraction features of the engine.
@author Himanshu Mishra

This module has extensively used OpenCV. The algorithm used to extract words out of a
text image is `Contour Approximation Method`. The entire module has been implemented
by the author. This module is to be used only for educational purposes and not for
production.
"""
import os
import sys
import util
import cv2 as cv
import numpy as np

# --- Preprocessing the image ---
def preprocess(image):
    """
    Preprocesses the image for better quality and contrast. This function performs
    GrayScale Conversion, Noise Reduction & Image Thresholding. All of which uses
    OpenCV methods.

    :param image: Image to preprocess
    :return: The preprocessed image
    """
    # GrayScale Conversion
    if len(image.shape) > 2:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    else:
        gray = image
    # Image Rescaling
    rescaled = util.rescaleImage(gray, util.reshape(gray))
    # Noise Reduction
    blur = cv.GaussianBlur(rescaled, (5, 5), 0)
    # Image Thresholding
    thresh = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                  cv.THRESH_BINARY_INV, 11, 2)

    return thresh

# --- Dilating the image ---
def dilate(image):
    """
    Dilates the image increasing the stroke width of the characters in turn
    merging them together. This method is used to join all the characters
    of a word together, hence connecting entire word into a single unit.

    Caution: This method is to be used with caution as overdoing it may
    result in combining two different words (or even two lines).

    :param image: Image to dilate
    :return: The dilated image
    """
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(image, kernel, iterations=1)

    return dilate

# --- Contour Approximation ---
def contourApx(image):
    """
    Finds all the contours in the image and returns those above a threshold.

    **Contours** are essentially the connected regions in an image. This method
    is used after dilation of the image. This ensures that we get different
    contours for each words. Limiting them to be above a threshold ensures
    that we only get word contours, eliminating any noise in the image.

    :param image: Dilated Image
    :return: All the contours above a threshold in the image
    """

    contours, hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Limiting contours above a threshold (Threshold assigned as the mean of the areas of all contours)
    # threshold = np.mean([cv.contourArea(cnt) for cnt in contours])
    threshold = 50

    return [cnt for cnt in contours if cv.contourArea(cnt) > threshold]

# --- Extract Lines out of Contours ---
def extractLines(contours, thresh = 30):
    """
    Extracts lines out of the given contours in reading order. Essentially this method
    sorts the given contour list in reading order from top to bottom. A custom algorithm
    is used for getting higer accuracy results.

    :param contours: Contour list for all the words in the text
    :return: A 2D list of contours each representing a word. The 1st dimension contains all
    the lines in sorted order. The 2nd dimension contains a list of all the words in the
    line in random order.
    """
    # Get mid values for all contours
    mark = []
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        mid = int(y + h / 2)
        mark.append(mid)

    # Find the correct line mark (r_mark) for text
    # Adjust by a threshold
    r_mark = []
    for m in mark:
        d = m // thresh
        r_mark.append(thresh * d)

    # Map right lines to contour index
    mapping = {}
    for i, v in enumerate(r_mark):
        if v in mapping:
            mapping[v].append(i)
        else:
            mapping[v] = [i]

    # Get right line index ordered
    lines = []
    for i in sorted(mapping):
        lines.append(mapping[i])

    # Get right line contours
    a_lines = []
    for line in lines:
        a_lines.append([contours[i] for i in line])

    return a_lines

# --- Word Extraction ---
def extractWords(lines):
    """
    Extracts words in reading order for each lines.

    :param lines: 2D list containing lines in the 1st dimension and words in
    the line in 2nd dimension
    :return: A sorted 2D list of words in reading order.
    """
    f_lines = []
    for line in lines:
        mid_dict = {}
        for i, cnt in enumerate(line):
            x, y, w, h = cv.boundingRect(cnt)
            mid = int(x + w / 2)
            mid_dict[mid] = i

        words = []
        for v in sorted(mid_dict):
            words.append(line[mid_dict[v]])
        f_lines.append(words)

    return f_lines

# --- Extract Word ROI ---
def extractROI(lines, image):
    """
    Extracts the Region of Interest (ROI) from the given lines as a list of ordered words
    in reading order.

    :param lines: {2D list} Containing words in reading order
    :param image: {numpy array} Image to extract ROI from
    :return: {2D list} Containing the ROI for each word
    """
    rList = []
    for line in lines:
        wList = []
        for word in line:
            x, y, w, h = cv.boundingRect(word)
            wList.append(image[y:y+h, x:x+w])
        rList.append(wList)

    return rList


# --- Wrapper Function of the module ---
def main(imageLocation):
    """
    Main Wrapper function of the module. This function performs a sequential execution of the algorithm used to implement the Word Extraction Feature of the system.

    @params imageLocation {string} Contains the location of the image to work on
    @returns A 2D list of words, where 1st dimension represents lines in the text and 2nd dimension represents words in the lines.
    """
    try:
        locationFound = os.path.exists(imageLocation)
    except Exception as e:
        print(f"Exception occurred: {e}")
        return

    # 1. Reading the image from file
    image = util.readImage(imageLocation)
    # 2. Preprocessing the image to make it ready for word extraction
    preprocessed = preprocess(image)
    # 3. Dilating the image to merge the characters of a word together
    dilated = dilate(preprocessed)
    # 4. Finding all the contours containing a word in the image
    contours = contourApx(dilated)

    # ## Displaying the contours in the image --- (to be used for debugging)
    # image_rect = util.rescaleImage(image.copy(), util.reshape(image))
    # util.displayImage(util.drawAllContours(image_rect, contours), "All word contours")

    # 5. Extracting lines out of the contours
    lines = extractLines(contours)

    # ## Displaying all the lines in the image --- (to be used for debugging)
    # image_rect = util.rescaleImage(image.copy(), util.reshape(image))
    # util.plotAllLines(image_rect, lines, "All lines in reading order")

    # 6. Extracting words out of lines
    words = extractWords(lines)

    # ## Displaying all the words in the image --- (to be used for debugging)
    # image_rect = util.rescaleImage(image.copy(), util.reshape(image))
    # util.plotAllWords(image_rect, words, "All Words in reading order")

    # 7. Extracting ROI out of the word contours from the image
    image_rect = util.rescaleImage(image.copy(), util.reshape(image))
    wImage = extractROI(words, image_rect)

    return wImage


############### StandAlone Behaviour ###############

if __name__ == "__main__":
    """
    This module when used as a standalone application, displays the extracted words 
    bounded in a rectangle with proper ordering applied to it. The module accepts 
    `Image Location` as an argument and then works on the image.
    """

    print(f"Caution: StandAlone usage of the module!!!")
    # If ImageLocation not passed as an argument to the module call.
    if len(sys.argv) != 2:
        print(f"Critical Error: Argument Error!")
        print(f"Usage: {sys.argv[0]} <image_location>")
        exit(1)

    # Get the image location
    imageLocation = sys.argv[1]
    # Get images for all words
    allWords = main(imageLocation)
    # Display all words one by one
    # util.displayAllWords(allWords)
    #
    # wordDir = "../images/words/test_sample"
    # util.saveAllWords(allWords, wordDir)

    exit(0)


