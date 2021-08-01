const personCreateOrder = document.getElementById("person");

//main function
function checkForm() {
  let message = "Don't forget this field.";
  if (personCreateOrder.value == "") {
    alertField("person", message);
    return false;
  }

  document.getElementById("form").submit();
}

//handler function
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
