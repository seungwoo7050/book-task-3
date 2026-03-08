import {
  applyPatches,
  createElement as baseCreateElement,
  createTextElement,
  diff,
  resetScheduler,
  type VNode,
} from "@front-react/render-pipeline";

import type {
  DelegatedEvent,
  DependencyList,
  EffectCallback,
  EffectHookSlot,
  EventHandler,
  HookContext,
  HookSlot,
  PendingEffect,
  RuntimeNode,
  RuntimeRoot,
  SetStateAction,
  StateHookSlot,
  StateSetter,
} from "./types";

let currentRoot: RuntimeRoot | null = null;
let currentHookContext: HookContext | null = null;

function normalizeChild(child: unknown): VNode | null {
  if (child === null || child === undefined || child === false || child === true) {
    return null;
  }

  if (typeof child === "object" && child !== null && "type" in child && "props" in child) {
    return child as VNode;
  }

  return createTextElement(String(child));
}

function splitProps(
  props: Record<string, any>,
): { domProps: Record<string, any>; handlers: Record<string, EventHandler> } {
  const domProps: Record<string, any> = {};
  const handlers: Record<string, EventHandler> = {};

  Object.entries(props).forEach(([key, value]) => {
    if (key === "children") {
      return;
    }

    if (key.startsWith("on") && typeof value === "function") {
      handlers[key.toLowerCase().slice(2)] = value as EventHandler;
      return;
    }

    domProps[key] = value;
  });

  return { domProps, handlers };
}

function createRuntimeNode(
  type: string,
  props: Record<string, any>,
  path: string,
  handlers: Record<string, EventHandler>,
  children: RuntimeNode[],
): RuntimeNode {
  return {
    type,
    path,
    handlers,
    props: {
      ...props,
      children,
    },
  };
}

function toVNode(node: RuntimeNode): VNode {
  return {
    type: node.type,
    props: {
      ...node.props,
      children: node.props.children.map((child) => toVNode(child)),
    },
  };
}

function depsChanged(prev: DependencyList, next: DependencyList): boolean {
  if (!prev || !next) {
    return true;
  }

  if (prev.length !== next.length) {
    return true;
  }

  return prev.some((value, index) => !Object.is(value, next[index]));
}

function getDisplayName(type: string | Function): string {
  if (typeof type === "string") {
    return type;
  }

  return type.name || "AnonymousComponent";
}

function scheduleRender(root: RuntimeRoot): void {
  root.needsRender = true;

  if (root.isRendering) {
    return;
  }

  performRender(root);
}

function collectUnmounts(root: RuntimeRoot): void {
  Array.from(root.instances.entries()).forEach(([path, slots]) => {
    if (root.visitedInstances.has(path)) {
      return;
    }

    slots.forEach((slot) => {
      if (slot.kind === "effect" && typeof slot.cleanup === "function") {
        root.pendingUnmounts.push(slot.cleanup);
      }
    });

    root.instances.delete(path);
  });
}

function runEffects(root: RuntimeRoot): void {
  root.pendingUnmounts.forEach((cleanup) => cleanup());
  root.pendingUnmounts = [];

  root.pendingEffects.forEach((effect) => {
    if (typeof effect.previousCleanup === "function") {
      effect.previousCleanup();
    }

    const slots = root.instances.get(effect.path);
    const slot = slots?.[effect.index];

    if (!slot || slot.kind !== "effect") {
      return;
    }

    slot.cleanup = effect.create();
  });

  root.pendingEffects = [];
}

function syncDomMeta(root: RuntimeRoot, domNode: Node, runtimeNode: RuntimeNode): void {
  root.domToMeta.set(domNode, {
    path: runtimeNode.path,
    handlers: runtimeNode.handlers,
  });

  const domChildren = Array.from(domNode.childNodes);
  runtimeNode.props.children.forEach((child, index) => {
    const domChild = domChildren[index];
    if (domChild) {
      syncDomMeta(root, domChild, child);
    }
  });
}

function createDelegatedEvent(nativeEvent: Event, currentTarget: EventTarget | null): DelegatedEvent {
  let propagationStopped = false;

  return {
    nativeEvent,
    target: nativeEvent.target,
    currentTarget,
    get defaultPrevented() {
      return nativeEvent.defaultPrevented;
    },
    get propagationStopped() {
      return propagationStopped;
    },
    preventDefault() {
      nativeEvent.preventDefault();
    },
    stopPropagation() {
      propagationStopped = true;
      nativeEvent.stopPropagation();
    },
  };
}

function dispatchDelegatedEvent(root: RuntimeRoot, eventType: string, nativeEvent: Event): void {
  let currentNode = nativeEvent.target as Node | null;

  while (currentNode) {
    const meta = root.domToMeta.get(currentNode);
    const handler = meta?.handlers[eventType];

    if (handler) {
      const event = createDelegatedEvent(nativeEvent, currentNode);
      handler(event);
      if (event.propagationStopped) {
        return;
      }
    }

    if (currentNode === root.container) {
      return;
    }

    currentNode = currentNode.parentNode;
  }
}

function syncEventListeners(root: RuntimeRoot): void {
  Array.from(root.listeners.entries()).forEach(([eventType, listener]) => {
    if (root.requestedEvents.has(eventType)) {
      return;
    }

    root.container.removeEventListener(eventType, listener);
    root.listeners.delete(eventType);
  });

  root.requestedEvents.forEach((eventType) => {
    if (root.listeners.has(eventType)) {
      return;
    }

    const listener: EventListener = (event) => dispatchDelegatedEvent(root, eventType, event);
    root.container.addEventListener(eventType, listener);
    root.listeners.set(eventType, listener);
  });
}

function commitRoot(root: RuntimeRoot, nextTree: RuntimeNode | null): void {
  const nextVNode = nextTree ? toVNode(nextTree) : null;

  if (!root.hostVNode && nextVNode) {
    applyPatches(root.container, [{ type: "CREATE", newNode: nextVNode, index: 0 }]);
  } else if (root.hostVNode && !nextVNode) {
    applyPatches(root.container, [{ type: "REMOVE", oldNode: root.hostVNode, index: 0 }]);
  } else if (root.hostVNode && nextVNode) {
    const patch = diff(root.hostVNode, nextVNode);
    if (patch) {
      patch.index = 0;
      applyPatches(root.container, [patch]);
    }
  }

  root.hostTree = nextTree;
  root.hostVNode = nextVNode;
  root.domToMeta = new WeakMap();

  if (nextTree && root.container.firstChild) {
    syncDomMeta(root, root.container.firstChild, nextTree);
  }

  syncEventListeners(root);
  runEffects(root);
}

function resolveFunctionComponent(root: RuntimeRoot, vnode: VNode, path: string): RuntimeNode | null {
  const previousSlots = root.instances.get(path) ?? [];
  const slots = previousSlots.slice();
  const previousContext = currentHookContext;

  root.visitedInstances.add(path);
  currentHookContext = {
    root,
    path,
    slots,
    hookIndex: 0,
    displayName: getDisplayName(vnode.type),
  };

  const output = (vnode.type as Function)(vnode.props);
  const usedHookCount = currentHookContext.hookIndex;
  currentHookContext = previousContext;

  if (previousSlots.length > 0 && previousSlots.length !== usedHookCount) {
    throw new Error(
      `Hook order changed for ${getDisplayName(vnode.type)}. ` +
        `Expected ${previousSlots.length} hooks but rendered ${usedHookCount}.`,
    );
  }

  slots.length = usedHookCount;
  root.instances.set(path, slots);

  return resolveNode(root, normalizeChild(output), path);
}

function resolveHostNode(root: RuntimeRoot, vnode: VNode, path: string): RuntimeNode {
  const { domProps, handlers } = splitProps(vnode.props);
  const children = (vnode.props.children ?? [])
    .map((child, index) => resolveNode(root, normalizeChild(child), `${path}.${index}`))
    .filter((child): child is RuntimeNode => child !== null);

  Object.keys(handlers).forEach((eventType) => {
    root.requestedEvents.add(eventType);
  });

  if (vnode.type === "TEXT_ELEMENT") {
    return createRuntimeNode("TEXT_ELEMENT", { nodeValue: vnode.props.nodeValue }, path, {}, []);
  }

  return createRuntimeNode(vnode.type as string, domProps, path, handlers, children);
}

function resolveNode(root: RuntimeRoot, vnode: VNode | null, path: string): RuntimeNode | null {
  if (!vnode) {
    return null;
  }

  if (typeof vnode.type === "function") {
    return resolveFunctionComponent(root, vnode, path);
  }

  return resolveHostNode(root, vnode, path);
}

function createRootState(element: VNode, container: HTMLElement): RuntimeRoot {
  return {
    container,
    element,
    hostTree: null,
    hostVNode: null,
    instances: new Map(),
    pendingEffects: [],
    pendingUnmounts: [],
    visitedInstances: new Set(),
    requestedEvents: new Set(),
    domToMeta: new WeakMap(),
    listeners: new Map(),
    isRendering: false,
    needsRender: false,
  };
}

function cleanupRoot(root: RuntimeRoot): void {
  root.listeners.forEach((listener, eventType) => {
    root.container.removeEventListener(eventType, listener);
  });

  root.instances.forEach((slots) => {
    slots.forEach((slot) => {
      if (slot.kind === "effect" && typeof slot.cleanup === "function") {
        slot.cleanup();
      }
    });
  });
}

function performRender(root: RuntimeRoot): void {
  if (!root.needsRender) {
    return;
  }

  if (root.isRendering) {
    return;
  }

  root.isRendering = true;

  try {
    while (root.needsRender) {
      root.needsRender = false;
      root.pendingEffects = [];
      root.pendingUnmounts = [];
      root.visitedInstances = new Set();
      root.requestedEvents = new Set();

      const nextTree = resolveNode(root, root.element, "0");
      collectUnmounts(root);
      commitRoot(root, nextTree);
    }
  } finally {
    root.isRendering = false;
  }
}

export function createElement(
  type: string | Function,
  props: Record<string, any> | null,
  ...children: any[]
): VNode {
  return baseCreateElement(type as any, props, ...children);
}

export function render(element: VNode, container: HTMLElement): void {
  if (currentRoot && currentRoot.container !== container) {
    cleanupRoot(currentRoot);
    currentRoot = null;
    resetScheduler();
  }

  currentRoot ??= createRootState(element, container);
  currentRoot.element = element;
  currentRoot.container = container;
  scheduleRender(currentRoot);
}

export function flushSync(): void {
  if (!currentRoot) {
    return;
  }

  performRender(currentRoot);
}

export function resetRuntime(): void {
  if (currentRoot) {
    cleanupRoot(currentRoot);
  }

  currentRoot = null;
  currentHookContext = null;
  resetScheduler();
}

export function useState<T>(initialValue: T): [T, StateSetter<T>] {
  if (!currentHookContext) {
    throw new Error("useState must be called during component render.");
  }

  const { root, path, slots } = currentHookContext;
  const hookIndex = currentHookContext.hookIndex;
  const existingSlot = slots[hookIndex] as StateHookSlot<T> | undefined;

  if (existingSlot && existingSlot.kind !== "state") {
    throw new Error(`Hook kind mismatch at ${path}:${hookIndex}.`);
  }

  if (!existingSlot) {
    const slot: StateHookSlot<T> = {
      kind: "state",
      value: initialValue,
      setState: ((action: SetStateAction<T>) => {
        const nextValue =
          typeof action === "function"
            ? (action as (value: T) => T)(slot.value)
            : action;

        if (Object.is(nextValue, slot.value)) {
          return;
        }

        slot.value = nextValue;
        scheduleRender(root);
      }) as StateSetter<T>,
    };

    slots[hookIndex] = slot;
  }

  const slot = slots[hookIndex] as StateHookSlot<T>;
  currentHookContext.hookIndex += 1;
  return [slot.value, slot.setState];
}

export function useEffect(callback: EffectCallback, deps?: DependencyList): void {
  if (!currentHookContext) {
    throw new Error("useEffect must be called during component render.");
  }

  const { root, path, slots } = currentHookContext;
  const hookIndex = currentHookContext.hookIndex;
  const previousSlot = slots[hookIndex] as EffectHookSlot | undefined;

  if (previousSlot && previousSlot.kind !== "effect") {
    throw new Error(`Hook kind mismatch at ${path}:${hookIndex}.`);
  }

  const nextSlot: EffectHookSlot = {
    kind: "effect",
    deps,
    cleanup: previousSlot?.cleanup,
  };

  slots[hookIndex] = nextSlot;
  currentHookContext.hookIndex += 1;

  if (!previousSlot || depsChanged(previousSlot.deps, deps)) {
    root.pendingEffects.push({
      path,
      index: hookIndex,
      create: callback,
      previousCleanup: previousSlot?.cleanup,
    } satisfies PendingEffect);
  }
}
