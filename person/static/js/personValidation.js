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
  if (phoneOnePerson.value.length > 0 && phoneOnePerson.value.length < 10) {
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

// ******************************

//Address filled by ZIP Code

const inputCep = document.getElementById("id_zip_code");
inputCep.addEventListener("focusout", () => {
  pesquisacep(inputCep.value);
});

function limpa_formulário_cep() {
  //Limpa valores do formulário de cep.
  document.getElementById("id_address").value = "";
  document.getElementById("id_district").value = "";
  document.getElementById("id_city").value = "";
  document.getElementById("id_state").value = "";
}

function meu_callback(conteudo) {
  if (!("erro" in conteudo)) {
    //Atualiza os campos com os valores.
    document.getElementById("id_address").value = conteudo.logradouro;
    document.getElementById("id_district").value = conteudo.bairro;
    document.getElementById("id_city").value = conteudo.localidade;
    document.getElementById("id_state").value = conteudo.uf;
  } //end if.
  else {
    //CEP não Encontrado.
    limpa_formulário_cep();
    // alert("CEP não encontrado.");
    let message = "CEP não encontrado.";
    alertField("id_zip_code", message);
  }
}

function pesquisacep(valor) {
  //Nova variável "cep" somente com dígitos.
  var cep = valor.replace(/\D/g, "");

  //Verifica se campo cep possui valor informado.
  if (cep != "") {
    //Expressão regular para validar o CEP.
    var validacep = /^[0-9]{8}$/;

    //Valida o formato do CEP.
    if (validacep.test(cep)) {
      //Preenche os campos com "..." enquanto consulta webservice.
      document.getElementById("id_address").value = "...";
      document.getElementById("id_district").value = "...";
      document.getElementById("id_city").value = "...";
      document.getElementById("id_state").value = "...";

      //Cria um elemento javascript.
      var script = document.createElement("script");

      //Sincroniza com o callback.
      script.src =
        "https://viacep.com.br/ws/" + cep + "/json/?callback=meu_callback";

      //Insere script no documento e carrega o conteúdo.
      document.body.appendChild(script);
    } //end if.
    else {
      //cep é inválido.
      limpa_formulário_cep();
      // alert("Formato de CEP inválido.");
      let message = "Formato de CEP inválido.";
      alertField("id_zip_code", message);
    }
  } //end if.
  else {
    //cep sem valor, limpa formulário.
    limpa_formulário_cep();
  }
}

// ******************************
