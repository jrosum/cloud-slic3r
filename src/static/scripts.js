document.addEventListener("DOMContentLoaded", function(){
  document.getElementById('stlfile').onchange = function () {

    var formData = new FormData();
    var fileField = document.querySelector("input[type='file']");

    formData.append('stlfile', fileField.files[0]);

    fetch('/uploader', {
      method: 'POST',
      body: formData
    })
    .then(response => console.log(response))
    .catch(error => console.error('Error:', error))
    .then(response => console.log('Success:', JSON.stringify(response)));

    document.getElementById('uploadtext').textContent = this.files.length + " STL ausgewählt";
  };
});