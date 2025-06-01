document.addEventListener("DOMContentLoaded", function () {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    const cartCountElement = document.getElementById("cart-count");
    const cartContainer = document.querySelector(".cart-items");
    const cartTotal = document.querySelector(".cart-total");

    function updateCartCount() {
        const totalQuantity = cart.reduce((sum, item) => sum + item.quantity, 0);
        localStorage.setItem("carrito_cantidad", totalQuantity);
        cartCountElement.textContent = totalQuantity;
    }

    function saveCart() {
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCartCount();
    }

    function updateCartDisplay() {
        cartContainer.innerHTML = "";
        let total = 0;

        if (cart.length === 0) {
            cartContainer.innerHTML = "<p>Tu carrito está vacío.</p>";
            cartTotal.textContent = "Total: $0.00";
            cartCountElement.textContent = "0";
            localStorage.removeItem("carrito_cantidad");
            return;
        }

        cart.forEach((item, index) => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" width="50">
                <span>${item.name} x${item.quantity}</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
                <button class="remove-item" data-index="${index}">Eliminar</button>
            `;
            cartContainer.appendChild(listItem);
            total += item.price * item.quantity;
        });

        cartTotal.textContent = `Total: $${total.toFixed(2)}`;
        updateCartCount();
    }

    document.querySelectorAll(".add-to-cart").forEach((button) => {
        button.addEventListener("click", function () {
            const productElement = this.closest(".product") || this.parentElement;
            const name = productElement.querySelector("h3").textContent;
            const price = parseFloat(productElement.querySelector(".price").textContent.replace("$", ""));
            const image = productElement.querySelector("img").src;

            const existingProduct = cart.find((item) => item.name === name);
            if (existingProduct) {
                existingProduct.quantity++;
            } else {
                cart.push({ name, price, image, quantity: 1 });
            }

            saveCart();
            updateCartDisplay();
        });
    });

    cartContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-item")) {
            const index = parseInt(event.target.dataset.index);
            cart.splice(index, 1);
            saveCart();
            updateCartDisplay();
        }
    });

    // Mostrar carrito al cargar
    updateCartDisplay();
});
document.getElementById("buyNowButton").addEventListener("click", function () {
    const carrito = localStorage.getItem("carrito");
    if (!carrito || carrito.length === 0) {
        alert("Tu carrito está vacío.");
        return;
    }

    // Coloca el carrito en el input oculto
    document.getElementById("carritoInput").value = carrito;

    // Envía el formulario hacia /pago
    document.getElementById("carritoForm").submit();
});