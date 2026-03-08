export { createElement, createTextElement, createDom, updateDom } from "@front-react/vdom-foundations";
export { diff, diffChildren, diffProps } from "./diff";
export { performUnitOfWork, reconcileChildren } from "./fiber";
export { applyPatches } from "./patch";
export { flushSync, render, resetScheduler, workLoop } from "./scheduler";
export type {
  Fiber,
  IdleDeadlineLike,
  Patch,
  PatchType,
  PropsPatch,
  VNode,
  VNodeProps,
} from "./types";
