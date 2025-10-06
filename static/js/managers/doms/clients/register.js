import { ApiManager, DomManager } from "../../index.js";

export class ClientRegisterManager {
  constructor() {}

  static #NE = 'No encontrado';


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
      } catch (err) {
        this.#resetFields({nameField, clientTypeField, addressInput});
      } finally {
        this.#setButtonLoading(searchButton, false);
      }
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
   * Initialize the client registration form on DOM load
   */
  static initOnDomLoad() {
    ClientRegisterManager.#clearForm();
    const elements = ClientRegisterManager.#setupDomElements();
    ClientRegisterManager.#initSearchButtonListener(elements);
  }
}