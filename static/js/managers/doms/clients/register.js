import { DomManager } from "../../index.js";

export class ClientRegisterManager {
  constructor() {}



  /** 
   * Clear form inputs and set initial state
   */
  static #clearForm() {
    document.querySelector('main').classList.add('cliente-register-body');
    document.querySelectorAll("#register-client-form input").forEach(input => {
      input.value = '';
    });
  }



  /**
   * Setup DOM elements for the client registration form
   * @return {Object} - An object containing references to the selected DOM elements
   */
  static #setupDomElements() {
    return DomManager.selectDomElements({
      searchButton: '#register-client-form button[type="button"]',
      rucDniInput: '#ruc-dni',
      nameField: '#client-name',
      clientTypeField: "#client-type",
      addressInput: "#client-address",
    });
  }



  static initOnDomLoad(){
    ClientRegisterManager.#clearForm();
    const elements = ClientRegisterManager.#setupDomElements();

    const searchButton = elements.searchButton;
    const rucDniInput = elements.rucDniInput;
    const nameField = elements.nameField;
    const clientTypeField = elements.clientTypeField;
    const addressInput = elements.addressInput;

    searchButton.addEventListener('click', async () => {
      const identifier = rucDniInput.value.trim();
      if (!identifier) return;

      searchButton.disabled = true;
      searchButton.textContent = '...';

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
        searchButton.disabled = false;
        searchButton.textContent = 'B';
      }
    });
  }
}