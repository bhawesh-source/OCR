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
import charseg as cs

# MODEL_PATH = "models/20210420-06461618901219-all-images-Adam.h5"
MODEL_PATH = "models/20210427-03301619494256-final-train.h5"
CHAR_DIR = cs.CHAR_DIR
# ---------- Extracting Text from Predictions ----------
def extractText(predictions):
    text = ""
    for pred in predictions:
        char = util.get_pred_label(pred)
        text += char
    return text

# ---------- Wrapper Function - Begin ----------
def main(model):
    """
    A wrapper function for all the methods of the module. This function
    performs text classification on the given image list.

    :return: {string} String representation of the classified image text
    """
    # Getting character file path
    imageFiles = [CHAR_DIR + imFile for imFile in os.listdir(CHAR_DIR)]
    # Creating batches of data
    data_batch = util.create_data_batches(imageFiles, test_data=True)

    # Making Predictions
    predictions = model.predict(data_batch)
    # Extracting text out of predictions
    text = extractText(predictions)

    return text
# ---------- Wrapper Function - End ----------

# ---------- Standalone Usage ----------
if __name__ == "__main__":
    """
    This module when used as a standalone application, displays the text of the image
    as a string on the terminal.
    """
    print(f"Caution: Standalone usage of the module!!!")
    # If ImageLocation not passed as an argument to the module call.
    if len(sys.argv) != 1:
        print(f"Critical Error: Argument Error!")
        print(f"Usage: {sys.argv[0]}")
        exit(1)
    # Loading the model
    model = util.load_model(MODEL_PATH)
    text = main(model)
    print(f"Resulting text: " + text)




