import type { VNode } from "@front-react/render-pipeline";

export type SetStateAction<T> = T | ((value: T) => T);
export type StateSetter<T> = (action: SetStateAction<T>) => void;
export type EffectCallback = () => void | (() => void);
export type DependencyList = unknown[] | undefined;
export type EventHandler = (event: DelegatedEvent) => void;

export interface DelegatedEvent {
  nativeEvent: Event;
  target: EventTarget | null;
  currentTarget: EventTarget | null;
  defaultPrevented: boolean;
  propagationStopped: boolean;
  preventDefault(): void;
  stopPropagation(): void;
}

export interface RuntimeNode {
  type: string;
  props: Record<string, any> & {
    children: RuntimeNode[];
  };
  path: string;
  handlers: Record<string, EventHandler>;
}

export interface RuntimeNodeMeta {
  path: string;
  handlers: Record<string, EventHandler>;
}

export interface StateHookSlot<T = any> {
  kind: "state";
  value: T;
  setState: StateSetter<T>;
}

export interface EffectHookSlot {
  kind: "effect";
  deps: DependencyList;
  cleanup?: (() => void) | void;
}

export type HookSlot = StateHookSlot<any> | EffectHookSlot;

export interface PendingEffect {
  path: string;
  index: number;
  create: EffectCallback;
  previousCleanup?: (() => void) | void;
}

export interface RuntimeRoot {
  container: HTMLElement;
  element: VNode;
  hostTree: RuntimeNode | null;
  hostVNode: VNode | null;
  instances: Map<string, HookSlot[]>;
  pendingEffects: PendingEffect[];
  pendingUnmounts: Array<() => void>;
  visitedInstances: Set<string>;
  requestedEvents: Set<string>;
  domToMeta: WeakMap<Node, RuntimeNodeMeta>;
  listeners: Map<string, EventListener>;
  isRendering: boolean;
  needsRender: boolean;
}

export interface HookContext {
  root: RuntimeRoot;
  path: string;
  slots: HookSlot[];
  hookIndex: number;
  displayName: string;
}
