import "./styles.css";
import { mountBoard } from "./app";

const container = document.querySelector<HTMLElement>("#app");

if (container) {
  mountBoard(container);
}
