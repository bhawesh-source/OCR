"""
@file mainTest.py Used for testing the engine `main` module.
@author Himanshu Mishra

This module contains various test cases which the engine `main` must pass.
"""
import unittest as utest 
import main as Main

class TestMain(utest.TestCase):

    def test_location_empty(self):
        """
        Testing for empty image location.
        """
        # Assertion for Empty Location
        self.assertFalse(Main.main(""))

    def test_location_invalid(self):
        """
        Testing  for an invalid location.
        """
        # Assertion for Garbage Location
        image_location = "garbage-xxkkkhhh1245"
        self.assertFalse(Main.main(image_location))

    def test_location_valid(self):
        """
        Testing for a valid location.
        """
        image_location = "data\\images\\test_sample.jpeg"
        status, text = Main.main(image_location)

        self.assertTrue(status)
        # self.assertEqual(text, "File Found!")



if __name__ == "__main__":
    unittest.main()
