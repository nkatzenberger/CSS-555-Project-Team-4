import unittest
import submit
from firebase_admin import storage
import os

class testUpload(unittest.TestCase):
    def test_submit(self):
        base_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        file_names = ["evoked_eeg_RV.mat", "evoked_eeg_RA.mat", "evoked_eeg_LV.mat", "evoked_eeg_LA.mat"]
        for file_name in file_names:
            file_path = os.path.join(base_dir, file_name)
            blob1 = submit.uploadToFirebase(file_path)
            bucket = storage.bucket()
            blob2 = bucket.blob(blob1.name)
            download_path = os.path.join(base_dir, 'down.mat')
            blob2.download_to_filename(download_path)     
            self.assertEqual(blob1.name, blob2.name)
        
if __name__ == "__main__":
    unittest.main()