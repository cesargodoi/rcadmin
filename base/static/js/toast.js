;(function () {
  var myToast = document.getElementById("toast")
  var toastBody = document.getElementById("toastBody")
  var toast = new bootstrap.Toast(myToast, { delay: 8000 })

  htmx.on("showToast", (event) => {
    toastBody.innerText = event.detail.value;
    toast.show();
  })
})()