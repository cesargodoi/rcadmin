//fields
var typeWorkGroup = document.getElementById("id_workgroup_type");
var aspectWorkGroup = document.getElementById("id_aspect");
var divAspectChoice = document.getElementById("div_id_aspect");

//makes Aspect field appear when clicking outside the Type field
typeWorkGroup.addEventListener("onload", displayAspectChoices());
typeWorkGroup.addEventListener("input", (e) => {displayAspectChoices()});

function displayAspectChoices() {
  if (typeWorkGroup.value == "ASP") {
    divAspectChoice.style.display = "block";
  } else {
    aspectWorkGroup.item(0).selected = true;
    divAspectChoice.style.display = "none";
  }
}