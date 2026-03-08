import { VNode } from "./types";

/**
 * Creates a real DOM node from a VNode.
 *
 * @param vnode - The virtual node to materialise.
 * @returns An HTMLElement or Text node.
 */
export function createDom(vnode: VNode): HTMLElement | Text {
  // TODO:
  //  1. If vnode.type is "TEXT_ELEMENT", create a Text node.
  //  2. Otherwise, create an HTMLElement with document.createElement.
  //  3. Apply properties from vnode.props using updateDom.
  //  4. Return the DOM node.
  throw new Error("Not implemented");
}

/**
 * Applies a diff of props to an existing DOM node.
 *
 * Handles three categories of props:
 *   - Event listeners (keys starting with "on")
 *   - The special "children" key (skipped)
 *   - All other DOM properties
 *
 * @param dom       - The real DOM node to update.
 * @param prevProps - The previous set of props.
 * @param nextProps - The next set of props.
 */
export function updateDom(
  dom: HTMLElement | Text,
  prevProps: Record<string, any>,
  nextProps: Record<string, any>,
): void {
  // TODO:
  //  1. Remove old/changed event listeners.
  //  2. Remove old properties (set to "").
  //  3. Set new/changed properties.
  //  4. Add new/changed event listeners.
  throw new Error("Not implemented");
}

/**
 * Recursively renders a VDOM tree into a real DOM container.
 *
 * @param element   - The root VNode to render.
 * @param container - The DOM node to append into.
 */
export function render(element: VNode, container: HTMLElement | Text): void {
  // TODO:
  //  1. Create a real DOM node for `element` with createDom.
  //  2. For each child in element.props.children, call render recursively.
  //  3. Append the DOM node to `container`.
  throw new Error("Not implemented");
}

