//form fields
const voucherImg = document.getElementById("id_voucher_img");
const bancFlagField = document.getElementById("id_bank_flag");
const ctrlNumberField = document.getElementById("id_ctrl_number");

//faz campo de valor não ser editável no profile>payments
const paymentValue = document.getElementById("id_value");
paymentValue.setAttribute("readonly", "readonly");

//handler functions

function alertField(input, message) {
  const invalidField = document.getElementById(input);

  var invalidValueField = document.createElement("p");
  invalidValueField.classList.add("invalid-feedback");
  var invalidText = document.createTextNode(message);
  invalidValueField.appendChild(invalidText);
  invalidField.parentElement.appendChild(invalidValueField);
  const lista = invalidValueField.parentElement.children;
  for (item of lista) {
    item.style.display = "block";
  }
  invalidField.classList.add("is-invalid");
  invalidField.focus();
}

function validateVoucherFile() {
  var _validFileExtensions = [".jpg", ".jpeg"];
  if (voucherImg.type == "file") {
    var sFileName = voucherImg.value;
    var blnValid = false;
    for (var j = 0; j < _validFileExtensions.length; j++) {
      var sCurExtension = _validFileExtensions[j];
      if (
        sFileName
          .substr(sFileName.length - sCurExtension.length, sCurExtension.length)
          .toLowerCase() == sCurExtension.toLowerCase()
      ) {
        blnValid = true;
        break;
      }
    }
    if (blnValid == false) {
      return false;
    }
  }
  return true;
}

//verifica se todos os campos estão válidos no formulário antes de salvar
function checkForm() {
  const message = "Don't forget this field.";
  if (bancFlagField.value == "") {
    alertField("id_bank_flag", message);
    return false;
  }
  if (ctrlNumberField.value == "") {
    alertField("id_ctrl_number", message);
    return false;
  }
  if (voucherImg.value == "") {
    const message = "Please send a voucher for your pay.";
    alertField("id_voucher_img", message);
    return false;
  }
  if (validateVoucherFile() == false) {
    const message = "Invalid voucher! .jpg files only";
    alertField("id_voucher_img", message);
    return false;
  }
  document.getElementById("form").submit();
}
