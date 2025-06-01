document.addEventListener("DOMContentLoaded", function () {
    const productsList = document.getElementById('productsList');
    const products = document.querySelectorAll('.product');
    const cartItems = document.querySelector('.cart-items');
    const cartTotal = document.querySelector('.cart-total');
    const searchInput = document.getElementById('searchInput');
    const cartCountElement = document.getElementById('cart-count');

    // Limpia el carrito si se completó el pago
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('pago_exitoso') === 'True') {
        localStorage.removeItem("cart");
        localStorage.removeItem("carrito_cantidad");
        localStorage.removeItem("carrito_total");

        if (cartItems) {
            cartItems.innerHTML = "<li>Tu carrito está vacío.</li>";
        }
        if (cartTotal) {
            cartTotal.innerText = "Total: $0.00";
        }
        if (cartCountElement) {
            cartCountElement.innerText = "0";
        }
    }

    // Carga del carrito desde localStorage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    updateCart();
    // Enviar al servidor
fetch('/agregar_producto_carrito', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name,
        price,
        quantity: 1 // ya que recién se está agregando
    })
}).then(response => response.json())
  .then(data => {
      console.log(data.mensaje || data.error);
  }).catch(error => {
      console.error("Error al enviar al backend:", error);
  });

    // Agregar producto al carrito
    if (productsList) {
        productsList.addEventListener('click', (event) => {
            if (event.target.classList.contains('add-to-cart')) {
                const product = event.target.closest('.product');
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
    }

    // Actualizar visual del carrito
    function updateCart() {
        cartItems.innerHTML = '';
        let total = 0;

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
        });

        cartTotal.textContent = `Total: $${total.toFixed(2)}`;
        const itemCount = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCountElement.textContent = itemCount;

        // Guardar total y cantidad en otras claves (opcional, si los usas en otros scripts)
        localStorage.setItem("carrito_cantidad", itemCount);
        localStorage.setItem("carrito_total", total.toFixed(2));
    }

    // Eliminar producto del carrito
    cartItems.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-item')) {
            const productName = event.target.dataset.name;
            cart = cart.filter(item => item.name !== productName);
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCart();
        }
    });

    // Filtro de búsqueda
    searchInput.addEventListener('input', function () {
        const searchTerm = searchInput.value.toLowerCase();
        Array.from(products).forEach(product => {
            const productName = product.dataset.name.toLowerCase();
            product.style.display = productName.includes(searchTerm) ? 'block' : 'none';
        });
    });
});
