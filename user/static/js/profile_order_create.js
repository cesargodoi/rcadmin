const idBankFlag = document.getElementById("id_bank_flag");
const idCtrlNumber = document.getElementById("id_ctrl_number");
const idVoucherImg = document.getElementById("id_voucher_img");
const payNowButton = document.getElementById('payNow');

// enabling the 'Pay now' button
idBankFlag.addEventListener("blur", (event) => enablingPayNow())
idCtrlNumber.addEventListener("blur", (event) => enablingPayNow())
idVoucherImg.addEventListener("blur", (event) => enablingPayNow())

function enablingPayNow() {
  if (idBankFlag.value != "" && idCtrlNumber.value != "" && idVoucherImg.value != "") {
    payNowButton.classList.remove('d-none');
  } else {
    payNowButton.classList.add('d-none');
  }
};

const paymentsDiv = document.getElementById("paymentsDiv");
const payformDiv = document.getElementById("payformDiv");
const totalPayments = document.getElementById('totalPayments');
const payformValue = document.getElementById('id_value');
const buttonPay = document.getElementById('payNow');

// onload page
document.body.addEventListener('htmx:load', (event) => {
  if (totalPayments.innerText != '0,00') {
    payformDiv.classList.remove('d-none');
  } else {
    payformDiv.classList.add('d-none');
  }
})

// onFly
document.body.addEventListener('htmx:afterSwap', function (evt) {
  // payments
  const payments = document.getElementById('payments');
  let _totalPayments = 0;
  for (let i = 0; i < payments.childElementCount; i++) {
    value = payments.children[i].children[2].innerText;
    _totalPayments += parseFloat(value.replace(',', '.'));
  }
  if (_totalPayments != 0) {
    totalPayments.innerText = _totalPayments.toFixed(2).replace('.', ',');
    payformValue.value = _totalPayments.toFixed(2);
  } else {
    totalPayments.innerText = '0,00';
    payformValue.value = '0.00';
  }
});