;(function () {
  // Response targeting #formBody => show the modal
  htmx.on("#modalForm", "htmx:afterSwap", (event) => {
    if (event.detail.target.id == "formBody") {
      $('#modalForm').modal('show');
    }
  })
  
  // Empty response targeting #formBody => hide the modal
  htmx.on("#modalForm", "htmx:beforeSwap", (event) => {
    if (event.detail.target.id == "formBody" && !event.detail.xhr.response) {
      $('#modalForm').modal('hide');
    }
  })

  // Close modal by event
  htmx.on("closeModal", () => {$('#modalForm').modal('hide')})
  
  // Close modal (old style)
  htmx.on("#modalForm", "htmx:beforeSend", (e) => {
    $('#modalForm').modal('hide');
  });

  // Remove #formBody content after hiding
  htmx.on("#modalForm", "hidden.bs.modal", () => {
    $("#formBody").empty();
  })
})()