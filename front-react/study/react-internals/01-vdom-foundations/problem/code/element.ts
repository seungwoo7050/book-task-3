import { VNode } from "./types";

/**
 * Wraps a primitive text value into a VNode with type "TEXT_ELEMENT".
 *
 * @param text - The string content for the text node.
 * @returns A VNode representing a text node.
 */
export function createTextElement(text: string): VNode {
  // TODO: Return a VNode with type "TEXT_ELEMENT",
  //       props.nodeValue set to `text`, and props.children as [].
  throw new Error("Not implemented");
}

/**
 * Creates a VNode — the Virtual DOM representation of a UI element.
 *
 * This function is the equivalent of `React.createElement` and is
 * what a JSX transpiler would call under the hood.
 *
 * @param type  - An HTML tag name (e.g., "div") or a function component.
 * @param props - A dictionary of attributes / event handlers, or null.
 * @param children - Zero or more child VNodes or primitive values.
 * @returns A VNode object.
 */
export function createElement(
  type: string,
  props: Record<string, any> | null,
  ...children: any[]
): VNode {
  // TODO: Build and return a VNode.
  //  - Merge `props` (handle null) with a `children` array.
  //  - Each child that is NOT an object must be wrapped with createTextElement.
  throw new Error("Not implemented");
}

