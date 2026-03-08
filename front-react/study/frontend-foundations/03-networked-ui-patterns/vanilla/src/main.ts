import "./styles.css";
import { mountDirectoryExplorer } from "./app";

const container = document.querySelector<HTMLElement>("#app");

if (container) {
  mountDirectoryExplorer(container);
}
