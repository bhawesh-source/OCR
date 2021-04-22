"""
@file main.py A wrapper file for all the engine modules.
@author Himanshu Mishra

This file combines all the functions and modules for the engine.
Pipeline for the task follows:
"""
import os
import sys

def main(image_location):
    """
    Main function to carry all the tasks of the engine.
    @params image_location Location where the image to be processed is stored

    @returns A tuple (status, text)
        status - Determines the status of the processing
        text - String representation of the documented text
    """
    try:
        if os.path.exists(image_location):
            image_found = True
        else:
            raise IOError
    except IOError as e:
        print(f"Exception occurred: {e}")
        return False

    text = "File Found!"
    status = image_found

    #
    # Wrapper Code Begin
    # 

    print("Work under progress!")

    #
    # Wrapper Code Ends
    #
    
    return status, text

    


    text = "*** Empty text ***"
    return text

if __name__ == "__main__":
    print("Caution: This file is meant to be used as an API and not a standalone application. Even so if you want to use it standalone then:")
    print("Remember as a result of running this application standalone, it will display the processed content on the console.")
    
    if len(sys.argv) != 2:
        print("Usage: filename <image_location>")

    image_location = sys.argv[0]
    text = main(image_location)

    if text == False:
        print("Could not find image!")
        exit()


    print("Processed Text: ")
    print(text)




