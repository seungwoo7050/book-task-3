import { VNode } from "./types";

const isEvent = (key: string): boolean => key.startsWith("on");

const isProperty = (key: string): boolean =>
  key !== "children" && !isEvent(key);

const isNew =
  (prev: Record<string, any>, next: Record<string, any>) =>
  (key: string): boolean =>
    prev[key] !== next[key];

const isGone =
  (_prev: Record<string, any>, next: Record<string, any>) =>
  (key: string): boolean =>
    !(key in next);

export function createDom(vnode: VNode): HTMLElement | Text {
  const dom =
    vnode.type === "TEXT_ELEMENT"
      ? document.createTextNode("")
      : document.createElement(vnode.type as string);

  updateDom(dom, {}, vnode.props);

  return dom;
}

export function updateDom(
  dom: HTMLElement | Text,
  prevProps: Record<string, any>,
  nextProps: Record<string, any>,
): void {
  Object.keys(prevProps)
    .filter(isEvent)
    .filter((key) => !(key in nextProps) || isNew(prevProps, nextProps)(key))
    .forEach((name) => {
      const eventType = name.toLowerCase().substring(2);
      dom.removeEventListener(eventType, prevProps[name]);
    });

  Object.keys(prevProps)
    .filter(isProperty)
    .filter(isGone(prevProps, nextProps))
    .forEach((name) => {
      (dom as any)[name] = "";
    });

  Object.keys(nextProps)
    .filter(isProperty)
    .filter(isNew(prevProps, nextProps))
    .forEach((name) => {
      (dom as any)[name] = nextProps[name];
    });

  Object.keys(nextProps)
    .filter(isEvent)
    .filter(isNew(prevProps, nextProps))
    .forEach((name) => {
      const eventType = name.toLowerCase().substring(2);
      dom.addEventListener(eventType, nextProps[name]);
    });
}

export function render(element: VNode, container: HTMLElement | Text): void {
  const dom = createDom(element);

  if (element.props.children) {
    element.props.children.forEach((child) => {
      render(child, dom);
    });
  }

  container.appendChild(dom);
}

