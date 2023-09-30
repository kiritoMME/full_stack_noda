// LOGOUT WARNING

const logoutBtn = document.querySelector("#logoutBtn")
const overlay = document.querySelector(".overlay")
const confirmLogout = document.querySelector(".confirm-logout")

logoutBtn.addEventListener("click", () => {
  overlay.style.display = 'block'
  confirmLogout.style.display = 'block'
})

let removeOverlay = () => {
  overlay.style.display = 'none'
  confirmLogout.style.display = 'none'
}

overlay.addEventListener("click", removeOverlay)

document.querySelector("#cancelLogout").addEventListener("click", removeOverlay)