const pendingDiv = document.querySelector("div.pending")
const shippingDiv = document.querySelector("div.shipping")
const shippedDiv = document.querySelector("div.shipped")
const pendingBtn = document.querySelector("button.pending")
const shippingBtn = document.querySelector("button.shipping")
const shippedBtn = document.querySelector("button.shipped")

pendingBtn.addEventListener("click", () => {
    pendingDiv.classList.add("show")
    shippingDiv.classList.remove("show")
    shippedDiv.classList.remove("show")
    
    pendingBtn.classList.add("show")
    shippingBtn.classList.remove("show")
    shippedBtn.classList.remove("show")
})

shippingBtn.addEventListener("click", () => {
    shippingDiv.classList.add("show")
    pendingDiv.classList.remove("show")
    shippedDiv.classList.remove("show")
    
    shippingBtn.classList.add("show")
    pendingBtn.classList.remove("show")
    shippedBtn.classList.remove("show")
})

shippedBtn.addEventListener("click", () => {
    shippedDiv.classList.add("show")
    pendingDiv.classList.remove("show")
    shippingDiv.classList.remove("show")

    shippedBtn.classList.add("show")
    pendingBtn.classList.remove("show")
    shippingBtn.classList.remove("show")
})