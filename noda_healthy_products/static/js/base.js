const cartItemsNo = document.querySelector("span.cart-items-no")

setInterval(() => {
    console.log(cartItemsNo.textContent)
    if (cartItemsNo.textContent == '0') {
        cartItemsNo.classList.add("no")
    } else {
        cartItemsNo.classList.remove("no")
    }
}, 400);