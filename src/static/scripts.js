document.addEventListener("DOMContentLoaded", function(){
  document.getElementById('stlfile').onchange = function () {
    document.getElementById('uploadtext').textContent = this.files.length + " STL ausgewählt";
  };
});