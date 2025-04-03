//contador de carrito
document.addEventListener("DOMContentLoaded", function () {
    const cartContainer = document.querySelector('.cart-items');
    const cartTotal = document.querySelector('.cart-total');
    const cartCountElement = document.getElementById("cart-count");

    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    updateCart();

    function updateCart() {
        cartContainer.innerHTML = '';
        let total = 0;
        let itemCount = 0;

        if (cart.length === 0) {
            cartContainer.innerHTML = '<p>Tu carrito está vacío.</p>';
            cartTotal.textContent = 'Total: $0.00';
            cartCountElement.textContent = '0';
            return;
        }

        cart.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" style="width: 50px;">
                <span>${item.name} x${item.quantity}</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
                <button class="remove-item" data-name="${item.name}">Eliminar</button>
            `;
            cartContainer.appendChild(listItem);
            total += item.price * item.quantity;
            itemCount += item.quantity;
        });

        cartTotal.textContent = `Total: $${total.toFixed(2)}`;
        cartCountElement.textContent = itemCount;
    }

    cartContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-item')) {
            const productName = event.target.dataset.name;
            cart = cart.filter(item => item.name !== productName);
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCart();
        }
    });
});
//agregar y eliminar productos de carrito
document.addEventListener("DOMContentLoaded", function () {
    let cart = JSON.parse(localStorage.getItem("cart")) || []; 
    const cartCountElement = document.getElementById("cart-count");
    const cartContainer = document.querySelector(".cart-items"); 

    function updateCartDisplay() {
        cartContainer.innerHTML = "";
        let total = 0;

        cart.forEach((item, index) => {
            const listItem = document.createElement("li");
            listItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" width="50">
                <span>${item.name}</span>
                <span>$${(item.price * item.quantity).toFixed(2)}</span>
                <button class="remove-item" data-index="${index}">Eliminar</button>
            `;
            cartContainer.appendChild(listItem);
            total += item.price * item.quantity;
        });

        document.querySelector(".cart-total").textContent = `Total: $${total.toFixed(2)}`;
        cartCountElement.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
    }

    document.querySelectorAll(".add-to-cart").forEach((button) => {
        button.addEventListener("click", function () {
            const productElement = this.parentElement;
            const name = productElement.querySelector("h3").textContent;
            const price = parseFloat(productElement.querySelector(".price").textContent.replace("$", ""));
            const image = productElement.querySelector("img").src;

            const existingProduct = cart.find((item) => item.name === name);

            if (existingProduct) {
                existingProduct.quantity++;
            } else {
                cart.push({ name, price, image, quantity: 1 });
            }

            localStorage.setItem("cart", JSON.stringify(cart));
            updateCartDisplay();
        });
    });

    cartContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("remove-item")) {
            const index = event.target.dataset.index;
            cart.splice(index, 1);
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCartDisplay();
        }
    });

    updateCartDisplay();
});

