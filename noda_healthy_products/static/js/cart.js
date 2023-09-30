// TOTAL PRICE OF THE CART

const productPrices = document.querySelectorAll(".total-price")

let totalPrice = 0

productPrices.forEach(element => {
  totalPrice += parseInt(element.textContent)
})

document.querySelector(".all-total-price").innerHTML = totalPrice