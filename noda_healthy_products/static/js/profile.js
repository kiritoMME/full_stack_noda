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

// VALIDATION

// Example starter JavaScript for disabling form submissions if there are invalid fields

'use strict'

// Fetch all the forms we want to apply custom Bootstrap validation styles to
const forms = document.querySelectorAll('.needs-validation')

// Loop over them and prevent submission
Array.from(forms).forEach(form => {
  form.addEventListener('submit', event => {
    if (!form.checkValidity()) {
      event.preventDefault()
      event.stopPropagation()
    }

    form.classList.add('was-validated')
  }, false)
})