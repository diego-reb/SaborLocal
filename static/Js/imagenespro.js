function mostrarNombreArchivo(input) {
    const fileNameSpan = document.getElementById('file-name');
    if (input.files && input.files[0]) {
        fileNameSpan.textContent = input.files[0].name;
    } else {
        fileNameSpan.textContent = "Haz clic aquí para seleccionar una imagen";
    }
}