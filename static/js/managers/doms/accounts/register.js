import { DomManager } from "../../DomManager.js";

export class AccountRegisterManager {
  constructor() {}

  static #initAccountTypeSelectListeners(elements) {
    elements.accountTypeSelect.addEventListener('change', () => {
      const selectedType = elements.accountTypeSelect.value;
      elements.currentFields.style.display = 'none';
      elements.termFields.style.display = 'none';
      if (selectedType === 'current') {
        elements.currentFields.style.display = 'grid';
      } else if (selectedType === 'term') {
        elements.termFields.style.display = 'grid';
      }
    });
  }

  static #initSearchInputListener(elements) {
    elements.searchInput.addEventListener('input', () => {
      const value = elements.searchInput.value.trim().toLowerCase();
      document.querySelectorAll('tbody tr').forEach(row => {
        const accountNumber = row.children[0]?.textContent.toLowerCase() || '';
        const clientName = row.children[1]?.textContent.toLowerCase() || '';
        if (accountNumber.includes(value) || clientName.includes(value)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  }

  static #initAddAccountBtnListener(elements) {
    elements.addAccountBtn.addEventListener('click', () => {
      elements.registerContainer.classList.add('active');
    });
  }

  static #initRegisterContainerListener(elements) {
    elements.registerContainer.addEventListener('click', (e) => {
      if (e.target === elements.registerContainer) {
        elements.registerContainer.classList.remove('active');
      }
    });
  }

  static #setupDomElements() {
    return DomManager.selectDomElements({
      accountTypeSelect: '#id_account_type',
      currentFields: '#current-account-fields',
      termFields: '#term-account-fields',
      searchInput: '.actions-bar input[type="text"]',
      addAccountBtn: '.actions-bar button',
      registerContainer: '.account-register-container',
    });
  }

  static initOnDomLoad() {
    document.querySelector('main')?.classList.add('account-register-body');
    const elements = this.#setupDomElements();
    this.#initAccountTypeSelectListeners(elements);
    this.#initSearchInputListener(elements);
    this.#initAddAccountBtnListener(elements);
    this.#initRegisterContainerListener(elements);
  }
}