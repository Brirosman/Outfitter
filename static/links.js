const fileInput = document.getElementById("fileElem"); // Coincide con el ID en links.html
const imageOutput = document.getElementById("output"); // Asegúrate de que exista en HTML
let selectedFile; // Hacer que el archivo esté disponible globalmente

fileInput.addEventListener("change", () => {
    let [file] = fileInput.files;

    if (!file) {
        alert("No file selected!");
        return;
    }

    selectedFile = file; // Guarda el archivo para uso posterior

    // Previsualización de la imagen
    const reader = new FileReader();
    reader.onload = (e) => {
        if (imageOutput) {
            imageOutput.src = e.target.result; // Muestra la imagen si hay un elemento <img>
        }
    };
    reader.readAsDataURL(file);
});

function uploadImage() {
    if (!selectedFile) {
        alert("No hay archivo seleccionado para subir.");
        return;
    }

    const cloudName = 'dtb2lrzet'; // Cloudinary cloud name
    const uploadPreset = 'Outfitter'; // Cloudinary unsigned upload preset
    const uploadUrl = `https://api.cloudinary.com/v1_1/${cloudName}/upload`;

    // Configura los datos del formulario
    const data = new FormData();
    data.append("file", file);
    data.append("upload_preset", "default-preset");

    // Envía la solicitud a Cloudinary
    fetch(uploadUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.secure_url) {
            console.log('Imagen subida exitosamente:', data.secure_url);
            alert(`Imagen subida correctamente: ${data.secure_url}`);
        } else {
            console.error('Error al subir imagen:', data);
            alert('Hubo un problema al subir la imagen.');
        }
    })
    .catch(error => {
        console.error('Error al subir imagen:', error);
        alert('Error al conectar con Cloudinary.');
    });
}
