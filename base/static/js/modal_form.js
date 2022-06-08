;(function () {
  // When the #modalForm has content => show the #modalForm
  htmx.on("#modalForm", "htmx:afterSwap", (e) => {
    $('#modalForm').modal('show');
  });

  // When the #modalForm is sent => hide the #modalForm
  htmx.on("#modalForm", "htmx:beforeSend", (e) => {
    $('#modalForm').modal('hide');
  });

  // Remove formBody content after hiding
  $("#modalForm").on("hidden.bs.modal", () => {
    $("#formBody").empty();
  })
})()