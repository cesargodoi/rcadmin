//basic
// label para e-mail input
var hint_email = document.getElementById("hint_id_email");
hint_email.innerHTML = "Enter a valid e-mail: your@mail.com";

//fields
const namePerson = document.getElementById("id_name");
const socialPerson = document.getElementById("id_social_name");
const emailPerson = document.getElementById("id_email");
const phoneOnePerson = document.getElementById("id_phone_1");
const phoneTwoPerson = document.getElementById("id_phone_2");
const sosContact = document.getElementById("id_sos_contact");
const sosPhone = document.getElementById("id_sos_phone");
const birthDay = document.getElementById("id_birth");

//main function
function checkForm() {
  if (namePerson.value == "") {
    let message = "Don't forget this field.";
    alertField("id_name", message);
    return false;
  }
  if (
    socialPerson.length < 2 ||
    socialPerson.value == "" ||
    socialPerson.value === null
  ) {
    let message = "Don't forget this field.";
    alertField("id_social_name", message);
    return false;
  }
  if (
    emailPerson.value.indexOf("@") == -1 ||
    emailPerson.value.indexOf(".") == -1 ||
    emailPerson.value == "" ||
    emailPerson.value == null
  ) {
    let message = "enter with a valid e-mail: your@mail.com";
    alertField("id_email", message);
    return false;
  }
  if (
    phoneOnePerson.value.length < 10 ||
    phoneOnePerson.value == "" ||
    phoneOnePerson.value === null
  ) {
    let message = "enter with a valid phone number: xx-98765.4321";
    alertField("id_phone_1", message);
    return false;
  }
  if (phoneTwoPerson.value.length > 0 && phoneTwoPerson.value.length < 10) {
    let message = "enter with a valid phone number: xx-98765.4321";
    alertField("id_phone_2", message);
    return false;
  }
  if (sosContact.value) {
    if (sosPhone.value.length >= 0 && sosPhone.value.length < 10) {
      let message = "Don't forget this field.";
      alertField("id_sos_phone", message);
      return false;
    }
  }
  if (sosPhone.value) {
    if (sosContact.value == "" || sosContact.value == null) {
      let message = "Don't forget this field.";
      alertField("id_sos_contact", message);
      return false;
    }
  }
  if (birthDay.value == "" || birthDay.value === null) {
    let message = "Don't forget this field.";
    alertField("id_birth", message);
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
