const productsList = document.getElementById('productsList');
        const products = document.querySelectorAll('.product');
        const cartItems = document.querySelector('.cart-items');
        const cartTotal = document.querySelector('.cart-total');
        const searchInput = document.getElementById('searchInput');

        let total = 0;
        const cart = [];

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
                updateCart();
            }
        });

        function updateCart() {
            cartItems.innerHTML = '';
            total = 0;

            cart.forEach(item => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <img src="${item.image}" alt="${item.name}" style="width: 50px;">
                    <span>${item.name}</span>
                    <span>$${(item.price * item.quantity).toFixed(2)}</span>
                    <button class="remove-item" data-name="${item.name}">Eliminar</button>
                `;
                cartItems.appendChild(listItem);
                total += item.price * item.quantity;
            });
            cartTotal.textContent = `Total: $${total.toFixed(2)}`;
        }

        cartItems.addEventListener('click', (event) => {
            if (event.target.classList.contains('remove-item')) {
                const productName = event.target.dataset.name;
                const index = cart.findIndex(item => item.name === productName);
                if (index !== -1) {
                    cart.splice(index, 1);
                    updateCart();
                }
            }
        });

        searchInput.addEventListener('input', function() {
            const searchTerm = searchInput.value.toLowerCase();
            Array.from(products).forEach(product => {
                const productName = product.dataset.name.toLowerCase();
                if (productName.includes(searchTerm)) {
                    product.style.display = 'block';
                } else {
                    product.style.display = 'none';
                }
            });
        });