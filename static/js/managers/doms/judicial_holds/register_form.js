import { DomManager } from "../../index.js";

export class JudicialHoldManagerRegisterFormManager {
  constructor() {}

  static #setupDomElements() {
    return DomManager.selectDomElements({
      holdTypeSelect: '#hold_type',
      amountGroup: '#amount-group',
      holdAmount: '#hold_amount',
    });
  }

  static #initHoldTypeSelectListeners(elements) {
    elements.holdTypeSelect.addEventListener('change', () => {
      if (elements.holdTypeSelect.value === 'partial') {
        elements.amountGroup.style.display = '';
        elements.holdAmount.required = true;
      } else {
        elements.amountGroup.style.display = 'none';
        elements.holdAmount.required = false;
        elements.holdAmount.value = '';
      }
    });
  }

  static initOnDomLoad(){
    document.querySelector('main').classList.add('judicial-hold-register-form-body');
    const elements = this.#setupDomElements();
    this.#initHoldTypeSelectListeners(elements);
    elements.holdTypeSelect.dispatchEvent(new Event('change'));
  }
}