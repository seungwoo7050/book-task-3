import { createDom, render as renderVNode, updateDom } from "@front-react/vdom-foundations";

import type { Patch } from "./types";

function createDomTree(patch: Patch): HTMLElement | Text | null {
  if (!patch.newNode) {
    return null;
  }

  const dom = createDom(patch.newNode);
  patch.newNode.props.children.forEach((child) => {
    renderVNode(child, dom);
  });

  return dom;
}

function applyPatchAt(parent: HTMLElement | Text, patch: Patch, index: number): void {
  const child = parent.childNodes[index];

  switch (patch.type) {
    case "CREATE":
      {
        const dom = createDomTree(patch);
        if (dom) {
          parent.insertBefore(dom, child ?? null);
        }
      }
      break;
    case "REMOVE":
      if (child) {
        parent.removeChild(child);
      }
      break;
    case "REPLACE":
      if (!patch.newNode) {
        return;
      }

      {
        const dom = createDomTree(patch);
        if (!dom) {
          return;
        }

        if (child) {
          parent.replaceChild(dom, child);
        } else {
          parent.insertBefore(dom, null);
        }
      }
      break;
    case "UPDATE":
      if (child && patch.oldNode && patch.newNode) {
        updateDom(child as HTMLElement | Text, patch.oldNode.props, patch.newNode.props);
      }

      if (child) {
        applyPatches(child as HTMLElement, patch.children ?? []);
      }
      break;
  }
}

export function applyPatches(parent: HTMLElement | Text, patches: Patch[]): void {
  const removals = patches
    .filter((patch) => patch.type === "REMOVE")
    .sort((left, right) => (right.index ?? 0) - (left.index ?? 0));

  const others = patches.filter((patch) => patch.type !== "REMOVE");

  others.forEach((patch) => {
    applyPatchAt(parent, patch, patch.index ?? 0);
  });

  removals.forEach((patch) => {
    applyPatchAt(parent, patch, patch.index ?? 0);
  });
}
