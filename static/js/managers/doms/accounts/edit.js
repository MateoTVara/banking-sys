import { DomManager } from "../../index.js";

export class EditAccountManager {
  constructor(){}

  static initOnDomLoad(){
    document.querySelector('main').classList.add('account-edit-form-body');
  }
}