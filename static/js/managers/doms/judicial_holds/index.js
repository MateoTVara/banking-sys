import { JudicialHoldRegisterManager } from "./register.js";

export class JudicialHoldManager {
  constructor() {}

  static initRegisterMngr() {
    JudicialHoldRegisterManager.initOnDomLoad();
  }
}