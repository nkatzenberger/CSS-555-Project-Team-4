import { getAuth, signInWithEmailAndPassword, credentials } from "./firebase/auth";
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
var email = document.getElementById("username");
var password = document.getElementById("password");
var loginButton = document.getElementById("login-btn");
cloudkeys = credentials.Certificate("../NewCreds.json");
loginButton.addEventListener("click", function() {
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
        document.getElementById("current-login") += credentials.user;
      // ...
    } else {
      // User is signed out
      // ...
    }
  });
});
