// // avoid submit with enter key
// $(document).ready(function () {
//   $(window).keydown(function (event) {
//     if (event.keyCode == 10) {
//       event.preventDefault();
//       return false;
//     }
//   });
// });

//Data Policy check
const aceptDataPolicy = document.getElementById("accept");
const submitButton = document.getElementById("submit-button");
const agreeButton = document.getElementById("agree-button");

function submitButtonIsDisabled() {
  if (aceptDataPolicy.checked) {
    submitButton.disabled = false;
  } else {
    submitButton.disabled = true;
  }
}

aceptDataPolicy.addEventListener("click", (evento) => {
  submitButtonIsDisabled();
});

agreeButton.onclick = () => {
  aceptDataPolicy.checked = true;
  submitButtonIsDisabled();
};

//validation form
//fields
const nameForm = document.getElementById("id_name");
const birthForm = document.getElementById("id_birth");
const cityForm = document.getElementById("id_city");
const UFForm = document.getElementById("id_state");
const phoneForm = document.getElementById("id_phone");
const emailForm = document.getElementById("id_email");

submitButton.onclick = () => {
  checkForm();
};

function checkForm() {
  if (nameForm.value == "" || nameForm.value == null) {
    let message = "Don't forget this field.";
    alertField("id_name", message);
    return false;
  }
  if (birthForm.value == "" || birthForm.value === null) {
    let message = "Don't forget this field.";
    alertField("id_birth", message);
    return false;
  }
  if (cityForm.value == "" || cityForm.value === null) {
    let message = "Don't forget this field.";
    alertField("id_city", message);
    return false;
  }
  if (UFForm.value == "" || UFForm.value === null) {
    let message = "Don't forget this field.";
    alertField("id_state", message);
    return false;
  }
  if (
    phoneForm.value.length < 10 ||
    phoneForm.value == "" ||
    phoneForm.value === null
  ) {
    let message = "enter with a valid phone number: xx-98765.4321";
    alertField("id_phone", message);
    return false;
  }
  if (
    emailForm.value.indexOf("@") == -1 ||
    emailForm.value.indexOf(".") == -1 ||
    emailForm.value == "" ||
    emailForm.value == null
  ) {
    let message = "enter with a valid e-mail: your@mail.com";
    alertField("id_email", message);
    return false;
  }
}

function alertField(input, message) {
  const invalidField = document.getElementById(input);

  var invalidValueField = document.createElement("p");
  invalidValueField.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(message);
  invalidValueField.appendChild(invalidText);
  invalidField.parentElement.appendChild(invalidValueField);
  invalidField.classList.add("is-invalid");
  invalidField.focus();
}
