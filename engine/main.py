"""
@file main.py Main file for engine module.
@author Himanshu Mishra
"""
import os
import src.util as util
import tensorflow as tf
import sys

import sys

import util
from wordext import main as wx
import charseg as cs
import charclf as cf
# import tensorflow as tf

CHAR_DIR = "images/e/"
MODEL = "models/20210427-03301619494256-final-train.h5"

def main(imageLocation):
    model = util.load_model(MODEL)
    lines = wx(imageLocation)
    t = ""
    for line in lines:
        l = ""
        for word in line:
            cs.main(word)
            l += cf.main(model) + " "
        t += l + "\n"
    return t


if __name__ == "__main__":
    print("Main file: ")
    # imageLocation = CHAR_DIR + os.listdir(CHAR_DIR)[0]
    # test_batch = util.create_data_batches([imageLocation], test_data=True)
    # model = util.load_model(MODEL)
    # predictions = model.predict(test_batch)
    #
    # str = ""
    # for p in predictions:
    #     s = util.get_pred_label(p)
    #     str += s

    imageLocation = sys.argv[1]
    text = main(imageLocation)
    print("Result: " + text)

    # print(str)
    exit(0)




