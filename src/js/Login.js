import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";
const auth = getAuth();
var loginButton = document.getElementById("login-btn");
loginButton.addEventListener("click", function() {
let email = document.getElementById("username").value;
let password = document.getElementById("password").value;
		if (email == '' || password == '') {
			document.getElementById('Login-errs').innerHTML = "Missing Email or Password!";
			document.getElementById('Login-errs').style.display = "inline";
		}
    else{
        signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
          // Signed in
          var user = userCredential.user;
          // ...
        })
        .catch((error) => {
          var errorCode = error.code;
          var errorMessage = error.message;
        });
         /*
          document.getElementById('Login-errs').innerHTML = "Incorrect Username or Password";
          document.getElementById('Login-errs').style.display = "inline"; */
        }
      
      }); 
onAuthStateChanged(auth, (user) => {
  if (user) {
      const uid = user.uid;
      document.getElementById("current-login").innerHTML =  "You are currently logged in as: " + user.email;
      // ...
  } else { 
      document.getElementById("current-login").innerHTML = "Sign in to view uploaded files:";
    }
  });




