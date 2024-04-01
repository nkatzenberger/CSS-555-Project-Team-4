import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCYsmHIkz0iL77uj2gAaOyuRimK-X0eC70",
  authDomain: "eegdata-93ae1.firebaseapp.com",
  projectId: "eegdata-93ae1",
  storageBucket: "eegdata-93ae1.appspot.com",
  messagingSenderId: "294911481131",
  appId: "1:294911481131:web:60994afd7f95f19070a16e",
  measurementId: "G-TP24HLJ5MJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
import { getStorage, ref } from "firebase/storage";

// Create a root reference
const storage = getStorage();

// Create a reference to file
const eegRef = ref(storage, 'evoked_eeg_LV.mat');

// Create a reference to 'images/mountains.jpg'

// While the file names are the same, the references point to different files
eegRef.name === eegRef.name;           // true
eegRef.fullPath === eegRef.fullPath;   // false 
  /*
  document.getElementById("submitBtn").addEventListener("click", function() { 
    let postid = uuidv4();
    let inputElem = document.getElementById("up");
    let file = inputElem.files[0];
    // Create new file so we can rename the file
    let blob = file.slice(0, file.size);
    newFile = new File([blob], postid); //renames file

    let formData = new FormData();
    formData.append("up", newFile);
    fetch("/upload", { //"https://httpbin.org/post"
        method: "POST",
        body: formData,
      })
      .then((res) => res.text());
      //   .then(loadPosts());
      console.log("res.text");
   
  });
*/