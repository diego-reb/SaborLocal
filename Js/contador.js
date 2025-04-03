document.addEventListener("DOMContentLoaded", function() {
    let cartCount = 0; // Contador del carrito
    const cartCountElement = document.getElementById("cart-count");

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function() {
            cartCount++; // Incrementa el contador
            cartCountElement.textContent = cartCount; // Actualiza el número en el carrito
        });
    });
});