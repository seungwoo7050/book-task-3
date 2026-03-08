import "./styles.css";
import { mountSettingsShell } from "./app";

const container = document.querySelector<HTMLElement>("#app");

if (container) {
  mountSettingsShell(container);
}
