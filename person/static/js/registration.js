// variables
const password = document.getElementById('password');
const passwordRepeat = document.getElementById('passwordRepeat');
const passDiff = document.getElementById('passDiff');
// 
const passStrength = document.getElementById('passStrength');
const lengthPass = document.getElementById('lengthPass');
const numberChar = document.getElementById('numberChar');
const lowerChar = document.getElementById('lowerChar');
const upperChar = document.getElementById('upperChar');
const specialChar = document.getElementById('specialChar');
const strength = document.getElementById('strength');
// 
const aceptDataPolicy = document.getElementById('accept');
const submitButton = document.getElementById('submit-button');
const agreeButton = document.getElementById('agree-button');
//
const nameForm = document.getElementById('id_name');
const birthForm = document.getElementById('id_birth');
const cityForm = document.getElementById('id_city');
const UFForm = document.getElementById('id_state');
const phoneForm = document.getElementById('id_phone');
const emailForm = document.getElementById('id_email');


// compare password and passwordRepeat ////////////////////////////////////////
password.addEventListener('change', () => differentPW());
passwordRepeat.addEventListener('keyup', () => differentPW());

function differentPW() {
  submitButtonIsDisabled();
  if (password.value != passwordRepeat.value) {
    passwordRepeat.classList.add('is-invalid');
    passDiff.innerText = 'as senhas não conferem';
  } else {
    passwordRepeat.classList.remove('is-invalid');
    passDiff.innerText = '';
  }
}

// toggle password
function togglePassword(id) {
  const passwd = document.getElementById(id);
  const icon = document.getElementById(`${id}Icon`);

  if (passwd.type == 'password') {
    passwd.type = 'text';
    icon.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    passwd.type = 'password';
    icon.classList.replace('fa-eye-slash', 'fa-eye')
  }
}

// others - Data Policy check /////////////////////////////////////////////////
function submitButtonIsDisabled() {
  if (
    aceptDataPolicy.checked && 
    password.value.length > 0 && 
    password.value === passwordRepeat.value
  ) {
    submitButton.disabled = false;
  } else {
    submitButton.disabled = true;
  }
}

aceptDataPolicy.addEventListener('click', () => {submitButtonIsDisabled();});

agreeButton.onclick = () => {
  aceptDataPolicy.checked = true;
  submitButtonIsDisabled();
};


// password strength //////////////////////////////////////////////////////////
password.addEventListener('keyup', () => checkTheStrength())

function checkTheStrength() {
  var totalStrength = 0;
  if (password.value.length > 10){
    totalStrength += 28;
    has(lengthPass);
  } else {
    hasNot(lengthPass);
  }
  if (password.value.match(/[0-9]+/)){
    totalStrength += 18;
    has(numberChar);
  } else {
    hasNot(numberChar);
  }
  if (password.value.match(/[a-z]+/)){
    totalStrength += 18;
    has(lowerChar);
  } else {
    hasNot(lowerChar);
  }
  if (password.value.match(/[A-Z]+/)){
    totalStrength += 18;
    has(upperChar);
  } else {
    hasNot(upperChar);
  } 
  if (password.value.match(/[^0-9a-zA-Z]+/)){
    totalStrength += 18;
    has(specialChar);
  } else {
    hasNot(specialChar);
  }
  checkTotal(totalStrength);
}

function checkTotal(total){
  if (total == 0) {
    strength.innerText = '';
    strength.className = ''
  }
  if (total > 0 && total <= 25) {
    strength.innerText = 'FRACA';
    strength.className = 'ml-4 font-weight-bold badge badge-pill badge-danger'
  }
  if (total > 25 && total <= 50) {
    strength.innerText = 'MÉDIA';
    strength.className = 'ml-4 font-weight-bold badge badge-pill badge-warning'
  }
  if (total > 50 && total <= 75) {
    strength.innerText = 'FORTE';
    strength.className = 'ml-4 font-weight-bold badge badge-pill badge-info'
  }
  if (total > 75) {
    strength.innerText = 'EXCELENTE';
    strength.className = 'ml-4 font-weight-bold badge badge-pill badge-primary'
  }
}

function has(obj){
  obj.classList.replace('text-secondary', 'text-primary');
  obj.children[0].classList.replace('fa-square', 'fa-square-check');
}

function hasNot(obj){
  obj.classList.replace('text-primary', 'text-secondary');
  obj.children[0].classList.replace('fa-square-check', 'fa-square');
}


// validation form ////////////////////////////////////////////////////////////
submitButton.onclick = () => {checkForm();};

function checkForm() {
  if (nameForm.value == '' || nameForm.value == null) {
    let message = "Don't forget this field.";
    alertField('id_name', message);
    return false;
  }
  if (birthForm.value == '' || birthForm.value === null) {
    let message = "Don't forget this field.";
    alertField('id_birth', message);
    return false;
  }
  if (cityForm.value == '' || cityForm.value === null) {
    let message = "Don't forget this field.";
    alertField('id_city', message);
    return false;
  }
  if (UFForm.value == '' || UFForm.value === null) {
    let message = "Don't forget this field.";
    alertField('id_state', message);
    return false;
  }
  if (
    phoneForm.value.length < 10 ||
    phoneForm.value == '' ||
    phoneForm.value === null
  ) {
    let message = 'enter with a valid phone number: xx-98765.4321';
    alertField('id_phone', message);
    return false;
  }
  if (
    emailForm.value.indexOf('@') == -1 ||
    emailForm.value.indexOf('.') == -1 ||
    emailForm.value == '' ||
    emailForm.value == null
  ) {
    let message = 'enter with a valid e-mail: your@mail.com';
    alertField('id_email', message);
    return false;
  }
}

function alertField(input, message) {
  const invalidField = document.getElementById(input);

  var invalidValueField = document.createElement('p');
  invalidValueField.classList.add('invalid-feedback');
  var invalidText = document.createTextNode(message);
  invalidValueField.appendChild(invalidText);
  invalidField.parentElement.appendChild(invalidValueField);
  invalidField.classList.add('is-invalid');
  invalidField.focus();
}