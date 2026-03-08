import type { VNode, VNodeProps } from "@front-react/vdom-foundations";

export type PatchType = "CREATE" | "REMOVE" | "REPLACE" | "UPDATE";
export type EffectTag = "PLACEMENT" | "UPDATE" | "DELETION";

export interface PropsPatch {
  set: Record<string, any>;
  remove: string[];
}

export interface Patch {
  type: PatchType;
  index?: number;
  oldNode?: VNode;
  newNode?: VNode;
  props?: PropsPatch;
  children?: Patch[];
}

export interface Fiber {
  type: string;
  props: VNodeProps;
  dom: HTMLElement | Text | null;
  parent: Fiber | null;
  child: Fiber | null;
  sibling: Fiber | null;
  alternate: Fiber | null;
  effectTag?: EffectTag;
}

export interface IdleDeadlineLike {
  timeRemaining(): number;
}

export type { VNode, VNodeProps };
