import { ApiManager, DomManager } from "../../index.js";

export class ClientRegisterManager {
  constructor() {}

  static #NE = 'No encontrado';
  static #stagedRucDni = '';



  /**
   * Setup DOM elements for the client registration form
   * @return {Object} - An object containing references to the selected DOM elements
   */
  static #setupDomElements() {
    return DomManager.selectDomElements({
      formContainer: '.form-container',
      form: '#register-client-form',
      searchInput: '.searcher > input',
      searchButton: '#register-client-form button[type="button"]',
      rucDniInput: '#ruc-dni',
      nameField: '#client-name',
      clientTypeField: "#client-type",
      addressInput: "#client-address",
      addClientBtn: ".add-client-btn",
    });
  }



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
   * Set the loading state of the button
   * @param {HTMLButtonElement} button - The button element to update
   * @param {boolean} isLoading - Whether the button is in a loading state
   */
  static #setButtonLoading(button, isLoading) {
    button.disabled = isLoading;
    button.textContent = isLoading ? '...' : 'B';
  }



  /**
   * Fetch client data from the API based on the identifier
   * @param {string} identifier - The RUC or DNI identifier
   * @return {Promise<Object>} - The fetched client data
   */
  static async #fetchClientData(identifier) {
    const formData = new FormData();
    formData.append('identifier', identifier);
    return await ApiManager.fetchData('/api/fetch_identifier/', formData);
  }



  /**
   * Update form fields based on fetched data
   * @param {Object} data - The fetched client data
   * @param {string} identifier - The RUC or DNI identifier
   * @param {Object} fields - An object containing references to the form fields
   */
  static #updateFieldsFromData(data, identifier, fields) {
    if (typeof fields !== 'object' || fields === null) {
      throw new TypeError('fields must be a non-null object');
    }

    const config = {
      dni: {
        name: data.full_name || this.#NE,
        clientType: (identifier.length === 8 && data.full_name) ? 'Natural' : '',
        address: '',
        addressDisabled: false,
      },
      ruc: {
        name: data.razon_social || this.#NE,
        clientType: (identifier.length === 11 && data.razon_social) ? 'Jurídico' : '',
        address: data.direccion || '',
        addressDisabled: !!data.direccion,
      },
    }

    const settings = config[data.type] || {
      name: this.#NE,
      clientType: '',
      address: '',
      addressDisabled: false,
    }

    this.#applyFieldSettings(fields, settings);
  }



  /**
   * Reset form fields to default state
   * @param {Object} fields - An object containing references to the form fields
   * @param {string} nameValue - The default value for the name field
   */
  static #resetFields(fields, nameValue = this.#NE) {
    this.#applyFieldSettings(fields, {
      name: nameValue,
      clientType: '',
      address: '',
      addressDisabled: false,
    });
  }



  /**
   * Apply settings to form fields
   * @param {Object} fields - An object containing references to the form fields
   * @param {Object} settings - An object containing the settings to apply
   */
  static #applyFieldSettings(fields, settings) {
    const { nameField, clientTypeField, addressInput } = fields;
    nameField.textContent = settings.name;
    clientTypeField.textContent = settings.clientType;
    addressInput.value = settings.address;
    addressInput.disabled = settings.addressDisabled; 
  }



  /**
   * Initialize the search button click event listener
   * @param {Object} elements - An object containing references to the DOM elements
   */
  static #initSearchButtonListener(elements) {
    const {searchButton, rucDniInput, nameField, clientTypeField, addressInput} = elements;

    searchButton.addEventListener('click', async () => {
      if (rucDniInput.value.trim().length !== 8 && rucDniInput.value.trim().length !== 11) {
        rucDniInput.setCustomValidity('Ingrese un RUC o DNI válido');
        rucDniInput.reportValidity();
        return;
      }

      rucDniInput.setCustomValidity('');

      const identifier = rucDniInput.value.trim();
      if (!identifier) return;

      this.#setButtonLoading(searchButton, true);

      try {
        const data = await this.#fetchClientData(identifier);
        this.#updateFieldsFromData(data, identifier, {nameField, clientTypeField, addressInput});
        this.#stagedRucDni = identifier;
      } catch (err) {
        this.#resetFields({nameField, clientTypeField, addressInput});
        this.#stagedRucDni = '';
      } finally {
        this.#setButtonLoading(searchButton, false);
      }
    });
  }





  /**
   * Extract form data for client registration
   * @returns {Object} - Formatted form data ready for submission
   */
  static #extractFormData() {
    const rucDni = ClientRegisterManager.#stagedRucDni;
    const name = document.getElementById('client-name').textContent.trim();
    const clientType = document.getElementById('client-type').textContent.trim();
    const address = document.getElementById('client-address').value.trim();
    const phone = document.getElementById('client-phone').value.trim();
    const email = document.getElementById('client-email').value.trim();

    const isDni = rucDni.length === 8;
    const isRuc = rucDni.length === 11;

    let client_type = '';
    if (clientType.toLowerCase().includes('natural')) {
      client_type = 'natural';
    } else if (clientType.toLowerCase().includes('jurídico')) {
      client_type = 'legal';
    }

    return {
      client_type,
      dni: isDni ? rucDni : '',
      ruc: isRuc ? rucDni : '',
      name,
      address,
      phone,
      email
    };
  }



  /**
   * Build FormData object from extracted data
   * @param {Object} data - The extracted form data
   * @returns {FormData} - FormData object ready for API submission
   */
  static #buildFormData(data) {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value);
    });
    return formData;
  }



  /**
   * Reset form after successful registration
   * @param {HTMLFormElement} form - The form element to reset
   */
  static #resetFormAfterSubmit(form) {
    form.reset();
    document.getElementById('client-name').textContent = '';
    document.getElementById('client-type').textContent = '';
    ClientRegisterManager.#stagedRucDni = '';
  }


  /**
   * Initialize the form submission event listener
   * @param {Object} elements - An object containing references to the DOM elements
   */
  static #initFormListener(elements) {
    elements.form.addEventListener('submit', async (e) => {

      e.preventDefault();

      const extractedData = ClientRegisterManager.#extractFormData();
      const formData = ClientRegisterManager.#buildFormData(extractedData);

      try {
        const result = await ApiManager.fetchData('/api/register_client/', formData);
        
        if (result.success) {
          alert(`Cliente registrado con código: ${result.code}`);
          ClientRegisterManager.#resetFormAfterSubmit(elements.form);
          elements.formContainer.classList.remove('active');
          location.reload();
        } else if (result.error) {
          alert(result.error);
        } else {
          alert('Error al registrar cliente');
        }
      } catch (err) {
        alert('Error al registrar cliente');
      }
    });
  }



  static #initAddClientBtnListener(elements) {
    elements.addClientBtn.addEventListener('click', () => {
      elements.formContainer.classList.add('active');
    });
  }



  static #initFormContainerListener(elements) {
    elements.formContainer.addEventListener('click', (e) => {
      if (e.target === elements.formContainer) {
        elements.formContainer.classList.remove('active');
      }
    });
  }



  static #initSearchInputListener(elements) {
    elements.searchInput.addEventListener('input', () => {
      document.querySelectorAll('.client-row').forEach(ele => {
        const idCell = ele.querySelector('.client-id');
        const nameCell = ele.querySelector('.client-name');
        if (idCell.textContent.includes(elements.searchInput.value) ||
            nameCell.textContent.includes(elements.searchInput.value)) {
          ele.style.display = ''; 
        } else {
          ele.style.display = 'none';
        }
      });
    });
  }



  /**
   * Initialize the client registration form on DOM load
   */
  static initOnDomLoad() {
    this.#clearForm();
    const elements = this.#setupDomElements();
    this.#initSearchButtonListener(elements);
    this.#initFormListener(elements);
    this.#initAddClientBtnListener(elements);
    this.#initFormContainerListener(elements);
    this.#initSearchInputListener(elements);
  }
}