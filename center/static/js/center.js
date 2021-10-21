//fields
const nameCenter = document.getElementById("id_name");
const phoneCenter = document.getElementById("id_phone_1");
const emailCenter = document.getElementById("id_email");
const secretaryCenter = document.getElementById("id_secretary");

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

// ***************************************

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

// ***************************************
