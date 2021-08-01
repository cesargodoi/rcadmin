//fields
const centerLecture = document.getElementById("id_center");
const dateLecture = document.getElementById("id_date");
const themeLecture = document.getElementById("id_theme");
const typeLecture = document.getElementById("id_type");

function checkForm() {
  if (centerLecture.item(0).selected) {
    let message = "Don't forget this field.";
    alertField("id_center", message);
    return false;
  }
  if (dateLecture.value == "" || dateLecture.value === null) {
    let message = "Don't forget this field.";
    alertField("id_date", message);
    return false;
  }
  if (themeLecture.value == "" || themeLecture.value === null) {
    let message = "What's theme for this lecture?";
    alertField("id_theme", message);
    return false;
  }
  if (typeLecture.value == "" || typeLecture.value === null) {
    let message = "What's type of this lecture?";
    alertField("id_type", message);
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
