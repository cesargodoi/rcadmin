//fields
const nameGroup = document.getElementById("id_name");
const centerGroup = document.getElementById("id_center");

function checkForm() {
  let message = "Don't forget this field.";
  if (nameGroup.value == "" || nameGroup.value === null) {
    alertField("id_name", message);
    return false;
  }
  if (centerGroup.item(0).selected) {
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
