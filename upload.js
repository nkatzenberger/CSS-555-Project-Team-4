function uploadFile() {
    console.log("uploadFile start");
    var fileInput = document.getElementById('up');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('response').innerHTML = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
    console.log("uploadFile end");
  }