import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
var email = document.getElementById("username");
var password = document.getElementById("password");

signInWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed in 
    const user = userCredential.user;
    // ...
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
  });

  onAuthStateChanged(auth, (user) => {
    if (user) {
      const uid = user.uid;
        document.getElementById("current-login") += userCredential.user;
      // ...
    } else {
      // User is signed out
      // ...
    }
  });