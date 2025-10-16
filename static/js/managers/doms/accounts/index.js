import { EditAccountManager } from "./edit.js";
import { AccountRegisterManager } from "./register.js";

export class AccountManager {
  constructor() {}

  static initEditAccountManager() {
    EditAccountManager.initOnDomLoad();
  }
  
  static initRegisterAccountManager() {
    AccountRegisterManager.initOnDomLoad();
  }
}