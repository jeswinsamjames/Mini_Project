document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector("form");
  const inputs = form.querySelectorAll(".form-control");

  const validationRules = {
    first_name: {
      regex: /^[A-Za-z\s]{2,30}$/, // Only alphabets and spaces allowed
      message: "First name must be valid (no numbers or special characters).",
    },
    last_name: {
      regex: /^[A-Za-z\s]{1,30}$/, // Only alphabets and spaces allowed
      message: "Last name must be valid (no numbers or special characters).",
    },
    email: {
      regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: "Email must be valid.",
    },
    phone: {
      regex: /^[0-9]{10}$/,
      message: "Phone number must be 10 digits.",
    },
    password: {
      regex: /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/, // Requires 8 characters with 1 special character and 1 number
      message: "Password must be at least 8 characters with one special character and one number.",
    },
    cnpassword: {
      confirm: "password",
      message: "Passwords must match.",
    },
  };

  inputs.forEach(input => {
    input.addEventListener("input", function() {
      const error = this.nextElementSibling;
      if (this.value.trim() === "") {
        error.textContent = "";
        this.classList.remove("error");
        return;
      }
      const validationRule = validationRules[this.id];
      if (validationRule) {
        validateField(validationRule, this, error);
      }
    });
  });

  function validateField(rule, input, error) {
    if (rule.regex && !rule.regex.test(input.value)) {
      error.textContent = rule.message;
      input.classList.add("error");
    } else if (rule.confirm) {
      const passwordInput = form.querySelector(`#${rule.confirm}`);
      if (passwordInput.value !== input.value) {
        error.textContent = rule.message;
        input.classList.add("error");
      } else {
        error.textContent = "";
        input.classList.remove("error");
      }
    } else {
      error.textContent = "";
      input.classList.remove("error");
    }
  }

  form.addEventListener("submit", function(e) {
    inputs.forEach(input => {
      const validationRule = validationRules[input.id];
      if (validationRule) {
        if (!input.value.trim() || (validationRule.regex && !validationRule.regex.test(input.value))) {
          const error = input.nextElementSibling;
          error.textContent = !input.value.trim() ? "This field is required." : validationRule.message;
          input.classList.add("error");
          e.preventDefault();
        }
      }
    });
  });
});
