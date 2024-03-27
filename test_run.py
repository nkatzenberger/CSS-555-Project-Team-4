import unittest
from run import convertToBB
import os

class TestConvertToBB(unittest.TestCase):

    def test_convertToBB(self):
        # Test data
        filename = "Test_result_evoked_LA.mat"
        
        # Call the function
        convertToBB(filename)
        
        # Assert that the output file exists
        self.assertTrue(os.path.exists("converted.txt"))
        
        # Clean up: delete the output file
        os.remove("converted.txt")

if __name__ == "__main__":
    unittest.main()