const shippingDiv = document.querySelector("div.shipping")
const shippedDiv = document.querySelector("div.shipped")
const shippingBtn = document.querySelector("button.shipping")
const shippedBtn = document.querySelector("button.shipped")

shippingBtn.addEventListener("click", () => {
    shippingDiv.classList.add("show")
    shippedDiv.classList.remove("show")
    
    shippingBtn.classList.add("show")
    shippedBtn.classList.remove("show")
})
shippedBtn.addEventListener("click", () => {
    shippedDiv.classList.add("show")
    shippingDiv.classList.remove("show")

    shippedBtn.classList.add("show")
    shippingBtn.classList.remove("show")
})