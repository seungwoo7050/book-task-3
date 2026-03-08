import "./styles.css";

import { mountRuntimeDemo } from "./app";

const container = document.querySelector<HTMLElement>("#app");

if (!container) {
  throw new Error("Runtime demo root container not found.");
}

mountRuntimeDemo(container);
