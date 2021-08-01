const valueFormPayment = document.getElementById("id_value");
const payFormType = document.getElementById("id_payform_type");
const flagFormPayment = document.getElementById("id_bank_flag");
const ctrlFormPayment = document.getElementById("id_ctrl_number");

//hidden inputs if payform type == cash
const divcomplementFormPayment = document.getElementById("div_id_complement");
const divctrlFormPayment = document.getElementById("div_id_ctrl_number");
const divflagFormPayment = document.getElementById("div_id_bank_flag");
divcomplementFormPayment.style.display = "none";
divctrlFormPayment.style.display = "none";
divflagFormPayment.style.display = "none";

//show inputs if payfom type !cash
payFormType.addEventListener("blur", (evento) => {
  displayfields();
});

function displayfields() {
  if (payFormType.value != "CSH") {
    divcomplementFormPayment.style.display = "block";
    divctrlFormPayment.style.display = "block";
    divflagFormPayment.style.display = "block";
  } else {
    divcomplementFormPayment.style.display = "none";
    divctrlFormPayment.style.display = "none";
    divflagFormPayment.style.display = "none";
  }
}

//main function
function checkForm() {
  let message = "Don't forget this field.";
  if (valueFormPayment.value == "" || valueFormPayment.value === null) {
    alertField("id_value", message);
    return false;
  }
  if (
    divflagFormPayment.style.display == "block" &&
    flagFormPayment.item(0).selected
  ) {
    let message = "What is your bank?";
    alertField("id_bank_flag", message);
    return false;
  }
  if (
    (divctrlFormPayment.style.display == "block" &&
      ctrlFormPayment.value == "") ||
    ctrlFormPayment.value === null
  ) {
    alertField("id_ctrl_number", message);
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
