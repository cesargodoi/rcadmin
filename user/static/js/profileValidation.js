//basic
// label para e-mail input
var hint_email = document.getElementById("hint_id_email");
hint_email.innerHTML = "Enter a valid e-mail: your@mail.com";

//fields
const socialName = document.getElementById("id_social_name");
const email = document.getElementById("id_email");
const phone_1 = document.getElementById("id_phone_1");
const phone_2 = document.getElementById("id_phone_2");
const sosContact = document.getElementById("id_sos_contact");
const sosPhone = document.getElementById("id_sos_phone");

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

// main check function
function checkForm() {
  // checking name input
  if (
    socialName.value.length < 2 ||
    socialName.value == "" ||
    socialName.value === null
  ) {
    let message = "Please write what you would like to be called.";
    alertField("id_social_name", message);
    return false;
  }
  // checking e-mail input
  if (
    email.value.indexOf("@") == -1 ||
    email.value.indexOf(".") == -1 ||
    email.value == "" ||
    email.value == null
  ) {
    let message = "Please enter a valid email address";
    alertField("id_email", message);
    return false;
  }
  if (
    phone_1.value.length < 10 ||
    phone_1.value == "" ||
    phone_1.value === null
  ) {
    let message = "Please register a valid phone number: xx-98765.4321";
    alertField("id_phone_1", message);
    return false;
  }
  if (phone_2.value.length > 0 && phone_2.value.length < 10) {
    let message = "Please register a valid phone number: xx-98765.4321";
    alertField("id_phone_2", message);
    return false;
  }
  if (sosContact.value) {
    if (sosPhone.value.length >= 0 && sosPhone.value.length < 10) {
      let message = "Please register a valid phone number: xx-98765.4321";
      alertField("id_sos_phone", message);
      return false;
    }
  }
  if (sosPhone.value) {
    if (sosContact.value == "" || sosContact.value == null) {
      let message = "What's the name of your emergency contact?";
      alertField("id_sos_contact", message);
      return false;
    }
  }
  // submit after checked form
  document.getElementById("form").submit();
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

// main function
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
