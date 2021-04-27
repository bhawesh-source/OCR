"""
@file main.py Main file for engine module.
@author Himanshu Mishra
"""
import os
import src.util as util
import tensorflow as tf
import sys


CHAR_DIR = "images/e/"
MODEL = "models/20210420-06461618901219-all-images-Adam.h5"

if __name__ == "__main__":
    imageLocation=sys.argv[1]
    print (imageLocation)
    if os.path.exists(imageLocation):
        # imageLocation = CHAR_DIR + os.listdir(CHAR_DIR)[0]
        print("1")
        test_batch = util.create_data_batches([imageLocation], test_data=True)
        print("2")
        model = util.load_model(MODEL)
        print("3")
        predictions = model.predict(test_batch)
        print("4")

        str = ""
        for p in predictions:
            s = util.get_pred_label(p)
            str += s

        print("result"+str)
    else:
        print ("location not found")




