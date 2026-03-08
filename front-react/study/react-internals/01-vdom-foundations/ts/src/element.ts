import { VNode } from "./types";

export function createTextElement(text: string): VNode {
  return {
    type: "TEXT_ELEMENT",
    props: {
      nodeValue: text,
      children: [],
    },
  };
}

export function createElement(
  type: string,
  props: Record<string, any> | null,
  ...children: any[]
): VNode {
  return {
    type,
    props: {
      ...(props ?? {}),
      children: children.map((child) =>
        typeof child === "object" ? child : createTextElement(String(child)),
      ),
    },
  };
}

