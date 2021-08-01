const paytypeCreateOrder = document.getElementById("id_paytype");
const monthCreateOrder = document.getElementById("id_ref_month");
const valueCreateOrder = document.getElementById("id_value");
const personCreateOrder = document.getElementById("id_person");
const eventCreateOrder = document.getElementById("id_event");

//hidden event input div
const divEventChoices = document.getElementById("div_id_event");
divEventChoices.style.display = "none";

//main function
function checkForm() {
  let message = "Don't forget this field.";

  if (paytypeCreateOrder.item(0).selected) {
    let message = "Choose what you will pay.";
    alertField("id_paytype", message);
    return false;
  }
  if (monthCreateOrder.value == "" || monthCreateOrder.value === null) {
    alertField("id_ref_month", message);
    return false;
  }
  if (valueCreateOrder.value == "" || valueCreateOrder.value === null) {
    alertField("id_value", message);
    return false;
  }
  if (personCreateOrder.item(0).selected) {
    let message = "Whose payment is it?";
    alertField("id_person", message);
    return false;
  }
  if (
    divEventChoices.style.display == "block" &&
    eventCreateOrder.item(0).selected
  ) {
    let message = "Which conference do you want to pay for?";
    alertField("id_event", message);
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

//faz campo Event aparecer ao clicar fora do campo Paytype
paytypeCreateOrder.addEventListener("blur", (evento) => {
  displayEventChoices();
});

function displayEventChoices() {
  const divEventChoices = document.getElementById("div_id_event");

  if (paytypeCreateOrder.value == "3") {
    divEventChoices.style.display = "block";
  } else {
    divEventChoices.style.display = "none";
  }
}
