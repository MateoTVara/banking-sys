import { DomManager } from './managers/index.js';

// const navToggle = document.querySelector('.nav-toggle');
// const nav = document.querySelector('nav');

// navToggle.addEventListener('click', () => {
//   document.body.classList.toggle('active-nav');
//   nav.classList.toggle('active');
// });

// nav.addEventListener("click", (e) => {
//   if (e.target.tagName === "P") {
//     const navItem = e.target.parentElement.querySelector(".nav-item");
//     if (navItem) {
//       navItem.classList.toggle("active");
//     }
//   }
// });

DomManager.initEventListener();

window.addEventListener('DOMContentLoaded', () => {
  if (window.location.pathname === '/clients/register/') {
    document.querySelector('main').classList.add('cliente-register-body');
    document.querySelectorAll("#register-client-form input").forEach(input => {
      input.value = '';
    });

    const bButton = document.querySelector('#register-client-form button[type="button"]');
    const rucDniInput = document.querySelector('#ruc-dni');
    const nameField = document.querySelector('#client-name');
    const clientTypeField = document.querySelector("#client-type");
    const addressInput = document.querySelector("#client-address");

    bButton.addEventListener('click', async () => {
      const identifier = rucDniInput.value.trim();
      if (!identifier) return;

      bButton.disabled = true;
      bButton.textContent = '...';

      try {
        const formData = new FormData();
        formData.append('identifier', identifier);

        const response = await fetch('/api/fetch_identifier/', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();

        if (data.type === "dni") {
          nameField.textContent = data.full_name ? data.full_name : 'No encontrado';
          clientTypeField.textContent = (identifier.length === 8 && data.full_name) ? 'Natural' : '';
          addressInput.value = '';
          addressInput.disabled = false;
        } else if (data.type === "ruc") {
          nameField.textContent = data.razon_social ? data.razon_social : 'No encontrado';
          clientTypeField.textContent = (identifier.length === 11 && data.razon_social) ? 'Jurídico' : '';
          addressInput.value = data.direccion ? data.direccion : '';
          addressInput.disabled = !!data.direccion;
        } else {
          nameField.textContent = 'No encontrado';
          clientTypeField.textContent = '';
          addressInput.value = '';
          addressInput.disabled = false;
        }
      } catch (err) {
        nameField.textContent = 'Error';
        clientTypeField.textContent = '';
        addressInput.value = '';
        addressInput.disabled = false;
      } finally {
        bButton.disabled = false;
        bButton.textContent = 'B';
      }
    });
  }
});