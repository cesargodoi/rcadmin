//fields
const nameCenter = document.getElementById("id_name");
const confCenter = document.getElementById("id_conf_center");
const phoneCenter = document.getElementById("id_phone_1");
const emailCenter = document.getElementById("id_email");
const secretaryCenter = document.getElementById("id_secretary");

//label with orientation for email field
const labelEmail = document.createElement("small");
labelEmail.classList.add("text-muted", "form-text");
var labelText = document.createTextNode("Enter a valid e-mail: your@mail.com");
labelEmail.appendChild(labelText);
emailCenter.parentElement.appendChild(labelEmail);

function checkForm() {
  let message = "Don't forget this field.";
  if (nameCenter.value == "" || nameCenter.value === null) {
    alertField("id_name", message);
    return false;
  }
  if (confCenter.item(0).selected) {
    alertField("id_conf_center", message);
    return false;
  }
  if (
    phoneCenter.value.length < 10 ||
    phoneCenter.value == "" ||
    phoneCenter.value === null
  ) {
    let message = "enter with a valid phone number: xx-98765.4321";
    alertField("id_phone_1", message);
    return false;
  }
  if (
    emailCenter.value.indexOf("@") == -1 ||
    emailCenter.value.indexOf(".") == -1 ||
    emailCenter.value == "" ||
    emailCenter.value == null
  ) {
    let message = "enter with a valid e-mail: your@mail.com";
    alertField("id_email", message);
    return false;
  }
  if (secretaryCenter.item(0).selected) {
    alertField("id_secretary", message);
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

//Address filled by ZIP Code
// aplicating function in tag
let inputCep = document.querySelector("input[id=id_zip_code]");
inputCep.addEventListener("change", searchZIPCode);

// handlers functions
function fillField(json) {
  document.querySelector("input[id=id_address]").value = json.logradouro;
  document.querySelector("input[id=id_district]").value = json.bairro;
  document.querySelector("input[id=id_complement]").value = json.complemento;
  document.querySelector("input[id=id_city]").value = json.localidade;
  document.querySelector("input[id=id_state]").value = json.uf;
}

// main function for ZIP code
function searchZIPCode() {
  let inputCep = document.querySelector("input[id=id_zip_code]");
  let cep = inputCep.value.replace("-", "");

  let url = "http://viacep.com.br/ws/" + cep + "/json";

  let xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) fillField(JSON.parse(xhr.responseText));
    }
  };
  xhr.send();
}
