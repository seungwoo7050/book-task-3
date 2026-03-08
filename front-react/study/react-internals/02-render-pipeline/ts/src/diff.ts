import type { Patch, PropsPatch, VNode } from "./types";

export function diffProps(
  oldProps: Record<string, any>,
  newProps: Record<string, any>,
): PropsPatch {
  const set: Record<string, any> = {};
  const remove: string[] = [];

  Object.keys(newProps).forEach((key) => {
    if (key === "children") {
      return;
    }

    if (oldProps[key] !== newProps[key]) {
      set[key] = newProps[key];
    }
  });

  Object.keys(oldProps).forEach((key) => {
    if (key === "children") {
      return;
    }

    if (!(key in newProps)) {
      remove.push(key);
    }
  });

  return { set, remove };
}

function isEmptyPropsPatch(patch: PropsPatch): boolean {
  return Object.keys(patch.set).length === 0 && patch.remove.length === 0;
}

function diffChildrenByIndex(oldChildren: VNode[], newChildren: VNode[]): Patch[] {
  const max = Math.max(oldChildren.length, newChildren.length);
  const patches: Patch[] = [];

  for (let index = 0; index < max; index += 1) {
    const patch = diff(oldChildren[index], newChildren[index]);

    if (patch) {
      patch.index = index;
      patches.push(patch);
    }
  }

  return patches;
}

function diffChildrenByKey(oldChildren: VNode[], newChildren: VNode[]): Patch[] {
  const oldMap = new Map<string, { node: VNode; index: number }>();
  const patches: Patch[] = [];
  const visitedKeys = new Set<string>();

  oldChildren.forEach((child, index) => {
    const key = child.props.key;
    if (typeof key === "string") {
      oldMap.set(key, { node: child, index });
    }
  });

  newChildren.forEach((child, index) => {
    const key = child.props.key;
    const oldMatch = typeof key === "string" ? oldMap.get(key) : undefined;

    if (typeof key === "string") {
      visitedKeys.add(key);
    }

    if (!oldMatch) {
      patches.push({
        type: "CREATE",
        newNode: child,
        index,
      });
      return;
    }

    const patch = diff(oldMatch.node, child);
    if (patch) {
      patch.index = index;
      patches.push(patch);
    }
  });

  oldChildren.forEach((child, index) => {
    const key = child.props.key;
    if (typeof key === "string" && !visitedKeys.has(key)) {
      patches.push({
        type: "REMOVE",
        oldNode: child,
        index,
      });
    }
  });

  return patches;
}

export function diffChildren(oldChildren: VNode[], newChildren: VNode[]): Patch[] {
  const keyed = [...oldChildren, ...newChildren].some(
    (child) => typeof child?.props?.key === "string",
  );

  if (keyed) {
    return diffChildrenByKey(oldChildren, newChildren);
  }

  return diffChildrenByIndex(oldChildren, newChildren);
}

export function diff(
  oldNode: VNode | undefined,
  newNode: VNode | undefined,
): Patch | undefined {
  if (!oldNode && newNode) {
    return { type: "CREATE", newNode };
  }

  if (oldNode && !newNode) {
    return { type: "REMOVE", oldNode };
  }

  if (!oldNode || !newNode) {
    return undefined;
  }

  if (oldNode.type !== newNode.type) {
    return {
      type: "REPLACE",
      oldNode,
      newNode,
    };
  }

  const props = diffProps(oldNode.props, newNode.props);
  const children = diffChildren(oldNode.props.children, newNode.props.children);

  if (isEmptyPropsPatch(props) && children.length === 0) {
    return undefined;
  }

  return {
    type: "UPDATE",
    oldNode,
    newNode,
    props,
    children,
  };
}
