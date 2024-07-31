/*----------------------------------------------------- Menuicon ----------------------------------------------------*/

function changemenuicon() {

    var icon = document.getElementById('menuicon');
    
        if(icon.className === "bi bi-menu-button-fill"){
    
        icon.className = "bi bi-menu-button-wide-fill";
    
        } else {
    
        icon.className = "bi bi-menu-button-fill";
    
        }
               
}

/*----------------------------------------------------- Sidebar ----------------------------------------------------*/

document.addEventListener('DOMContentLoaded', (event) => {
    var menuicon = document.getElementById('Menuicon');
    var sidebar = document.querySelector(".sidebar");
    var sidebox = document.querySelector(".side-box");
    var main = document.querySelector(".Main-box");

    menuicon.onclick = function() {
        sidebar.classList.toggle("hidden-sidebar");
        sidebox.classList.toggle("hidden-sidebox");
        main.classList.toggle("large-main");
    }
});

/*----------------------------------------------------- Alert Box ----------------------------------------------------*/

function closeAlert(alertId) {
    const alertElement = document.getElementById(alertId);
    if (alertElement) {
        alertElement.style.display = 'none';
    }
}

/*----------------------------------------------------- Password ----------------------------------------------------*/

const passwordField = document.getElementById("password");
const passwordField2 = document.getElementById("password2");
const togglePassword = document.getElementById("eye");
const togglePassword2 = document.getElementById("eye2");

togglePassword.addEventListener("click", function () {
  if (passwordField.type === "password") {
    passwordField.type = "text";
    togglePassword.className = "bi bi-eye-slash-fill";

  } else {
    passwordField.type = "password";
    togglePassword.className = "bi bi-eye-fill";
  }
});

togglePassword2.addEventListener("click", function () {
    if (passwordField2.type === "password") {
      passwordField2.type = "text";
      togglePassword2.className = "bi bi-eye-slash-fill";
  
    } else {
      passwordField2.type = "password";
      togglePassword2.className = "bi bi-eye-fill";
    }
  });