import unittest
import submit
from firebase_admin import storage

class testUpload(unittest.TestCase):
    def test_submit(self):
        blob1 = submit.uploadToFirebase("evoked_eeg_RV.mat")
        bucket = storage.bucket()
        blob2 = bucket.blob("evoked_eeg_RV.mat")
        blob2.download_to_filename("./down.mat")        
        self.assertEqual(blob1.name, blob2.name)

if __name__ == "__main__":
    unittest.main()