document.addEventListener("DOMContentLoaded", () => {
    const userIcon = document.getElementById("userIcon");
    const dropdownMenu = document.getElementById("dropdownMenu");

    userIcon.addEventListener("click", (event) => {
        event.stopPropagation();
        dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block";
    });

    document.addEventListener("click", (event) => {
        if (!userIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = "none";
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    const cartContainer = document.getElementById("cartItemsContainer");
    const emptyMessage = document.getElementById("emptyMessage");

    if (cartItems.length > 0) {
        emptyMessage.style.display = "none";
        cartItems.forEach((item, index) => {
            const cartItemElement = document.createElement("div");
            cartItemElement.classList.add("cart-item");
            cartItemElement.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <div class="cart-item-info">
                    <h3>${item.name}</h3>
                    <p class="price">${item.price}</p>
                </div>
                <button class="remove-item" data-index="${index}">X</button>
            `;
            cartContainer.appendChild(cartItemElement);
        });

        // Eliminar producto del carrito
        document.querySelectorAll(".remove-item").forEach(button => {
            button.addEventListener("click", function () {
                let index = this.getAttribute("data-index");
                cartItems.splice(index, 1);
                localStorage.setItem("cartItems", JSON.stringify(cartItems));
                window.location.reload();
            });
        });
    }
});