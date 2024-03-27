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
        
        # Assert that the content of the output file is as expected
        with open("converted.txt", "r") as file:
            content = file.read()
            # Add assertions for the expected content here
            # For example:
            # self.assertIn("expected_string_in_file", content)
        
        # Clean up: delete the output file
        os.remove("converted.txt")

if __name__ == "__main__":
    unittest.main()