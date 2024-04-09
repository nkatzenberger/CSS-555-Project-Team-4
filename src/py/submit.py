
import os
from firebase_admin import credentials, initialize_app, storage
# Init firebase with credentials
current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_dir, '..', 'NewCreds.json')
cloudkeys = credentials.Certificate(credentials_path)
initialize_app(cloudkeys, {'storageBucket': 'eegdata-93ae1.appspot.com'}) #calls to firebasse bucket
def uploadToFirebase(f):
  fileName = f 
  bucket = storage.bucket()
  blob = bucket.blob(fileName)
  blob.upload_from_filename(fileName) 
  blob.make_public()
  #print("your file at the url", blob.public_url, "was uploaded successfully")
  return (blob)
#Removed Smells: Too many comments and bad variable names