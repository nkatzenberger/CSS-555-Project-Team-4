function uploadFile() {
    let inputElem = document.getElementById('up');
    let file = inputElem.files[0];

    if (!file) {
        document.getElementById('uploadStatus').innerText = 'No file selected.';
        return;
    }

    // Show loading spinner
    document.getElementById('loading').style.display = 'block';

    let formData = new FormData();
    formData.append('file', file);

    fetch('/upload',{
        method: 'POST',
        body: formData,
        mode: 'no-cors',
        credentials: "same-origin",
        dataType: 'mat',
        headers: {
            "Content-Type": "multipart/form-data, text/plain",
            "Accept" : "multipart/form-data, text/plain",
    }, 
    })
    .then(response => {
        return response.text();
    })
    .then(data => {
        document.getElementById('response').innerHTML = data;
        document.getElementById('uploadStatus').innerText = 'Upload successful';
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('uploadStatus').innerText = 'Upload failed';
    })
    .finally(() => {
        // Hide loading spinner
        document.getElementById('loading').style.display = 'none';
    });   
}

function uuidv4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16)
    );
}
