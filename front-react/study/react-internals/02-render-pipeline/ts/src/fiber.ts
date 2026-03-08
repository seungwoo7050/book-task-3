import { createDom } from "@front-react/vdom-foundations";

import type { Fiber, VNode } from "./types";

export function reconcileChildren(wipFiber: Fiber, elements: VNode[]): Fiber[] {
  const deletions: Fiber[] = [];
  let index = 0;
  let oldFiber = wipFiber.alternate?.child ?? null;
  let previousSibling: Fiber | null = null;

  while (index < elements.length || oldFiber) {
    const element = elements[index];
    let nextFiber: Fiber | null = null;

    const sameType = Boolean(oldFiber && element && oldFiber.type === element.type);

    if (sameType && oldFiber) {
      nextFiber = {
        type: oldFiber.type,
        props: element.props,
        dom: oldFiber.dom,
        parent: wipFiber,
        child: null,
        sibling: null,
        alternate: oldFiber,
        effectTag: "UPDATE",
      };
    }

    if (element && !sameType) {
      nextFiber = {
        type: element.type as string,
        props: element.props,
        dom: null,
        parent: wipFiber,
        child: null,
        sibling: null,
        alternate: null,
        effectTag: "PLACEMENT",
      };
    }

    if (oldFiber && !sameType) {
      oldFiber.effectTag = "DELETION";
      deletions.push(oldFiber);
    }

    if (oldFiber) {
      oldFiber = oldFiber.sibling;
    }

    if (index === 0) {
      wipFiber.child = nextFiber;
    } else if (previousSibling && nextFiber) {
      previousSibling.sibling = nextFiber;
    }

    if (nextFiber) {
      previousSibling = nextFiber;
    }

    index += 1;
  }

  return deletions;
}

export function performUnitOfWork(
  fiber: Fiber,
  onDeletion?: (fiber: Fiber) => void,
): Fiber | null {
  if (!fiber.dom && fiber.type !== "ROOT") {
    fiber.dom = createDom({
      type: fiber.type,
      props: fiber.props,
    });
  }

  const deletions = reconcileChildren(fiber, fiber.props.children ?? []);
  deletions.forEach((deletion) => onDeletion?.(deletion));

  if (fiber.child) {
    return fiber.child;
  }

  let nextFiber: Fiber | null = fiber;
  while (nextFiber) {
    if (nextFiber.sibling) {
      return nextFiber.sibling;
    }
    nextFiber = nextFiber.parent;
  }

  return null;
}
