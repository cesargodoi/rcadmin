//fields
const nameWorkGroup = document.getElementById("id_name");
const centerWorkGroup = document.getElementById("id_center");
const typeWorkGroup = document.getElementById("id_workgroup_type");
const aspectWorkGroup = document.getElementById("id_aspect");
const divAspectChoice = document.getElementById("div_id_aspect");

//main function
function checkForm() {
  let message = "Don't forget this field.";
  if (nameWorkGroup.value == "" || nameWorkGroup.value === null) {
    let message = "What's your group name?";
    alertField("id_name", message);
    return false;
  }
  if (centerWorkGroup.item(0).selected) {
    alertField("id_center", message);
    return false;
  }
  if (typeWorkGroup.value == "" || typeWorkGroup.value === null) {
    let message = "What's your group type?";
    alertField("id_workgroup_type", message);
    return false;
  }
  if (aspectWorkGroup.item(0).selected) {
    if (divAspectChoice.style.display === "block") {
      alertField("id_aspect", message);
      return false;
    }
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

//makes Aspect field appear when clicking outside the Type field
divAspectChoice.style.display = "none";
typeWorkGroup.addEventListener("blur", (evento) => {
  displayAspectChoices();
});

function displayAspectChoices() {
  if (typeWorkGroup.value == "ASP") {
    divAspectChoice.style.display = "block";
  } else {
    divAspectChoice.style.display = "none";
  }
}
