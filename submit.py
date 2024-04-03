
from firebase_admin import credentials, initialize_app, storage
# Init firebase with credentials

def uploadToFirebase(f):
  cloudkeys = credentials.Certificate("./NewCreds.json")
  initialize_app(cloudkeys, {'storageBucket': 'eegdata-93ae1.appspot.com'}) #calls to firebasse bucket

  fileName = f 
  bucket = storage.bucket()
  blob = bucket.blob(fileName)
  blob.upload_from_filename(fileName) 
  blob.make_public()
  #print("your file at the url", blob.public_url, "was uploaded successfully")
  return (blob)
#Removed Smells: Too many comments and bad variable names