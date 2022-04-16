modal = document.getElementById('orderModal');
divIdEvent = document.getElementById('div_id_event');
idEvent = document.getElementById('id_event');
idPaytype = document.getElementById("id_paytype");

// default 
$(modal).ready((event) => {
  idEvent.removeAttribute('required')
  divIdEvent.classList.add('d-none');
});

// show inputs if paytype is 'Conference'
idPaytype.addEventListener("blur", (event) => {
  if (idPaytype.value == "1") {
    idEvent.setAttribute('required', '');
    divIdEvent.classList.remove('d-none');
  } else {
    idEvent.removeAttribute('required')
    divIdEvent.classList.add('d-none');
  }
});