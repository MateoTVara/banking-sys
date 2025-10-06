import { ClientRegisterManager } from "./register.js";

export class ClientManager {
  constructor() {}

  static initRegisterMngr() {
    ClientRegisterManager.initOnDomLoad();
  }
}