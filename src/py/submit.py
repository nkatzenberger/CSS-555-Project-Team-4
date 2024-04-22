
import os
from firebase_admin import credentials, initialize_app, storage
# Init firebase with credentials
current_dir = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_dir, '..', 'NewCreds.json')
cloudkeys = credentials.Certificate(credentials_path)
initialize_app(cloudkeys, {'storageBucket': 'eegdata-93ae1.appspot.com'}) #calls to firebasse bucket
def uploadToFirebase(fileName, email = ""):
  if email != "":
    f = email + "/" + fileName
  else:
    f = fileName
  bucket = storage.bucket()
  blob = bucket.blob(f)
  blob.upload_from_filename(fileName) 
  blob.make_public()
  return (blob)

def downloadFile(fileName, folderName):
  bucket = storage.bucket()
  blob = bucket.blob(folderName+"/"+fileName)
  downloadDirectory = os.path.join('./downloadedFiles/', fileName)
  file = blob.download_to_filename(downloadDirectory)
  return(file)