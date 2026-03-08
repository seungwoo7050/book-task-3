import { updateDom } from "@front-react/vdom-foundations";

import { performUnitOfWork } from "./fiber";

import type { Fiber, IdleDeadlineLike, VNode } from "./types";

let nextUnitOfWork: Fiber | null = null;
let wipRoot: Fiber | null = null;
let currentRoot: Fiber | null = null;
let deletions: Fiber[] = [];

function getParentDom(fiber: Fiber): HTMLElement | Text {
  let parent = fiber.parent;
  while (parent && !parent.dom) {
    parent = parent.parent;
  }

  if (!parent?.dom) {
    throw new Error("Cannot commit fiber without a host parent.");
  }

  return parent.dom;
}

function commitDeletion(fiber: Fiber, parentDom: HTMLElement | Text): void {
  if (fiber.dom) {
    parentDom.removeChild(fiber.dom);
    return;
  }

  if (fiber.child) {
    commitDeletion(fiber.child, parentDom);
  }
}

function commitWork(fiber: Fiber | null): void {
  if (!fiber) {
    return;
  }

  const parentDom = getParentDom(fiber);

  if (fiber.effectTag === "PLACEMENT" && fiber.dom) {
    parentDom.appendChild(fiber.dom);
  } else if (fiber.effectTag === "UPDATE" && fiber.dom) {
    updateDom(fiber.dom, fiber.alternate?.props ?? {}, fiber.props);
  } else if (fiber.effectTag === "DELETION") {
    commitDeletion(fiber, parentDom);
  }

  commitWork(fiber.child);
  commitWork(fiber.sibling);
}

function commitRoot(): void {
  deletions.forEach((fiber) => commitWork(fiber));
  deletions = [];
  commitWork(wipRoot?.child ?? null);
  currentRoot = wipRoot;
  wipRoot = null;
}

export function render(element: VNode, container: HTMLElement): void {
  wipRoot = {
    type: "ROOT",
    props: {
      children: [element],
    },
    dom: container,
    parent: null,
    child: null,
    sibling: null,
    alternate: currentRoot,
  };
  deletions = [];
  nextUnitOfWork = wipRoot;
}

export function workLoop(deadline: IdleDeadlineLike): void {
  let shouldYield = false;

  while (nextUnitOfWork && !shouldYield) {
    nextUnitOfWork = performUnitOfWork(nextUnitOfWork, (fiber) => {
      deletions.push(fiber);
    });
    shouldYield = deadline.timeRemaining() < 1;
  }

  if (!nextUnitOfWork && wipRoot) {
    commitRoot();
  }
}

export function flushSync(): void {
  workLoop({
    timeRemaining() {
      return Number.POSITIVE_INFINITY;
    },
  });
}

export function resetScheduler(): void {
  nextUnitOfWork = null;
  wipRoot = null;
  currentRoot = null;
  deletions = [];
}
