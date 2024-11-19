const fileInput = document.getElementById("fileUpload");
const imageOutput = document.getElementById("output");

fileInput.addEventListener("change", async () => {
    let [file] = fileInput.files;

    if (!file) {
        alert("No file selected!");
        return;
    }

    // Previsualización de la imagen
    const reader = new FileReader();
    reader.onload = (e) => {
        imageOutput.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Subida a Cloudinary
    
    
});


function uploadImage() {
    const cloudName = 'dtb2lrzet'; // Your Cloudinary cloud name
    const uploadPreset = 'Outfitter'; // The unsigned upload preset you created on Cloudinary
    const uploadUrl = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;

    // Prepare form data to send with the request
    const formData = new FormData();
    
    // Append the file to the form data
    formData.append('file', file);
    formData.append('upload_preset', uploadPreset);
    
   
    // Use Fetch API to send a POST request to Cloudinary
    fetch(uploadUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json()) // Parse the JSON response from Cloudinary
    .then(data => {
        if (data.secure_url) {
            console.log('Image uploaded successfully:', data.secure_url);
            // You can use the secure_url to display or save the image
        } else {
            console.error('Error uploading image:', data);
        }
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
}


    fetch("/upload-to-cloudinary/", {
        method: "POST",
        body: JSON.stringify({ url: secure_url }),
    }).then((response) => {
        console.log(response);
    }).then((data) => {
        //despues de que se sube la imagen
    }).catch((error) => {
        console.error("Error:", error);
    });
