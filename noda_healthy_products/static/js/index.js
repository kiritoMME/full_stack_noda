// // Testimonials
// const tBoxes = document.querySelectorAll(".testimonials .t-box");
// const tNext = document.querySelector(".change-t-box span:last-of-type");
// const tLast = document.querySelector(".change-t-box span:first-of-type");

// tNext.addEventListener("click", () => {
//   for (let i = 0; i < tBoxes.length - 1; i++) {
//     if (tBoxes[i].classList.contains("active")) {
//       tBoxes[i].classList.remove("active");
//       tBoxes[i + 1].classList.add("active");
//       break;
//     }
//   }
// });

// tLast.addEventListener("click", () => {
//   for (let i = 1; i < tBoxes.length; i++) {
//     if (tBoxes[i].classList.contains("active")) {
//       tBoxes[i].classList.remove("active");
//       tBoxes[i - 1].classList.add("active");
//       break;
//     }
//   }
// });

// // FAQ
// const tabsLinks = document.querySelectorAll(".tabs-list li");
// tabsLinks.forEach((link) => {
//   link.addEventListener("click", () => {
//     if (
//       document.querySelector(link.dataset.answer).classList.contains("active")
//     ) {
//       document.querySelectorAll(".tabs-list .answer").forEach((ele) => {
//         if (ele.classList.contains("active")) {
//           ele.classList.remove("active");
//         }
//       });
//     } else {
//       document.querySelectorAll(".tabs-list .answer").forEach((ele) => {
//         if (ele.classList.contains("active")) {
//           ele.classList.remove("active");
//         }
//       });
//       document.querySelector(link.dataset.answer).classList.add("active");
//     }
//   });
// });