const divEventChoices = document.getElementById("div_id_event");
divEventChoices.style.display = "none";

//makes Event field appear when clicking outside the Paytype field
const paytypeField = document.getElementById("id_paytype");
paytypeField.addEventListener("blur", (evento) => {
  displayEventChoices();
});

//verify that all fields are valid in the form before saving
function checkForm() {
  const paytypeField = document.getElementById("id_paytype");
  const valueField = document.getElementById("id_value");
  const eventField = document.getElementById("id_event");
  const dateField = document.getElementById("id_ref_month");

  message = "Please choose one of the options.";
  if (paytypeField.value == "") {
    alertField("id_paytype", message);
    return false;
  }
  if (divEventChoices.style.display != "none" && eventField.value == "") {
    alertField("id_event", message);
    return false;
  }
  if (valueField.value == "") {
    alertField("id_value", message);
    return false;
  }
  if (dateField.value == "") {
    message = "Don't forget this field.";
    alertField("id_ref_month", message);
    return false;
  }

  document.getElementById("form").submit();
}

// handler function
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

function displayEventChoices() {
  const paytypeChoices = document.getElementById("id_paytype");
  const divEventChoices = document.getElementById("div_id_event");

  if (paytypeChoices.value == "3") {
    divEventChoices.style.display = "block";
  } else {
    divEventChoices.style.display = "none";
  }
}
