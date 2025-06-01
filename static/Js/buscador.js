document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const promocionesList = document.getElementById('promocionesList');
    const promociones = promocionesList.getElementsByClassName('promocion');

    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();

        Array.from(promociones).forEach(promocion => {
            const promocionName = promocion.querySelector('h3').textContent.toLowerCase();
            if (promocionName.includes(searchTerm)) {
                promocion.style.display = 'block';
            } else {
                promocion.style.display = 'none';
            }
        });
    });
});

document.getElementById('searchInput').addEventListener('input', function() {
    let searchTerm = this.value.toLowerCase(); // Obtener el valor del campo de búsqueda y convertirlo a minúsculas
    let products = document.querySelectorAll('.product'); // Seleccionar todos los productos

    products.forEach(function(product) {
        let productName = product.querySelector('h3').textContent.toLowerCase(); // Obtener el nombre del producto y convertirlo a minúsculas
        if (productName.includes(searchTerm)) {
            product.style.display = ''; // Si el nombre del producto contiene el término de búsqueda, mostrar el producto
        } else {
            product.style.display = 'none'; // Si no coincide, ocultar el producto
        }
    });
});
// buscador de promocion
document.getElementById('searchInput').addEventListener('input', function() {
    let searchTerm = this.value.toLowerCase(); // Obtener el valor del campo de búsqueda y convertirlo a minúsculas
    let promociones = document.querySelectorAll('.promocion'); // Seleccionar todos los productos (promociones)

    promociones.forEach(function(promocion) {
        let promocionName = promocion.querySelector('h3').textContent.toLowerCase(); // Obtener el nombre del producto
        if (promocionName.includes(searchTerm)) {
            promocion.style.display = ''; // Mostrar la promoción si coincide
        } else {
            promocion.style.display = 'none'; // Ocultar la promoción si no coincide
        }
    });
});
