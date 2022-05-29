const searchForm = document.getElementById("searchForm");
const personName = document.getElementById("personName");
const personNames = document.getElementById('personNames');
const toChange = document.getElementById('toChange');
const paymentsDiv = document.getElementById("paymentsDiv");
const payformsDiv = document.getElementById("payformsDiv");
const othersDiv = document.getElementById("othersDiv");
const totalPayments = document.getElementById('totalPayments');
const totalPayforms = document.getElementById('totalPayforms');
const due = document.getElementById('due');
const buttonPay = document.getElementById('payNow');


// onload page
document.body.addEventListener('htmx:load', (event) => {
  // personName -> paymentsDiv
  if (personName.innerText) {
    searchForm.classList.add('d-none');
    toChange.classList.remove('d-none');
    paymentsDiv.classList.remove('d-none');
    // paymentsDiv -> payformsDiv
    if (totalPayments.innerText != '0,00') {
      payformsDiv.classList.remove('d-none');
      // payformsDiv -> othersDiv
      if (totalPayforms.innerText == totalPayments.innerText) {
        othersDiv.classList.remove('d-none');
        due.parentElement.classList.add('d-none')
        buttonPay.parentElement.classList.remove('d-none');
      } else {
        othersDiv.classList.add('d-none');
        buttonPay.parentElement.classList.add('d-none');
      }
    } else {
      payformsDiv.classList.add('d-none');
    }
  } else {
    searchForm.classList.remove('d-none');
    toChange.classList.add('d-none');
  };
})

// on change name
htmx.on("#personName", "htmx:beforeSwap", (event) => {
  searchForm.classList.add('d-none');
  toChange.classList.remove('d-none');
  paymentsDiv.classList.remove('d-none');
});

// click on toChange link
htmx.on("#toChange", "click", (event) => {
  searchForm.classList.remove('d-none');
  toChange.classList.add('d-none');
  personName.innerText = '';
  searchForm.children[0].children[0].value = '';
  if (personNames.children[0]) {
    personNames.children[0].innerHTML = '';
  }
});

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
  } else {
    totalPayments.innerText = '0,00';
  }

  // payforms
  const payforms = document.getElementById('payforms');
  let _totalPayforms = 0;
  for (let i = 0; i < payforms.childElementCount; i++) {
    value = payforms.children[i].children[2].innerText;
    _totalPayforms += parseFloat(value.replace(',', '.'));
  }
  if (_totalPayforms != 0) {
    totalPayforms.innerText = _totalPayforms.toFixed(2).replace('.', ',');
  } else {
    totalPayforms.innerText = '0,00';
  }

  // due
  let _due = _totalPayments - _totalPayforms;
  due.innerText = _due.toFixed(2).replace('.', ',');
  if (_due == 0) {
    due.parentElement.classList.add('d-none')
    // $('#showDue').addClass('d-none');
  } else {
    due.parentElement.classList.remove('d-none')
    // $('#showDue').removeClass('d-none');
  }
});