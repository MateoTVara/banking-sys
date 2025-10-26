import { AccountManager } from "./doms/accounts/index.js";
import { ClientManager } from "./doms/clients/index.js";
import { JudicialHoldManager } from "./doms/judicial_holds/index.js";

export class DomManager {
  constructor() {}



  static body = DomManager.selectDomElements({
    nav: "nav",
    navToggle: ".nav-toggle",
  });



  /**
   * Selects multiple DOM elements based on the provided CSS selectors.
   * @param {object} selectors - An object where keys are names and values are CSS selector strings.
   * @param {HTMLElement} [parentEle=document] - The parent element to scope the query (default is the entire document).
   * @returns {object} An object containing the selected DOM elements.
   * @throws {TypeError} If selectors is not an object or if any selector is not a string.
   */
  static selectDomElements(selectors = {}, parentEle = document) {
    if (typeof selectors !== "object") {
      throw new TypeError("selector must be an object");
    }

    const elements = {};

    Object.entries(selectors).forEach(([key, value]) => {
      if (typeof value !== "string") {
        throw new TypeError("selector must be a string");
      }
      elements[key] = parentEle.querySelector(value);
    });

    return elements
  }



  /**
   * Initializes event listeners for dom elements.
   */
  static initEventListener() {
    this.body.navToggle.addEventListener("click", () => {
      document.body.classList.toggle("active-nav");
      this.body.nav.classList.toggle("active");
    }); 



    this.body.nav.addEventListener("click", (e) => {
      if (e.target.tagName === "P") {
        const navItem = e.target.parentElement.querySelector(".nav-item");
        if (navItem) {
          navItem.classList.toggle("active");
        }
      }
    });

    window.addEventListener('DOMContentLoaded', () => {
      if (window.location.pathname === '/management/clients/register/') {
        ClientManager.initRegisterMngr();
      } else if (window.location.pathname === '/management/accounts/register/') {
        AccountManager.initRegisterAccountManager();
      } else if (window.location.pathname === '/management/judicial_holds/register/') {
        JudicialHoldManager.initRegisterMngr();
      } else if (window.location.pathname === '/management/judicial_holds/register_form/') {
        JudicialHoldManager.initRegisterFormMngr();
      } else if (window.location.pathname === '/management/accounts/edit/') {
        AccountManager.initEditAccountManager();
      }
    });
  }
}