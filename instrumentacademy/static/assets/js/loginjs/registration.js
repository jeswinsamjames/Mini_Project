document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const inputs = form.querySelectorAll(".form-control");
  
    // Regular expressions for validation
    const nameRegex = /^[a-zA-Z ]{2,30}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[0-9]{10}$/;
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
  
    inputs.forEach(input => {
      input.addEventListener("input", function() {
        const error = this.nextElementSibling;
        if (this.value.trim() === "") {
          error.textContent = "";
          this.classList.remove("error");
          return;
        }
        switch (this.id) {
          case "full_name":
            validateField(nameRegex, this, error, "Full name must be valid.");
            break;
          case "email":
            validateField(emailRegex, this, error, "Email must be valid.");
            break;
          case "phone":
            validateField(phoneRegex, this, error, "Phone number must be 10 digits.");
            break;
          case "password":
            validateField(passwordRegex, this, error, "Password must be at least 8 characters and contain at least one letter and one number.");
            break;
          case "cnpassword":
            const passwordInput = form.querySelector("#password");
            validateConfirmPassword(this, passwordInput, error, "Passwords must match.");
            break;
          default:
            break;
        }
      });
    });
  
    function validateField(regex, input, error, message) {
      if (regex.test(input.value)) {
        error.textContent = "";
        input.classList.remove("error");
      } else {
        error.textContent = message;
        input.classList.add("error");
      }
    }
  
    function validateConfirmPassword(confirmInput, passwordInput, error, message) {
      if (confirmInput.value === passwordInput.value) {
        error.textContent = "";
        confirmInput.classList.remove("error");
      } else {
        error.textContent = message;
        confirmInput.classList.add("error");
      }
    }
  
    form.addEventListener("submit", function(e) {
      inputs.forEach(input => {
        if (!input.value.trim()) {
          const error = input.nextElementSibling;
          error.textContent = "This field is required.";
          input.classList.add("error");
          e.preventDefault();
        }
      });
    });
  });
  document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const inputs = form.querySelectorAll(".form-control");
  
    // Regular expressions for validation
    // ... existing regex patterns ...
  
    // State and District dropdowns
    const stateSelect = document.getElementById("state");
    const districtSelect = document.getElementById("district");
  
    inputs.forEach(input => {
      // ... existing input validation ...
  
      // Add validation for State dropdown
      stateSelect.addEventListener("change", function() {
        if (stateSelect.value) {
          clearError("state");
        } else {
          showError("state", "Please select a state.");
        }
      });
  
      // Add validation for District dropdown
      districtSelect.addEventListener("change", function() {
        if (districtSelect.value) {
          clearError("district");
        } else {
          showError("district", "Please select a district.");
        }
      });
    });
  
    // ... existing functions ...
  
    form.addEventListener("submit", function(e) {
      inputs.forEach(input => {
        // ... existing form submission validation ...
  
        // Validate State dropdown
        if (!stateSelect.value) {
          showError("state", "Please select a state.");
          e.preventDefault();
        }
  
        // Validate District dropdown
        if (!districtSelect.value) {
          showError("district", "Please select a district.");
          e.preventDefault();
        }
      });
    });
  });
  