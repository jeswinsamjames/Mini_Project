
  // Get the form element
  const form = document.querySelector('form');

  // Get the form inputs
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');

  // Add event listeners for input fields
  usernameInput.addEventListener('input', validateUsername);
  passwordInput.addEventListener('input', validatePassword);

  // Function to validate username
  function validateUsername() {
    const usernameValue = usernameInput.value.trim();
    const formGroup = usernameInput.parentElement;

    if (usernameValue === '') {
      setErrorFor(formGroup, 'Username cannot be empty');
    } else {
      setSuccessFor(formGroup);
    }
  }

  // Function to validate password
  function validatePassword() {
    const passwordValue = passwordInput.value.trim();
    const formGroup = passwordInput.parentElement;

    if (passwordValue === '') {
      setErrorFor(formGroup, 'Password cannot be empty');
    } else {
      setSuccessFor(formGroup);
    }
  }

  // Function to set error class and display error message
  function setErrorFor(formGroup, message) {
    const errorMessage = formGroup.querySelector('.error-message');

    formGroup.classList.add('error');
    errorMessage.innerText = message;
  }

  // Function to set success class
  function setSuccessFor(formGroup) {
    formGroup.classList.remove('error');
  }

  // Add form submit event listener
  form.addEventListener('submit', function (e) {
    // Validate fields before form submission
    validateUsername();
    validatePassword();

    // Prevent form submission if there are errors
    if (document.querySelector('.error')) {
      e.preventDefault();
    }
  });




