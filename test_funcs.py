import unittest
import submit
from firebase_admin import storage

class testUpload(unittest.TestCase):
    def test_submit(self):
        file_names = ["/data/evoked_eeg_RV.mat", "/data/evoked_eeg_RA.mat", "/data/evoked_eeg_LV.mat", "/data/evoked_eeg_LA.mat"]
        for file in file_names:
            blob1 = submit.uploadToFirebase(file)
            bucket = storage.bucket()
            blob2 = bucket.blob(file)
            blob2.download_to_filename("./data/down.mat")        
            self.assertEqual(blob1.name, blob2.name)
        
if __name__ == "__main__":
    unittest.main()