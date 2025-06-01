document.addEventListener("DOMContentLoaded", function () {
    const productsList = document.getElementById('productsList');
    const cartItems = document.querySelector('.cart-items');
    const cartTotal = document.querySelector('.cart-total');
    const cartCountElement = document.getElementById("cart-count");

    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    updateCart();

    productsList.addEventListener('click', (event) => {
        if (event.target.classList.contains('add-to-cart')) {
            const product = event.target.parentElement;
            const name = product.dataset.name;
            const price = parseFloat(product.dataset.price);
            const image = product.dataset.image;

            const existingProduct = cart.find(item => item.name === name);

            if (existingProduct) {
                existingProduct.quantity++;
            } else {
                cart.push({ name, price, image, quantity: 1 });
            }

            localStorage.setItem("cart", JSON.stringify(cart));
            updateCart();
        }
    });

    function updateCart() {
        cartItems.innerHTML = '';
        let total = 0;
        let itemCount = 0;

        cart.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" style="width: 50px;">
                <span>${item.name} x${item.quantity}</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
                <button class="remove-item" data-name="${item.name}">Eliminar</button>
            `;
            cartItems.appendChild(listItem);
            total += item.price * item.quantity;
            itemCount += item.quantity;
        });

        cartTotal.textContent = `Total: $${total.toFixed(2)}`;
        cartCountElement.textContent = itemCount;
    }

    cartItems.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-item')) {
            const productName = event.target.dataset.name;
            cart = cart.filter(item => item.name !== productName);
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCart();
        }
    });
});

//para agregar al carrito en promocion 
let cart = JSON.parse(localStorage.getItem('cart')) || []; // Recuperar carrito desde localStorage o inicializarlo vacío

document.querySelectorAll('.boton-comprar').forEach(function(button, index) {
    button.addEventListener('click', function() {
        let product = document.querySelectorAll('.promocion')[index]; // Obtener el producto correspondiente
        let productName = product.querySelector('h3').textContent;
        let productPrice = product.querySelector('.precio-descuento').textContent;

        let productToAdd = {
            name: productName,
            price: productPrice
        };

        // Agregar el producto al carrito
        cart.push(productToAdd);
        localStorage.setItem('cart', JSON.stringify(cart)); // Guardar carrito en localStorage

        updateCartCount(); // Actualizar el contador del carrito
    });
});

function updateCartCount() {
    let cartCount = document.getElementById('cart-count');
    cartCount.textContent = cart.length; // Actualiza el contador con la cantidad de productos en el carrito
}

updateCartCount(); // Inicializa el contador al cargar la página
