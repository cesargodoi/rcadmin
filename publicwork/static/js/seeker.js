//fields
const nameSeeker = document.getElementById("id_name");
const birthSeeker = document.getElementById("id_birth");
const citySeeker = document.getElementById("id_city");
const UFSeeker = document.getElementById("id_state");
const phoneSeeker = document.getElementById("id_phone");
const emailSeeker = document.getElementById("id_email");
const centerSeeker = document.getElementById("id_center");

//label with orientation for email field
const labelEmailSeeker = document.createElement("small");
labelEmailSeeker.classList.add("text-muted", "form-text");
var labelText = document.createTextNode("Enter a valid e-mail: your@mail.com");
labelEmailSeeker.appendChild(labelText);
emailSeeker.parentElement.appendChild(labelEmailSeeker);

function checkForm() {
  if (nameSeeker.value == "" || nameSeeker.value == null) {
    let message = "Don't forget this field.";
    alertField("id_name", message);
    return false;
  }
  if (birthSeeker.value == "" || birthSeeker.value === null) {
    let message = "Don't forget this field.";
    alertField("id_birth", message);
    return false;
  }
  if (
    phoneSeeker.value.length < 10 ||
    phoneSeeker.value == "" ||
    phoneSeeker.value === null
  ) {
    let message = "enter with a valid phone number: xx-98765.4321";
    alertField("id_phone", message);
    return false;
  }
  if (
    emailSeeker.value.indexOf("@") == -1 ||
    emailSeeker.value.indexOf(".") == -1 ||
    emailSeeker.value == "" ||
    emailSeeker.value == null
  ) {
    let message = "enter with a valid e-mail: your@mail.com";
    alertField("id_email", message);
    return false;
  }
  if (centerSeeker.item(0).selected) {
    let message = "Don't forget this field.";
    alertField("id_center", message);
    return false;
  }

  document.getElementById("form").submit();
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
