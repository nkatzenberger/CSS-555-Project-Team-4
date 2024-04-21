import { signOut, getAuth } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";
var SObutton = document.getElementById("signOut-btn");
SObutton.addEventListener("click", function(){
const auth = getAuth();
signOut(auth).then(function() {
    console.log('Signed Out');
    document.getElementById("current-login").innerHTML = "User Signed Out";
    document.getElementById("signOut-btn").style.display = "none";
    document.getElementById("right-input-fields").style.display = "inline";
    document.getElementById("login-btn").style.display = "inline";
    document.getElementById("Login-errs").style.display = "none";
})
  .catch((error) => {
    console.error('Sign Out Error', error);
  })
});
