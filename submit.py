from firebase_admin import credentials, initialize_app, storage
# Init firebase with credentials
cloudkeys = credentials.Certificate("./NewCreds.json")
initialize_app(cloudkeys, {'storageBucket': 'eegdata-93ae1.appspot.com'}) #calls to firebasse bucket
def uploadToFirebase(f):
  fileName = f 
  bucket = storage.bucket()
  blob = bucket.blob(fileName)
  blob.upload_from_filename(fileName) 
  blob.make_public()
  #print("your file at the url", blob.public_url, "was uploaded successfully")
  return (blob)
