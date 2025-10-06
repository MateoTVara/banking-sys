const navToggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('nav');

navToggle.addEventListener('click', () => {
  document.body.classList.toggle('active-nav');
  nav.classList.toggle('active');
});

nav.addEventListener("click", (e) => {
  if (e.target.tagName === "P") {
    const navItem = e.target.parentElement.querySelector(".nav-item");
    if (navItem) {
      navItem.classList.toggle("active");
    }
  }
});

window.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname === '/clients/register/') {
    document.querySelector('main').classList.add('cliente-register-body');
  }
});