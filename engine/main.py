"""
@file main.py Main file for engine module.
@author Himanshu Mishra
"""
import os
import src.util as util
import tensorflow as tf

CHAR_DIR = "images/e/"
MODEL = "models/20210420-06461618901219-all-images-Adam.h5"

if __name__ == "__main__":
    print("Main file: ")
    imageLocation = CHAR_DIR + os.listdir(CHAR_DIR)[0]
    test_batch = util.create_data_batches([imageLocation], test_data=True)
    model = util.load_model(MODEL)
    predictions = model.predict(test_batch)

    str = ""
    for p in predictions:
        s = util.get_pred_label(p)
        str += s

    print(str)





