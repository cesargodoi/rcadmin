modal = document.getElementById('orderModal');
idPayformType = document.getElementById("id_payform_type");
divIdBankFlag = document.getElementById("div_id_bank_flag");
divIdCtrlNumber = document.getElementById("div_id_ctrl_number");
divIdComplement = document.getElementById("div_id_complement");
divIdVoucherImg = document.getElementById("div_id_voucher_img");

// default 
$(modal).ready((event) => {
  divIdBankFlag.classList.add('d-none');
  divIdCtrlNumber.classList.add('d-none');
  divIdComplement.classList.add('d-none');
  divIdVoucherImg.classList.add('d-none');
});

// show inputs if payfom type !cash
idPayformType.addEventListener("blur", (event) => {
  if (idPayformType.value != "CSH") {
    divIdBankFlag.classList.remove('d-none');
    divIdCtrlNumber.classList.remove('d-none');
    divIdComplement.classList.remove('d-none');
  } else {
    divIdBankFlag.classList.add('d-none');
    divIdCtrlNumber.classList.add('d-none');
    divIdComplement.classList.add('d-none');
  }
});