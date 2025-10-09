import { JudicialHoldRegisterManager } from "./register.js";
import { JudicialHoldManagerRegisterFormManager } from "./register_form.js";

export class JudicialHoldManager {
  constructor() {}

  static initRegisterMngr() {
    JudicialHoldRegisterManager.initOnDomLoad();
  }

  static initRegisterFormMngr() {
    JudicialHoldManagerRegisterFormManager.initOnDomLoad();
  }
}