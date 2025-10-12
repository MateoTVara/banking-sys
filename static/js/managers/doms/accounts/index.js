import { EditAccountManager } from "./edit.js";

export class AccountManager {
  constructor() {}

  static initEditAccountManager() {
    EditAccountManager.initOnDomLoad();
  }
}