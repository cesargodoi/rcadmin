//fields
const activityEvent = document.getElementById("id_activity");
const centerEvent = document.getElementById("id_center");
const initialDateEvent = document.getElementById("id_date");

function checkForm() {
  let message = "Don't forget this field.";
  if (activityEvent.item(0).selected) {
    alertField("id_activity", message);
    return false;
  }
  if (centerEvent.item(0).selected) {
    alertField("id_center", message);
    return false;
  }
  if (initialDateEvent.value == "" || initialDateEvent.value === null) {
    alertField("id_date", message);
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
