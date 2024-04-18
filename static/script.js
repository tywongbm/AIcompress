function showSecondOption() {
    var secondOption = document.querySelector('.second-option');
    secondOption.style.display = 'block';
}

function hideSecondOption() {
    var secondOption = document.querySelector('.second-option');
    secondOption.style.display = 'none';

    var compressionTypeRadios = document.getElementsByName('compression-type');
    for (var i = 0; i < compressionTypeRadios.length; i++) {
        compressionTypeRadios[i].checked = false;
    } 
}


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


function handleFiles(files) {

    //setting check
    const firstOption = document.querySelector('.first-option input[name="compression"]:checked');
    const secondOption = document.querySelector('.second-option input[name="compression-type"]:checked');

    if (!firstOption) {
        console.log('Upload fail, please select first option');
        return;
    }

    if (firstOption.value === 'compress' && !secondOption) {
        console.log('Upload fail, please select second option');
        return;
    }

    const file = files[0];
    const fileName = file.name;
    const fileExtension = fileName.split('.').pop();

    if (firstOption.value === 'compress' && fileExtension !== 'jpg') {
        console.log('Upload fail, only support .jpg file');
        return;
    }

    if (firstOption.value === 'decompress' && fileExtension !== 'zip') {
        console.log('Upload fail, only support .zip file');
        return;
    }


    // Uploading
    uploadRegion.classList.add('uploading');
    uploadRegion.querySelector('.waiting').style.display = 'none';
    uploadRegion.querySelector('.uploading').style.display = 'block';
    console.log("uploading")

    const formData = new FormData();
    formData.append('file', file); // 将文件添加到FormData对象中

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        uploadRegion.classList.remove('uploading');
        uploadRegion.classList.add('processing');
        uploadRegion.querySelector('.uploading').style.display = 'none';
        uploadRegion.querySelector('.processing').style.display = 'block';
        console.log("processing")
        return response.blob()
    })
    .then(blob => {
        uploadRegion.classList.remove('processing');
        uploadRegion.classList.add('success');
        uploadRegion.querySelector('.processing').style.display = 'none';
        uploadRegion.querySelector('.success').style.display = 'block';
        console.log("success")

        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'processed_image.jpg';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        console.log("downloading");
    })
    .catch(error => {
        uploadRegion.classList.remove('processing');
        uploadRegion.classList.add('failure');
        uploadRegion.querySelector('.processing').style.display = 'none';
        uploadRegion.querySelector('.failure').style.display = 'block';
        console.error(error);
    });
}

const tryAgain = document.getElementById('try-again');
tryAgain.addEventListener('click', (e) => {
    e.preventDefault();
    uploadRegion.classList.remove('success');
    uploadRegion.querySelector('.success').style.display = 'none';
    uploadRegion.querySelector('.failure').style.display = 'none';
    uploadRegion.querySelector('.waiting').style.display = 'block';
  });
