import { DomManager } from "../../index.js";

export class JudicialHoldRegisterManager {
  constructor() {}

  static #setupDomElements() {
    return DomManager.selectDomElements({
      section: '#judicial-hold-register-section',
      inputSearch: 'input',
    });
  }

  static #initFormListeners(elements) {
    elements.section.addEventListener('click', (e) => {
      const clientInfo = e.target.closest('.client-info');
      if (clientInfo && elements.section.contains(clientInfo)) {
        const card = clientInfo.parentElement;
        const accountList = card.querySelector('.account-list');
        if (accountList) {
          accountList.classList.toggle('active');
        }
      }
    });
  }

  static #initInputSearchListeners(elements) {
    elements.inputSearch.addEventListener('input', (e) => {
      elements.section.querySelectorAll('.client-info').forEach(clientInfo => {
        const clientName = clientInfo.textContent.toLowerCase();
        const searchTerm = e.target.value.toLowerCase();
        clientInfo.parentElement.style.display = clientName.includes(searchTerm) ? '' : 'none';
      });
    });
  }

  static initOnDomLoad(){
    document.querySelector('main').classList.add('judicial-hold-register-body');
    const elements = this.#setupDomElements();
    this.#initFormListeners(elements);
    this.#initInputSearchListeners(elements);
  }

}