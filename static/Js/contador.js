document.addEventListener("DOMContentLoaded", function () {
    const cartCountElement = document.getElementById("cart-count");

    // Leer cantidad actual desde localStorage o poner 0 si no hay nada
    let cartCount = parseInt(localStorage.getItem("carrito_cantidad")) || 0;
    cartCountElement.textContent = cartCount;

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            // Sumar 1 producto
            cartCount++;
            localStorage.setItem("carrito_cantidad", cartCount); // Actualiza en localStorage
            cartCountElement.textContent = cartCount; // Muestra en pantalla
        });
    });
});
