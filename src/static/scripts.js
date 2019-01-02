document.addEventListener("DOMContentLoaded", function(){
  document.getElementById('stlfile').onchange = function () {
    document.getElementById('uploadtext').textContent = "Vorschau wird berechnet";
    document.getElementById("slicerForm").submit();
  };
});