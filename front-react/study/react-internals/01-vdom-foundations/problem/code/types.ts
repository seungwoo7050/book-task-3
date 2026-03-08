/**
 * VNode type definitions for the Virtual DOM.
 *
 * These types describe the shape of the in-memory tree that mirrors
 * the real DOM.  Every node in this tree is a plain JavaScript object.
 */

/** The `type` field of a VNode: either an HTML tag name or a function component. */
export type VNodeType = string | Function;

/** Props carried by every VNode. `children` is always present and is an array. */
export interface VNodeProps {
  [key: string]: any;
  children: VNode[];
}

/** A single node in the Virtual DOM tree. */
export interface VNode {
  type: VNodeType;
  props: VNodeProps;
}

