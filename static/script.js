//option1 style
const radioButtons = document.getElementsByName('compression-type');
const labels = document.getElementsByClassName('radio-button');

for (let i = 0; i < radioButtons.length; i++) {
  if (radioButtons[i].checked) {
    const label = radioButtons[i].parentNode;
    label.classList.add('selected');
    break;
  }
}

for (let i = 0; i < radioButtons.length; i++) {
  radioButtons[i].addEventListener('click', function() {
    for (let j = 0; j < labels.length; j++) {
      labels[j].classList.remove('selected');
    }

    if (this.checked) {
      const label = this.parentNode;
      label.classList.add('selected');
    }
  });
}


//option3 and 4 visible
const firstOption = document.querySelector('.first-option');
const secondOption = document.querySelector('.second-option');
const thirdOption = document.querySelector('.third-option');
const fourthOption = document.querySelector('.fourth-option');
const rangeInput = document.querySelector('input[name="quality"]');

firstOption.addEventListener('change', handleOptionChange);
secondOption.addEventListener('change', handleOptionChange);

function handleOptionChange() {
    const compressionType = document.querySelector('input[name="compression-type"]:checked').value;
    const compression = document.querySelector('input[name="compression"]:checked').value;

    if (compressionType === 'lossless' && compression === 'compress') {
        thirdOption.style.display = 'block';
        fourthOption.style.display = 'block';

    }
    else if (compressionType === 'lossless' && compression === 'decompress'){
        fourthOption.style.display = 'none';
        rangeInput.value = 1;
    }
    
    else {
        thirdOption.style.display = 'none';
        fourthOption.style.display = 'none';
        rangeInput.value = 1;
    }
}


//Upload reagion style
const uploadRegion = document.querySelector('.upload-region');

uploadRegion.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadRegion.classList.add('dragover');
});

uploadRegion.addEventListener('dragleave', () => {
    uploadRegion.classList.remove('dragover');
});

uploadRegion.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadRegion.classList.remove('dragover');
    const files = e.dataTransfer.files;
    handleFiles(files);
});

const fileUpload = document.getElementById('file-upload');
fileUpload.addEventListener('change', (e) => {
    const files = e.target.files;
    handleFiles(files);
});

// upload region content change
function updateUploadStatus(uploadRegion, status) {
    const states = ['waiting', 'uploading', 'processing', 'success', 'downloading', 'failure'];

    states.forEach(state => {
        uploadRegion.classList.remove(state);
        const element = uploadRegion.querySelector('.' + state);
        if (element) {
            element.style.display = (state === status) ? 'block' : 'none';
        }
    });

    uploadRegion.classList.add(status);
}

const download = document.getElementById('download-link');
download.addEventListener('click', (e) => {
    updateUploadStatus(uploadRegion, 'downloading');
  });

const tryAgain = document.getElementById('try-again');
tryAgain.addEventListener('click', (e) => {
    e.preventDefault();
    updateUploadStatus(uploadRegion, 'waiting');
  });


function handleFiles(files) {

    //setting check
    const firstOption = document.querySelector('.first-option input[name="compression-type"]:checked');
    const secondOption = document.querySelector('.second-option input[name="compression"]:checked');
    const thirdOption = document.querySelector('.third-option input[name="lossless-model"]:checked');
    const fourthOption = document.querySelector('.fourth-option input[name="quality"]');

    const file = files[0];
    const fileName = file.name;
    const fileExtension = fileName.split('.').pop();

    if (fileExtension !== 'jpg' && fileExtension !== 'png') {
        alert('Upload failed, only support jpg/png file');
        return;
    }

    // Uploading
    updateUploadStatus(uploadRegion, 'uploading');
    console.log("uploading")

    const formData = new FormData();
    formData.append('file', file);
    formData.append('option1', firstOption.value);
    formData.append('option2', secondOption.value);
    formData.append('option3', thirdOption.value);
    formData.append('option4', fourthOption.value);
    console.log(firstOption.value)
    console.log(secondOption.value)
    console.log(thirdOption.value)
    console.log(fourthOption.value)

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        updateUploadStatus(uploadRegion, 'processing');
        console.log("processing")
        return response.json()
    })
    .then(data => {
        updateUploadStatus(uploadRegion, 'success');
        console.log("success")
/*
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'processed_image.jpg';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
*/
        const fileType = data.type;
        const filePath = data.path;
        const link = document.getElementById('download-link');
        link.href = `/download/${fileType}/${filePath}`;
        link.download = fileType === 'image' ? 'output_image.jpg' : 'output_file.py';
        link.style.display = 'block';
        console.log("downloading");
    })
    .catch(error => {
        updateUploadStatus(uploadRegion, 'failure');
        console.error(error);
    });
}
