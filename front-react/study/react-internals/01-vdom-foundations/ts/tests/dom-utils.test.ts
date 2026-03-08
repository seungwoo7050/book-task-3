import { beforeEach, describe, expect, it, vi } from "vitest";
import { createDom, render, updateDom } from "../src/dom-utils";
import { createElement, createTextElement } from "../src/element";

describe("createDom", () => {
  it("should create a Text node for TEXT_ELEMENT", () => {
    const vnode = createTextElement("Hello");
    const dom = createDom(vnode);

    expect(dom).toBeInstanceOf(Text);
    expect(dom.nodeValue).toBe("Hello");
  });

  it("should create an HTMLElement for a tag type", () => {
    const vnode = createElement("div", { id: "test" });
    const dom = createDom(vnode) as HTMLElement;

    expect(dom).toBeInstanceOf(HTMLDivElement);
    expect(dom.id).toBe("test");
  });

  it("should apply className as a property", () => {
    const vnode = createElement("span", { className: "highlight" });
    const dom = createDom(vnode) as HTMLElement;

    expect(dom.className).toBe("highlight");
  });
});

describe("updateDom", () => {
  it("should set new properties", () => {
    const dom = document.createElement("div");
    updateDom(dom, {}, { id: "new", className: "box" });

    expect(dom.id).toBe("new");
    expect(dom.className).toBe("box");
  });

  it("should remove old properties by setting them to empty string", () => {
    const dom = document.createElement("div");
    (dom as any).id = "old";

    updateDom(dom, { id: "old" }, {});

    expect(dom.id).toBe("");
  });

  it("should update changed properties", () => {
    const dom = document.createElement("div");
    updateDom(dom, { id: "old" }, { id: "new" });

    expect(dom.id).toBe("new");
  });

  it("should not touch unchanged properties", () => {
    const dom = document.createElement("div");
    dom.id = "same";
    updateDom(dom, { id: "same" }, { id: "same" });

    expect(dom.id).toBe("same");
  });

  it("should add event listeners", () => {
    const dom = document.createElement("button");
    const handler = vi.fn();

    updateDom(dom, {}, { onClick: handler });
    dom.click();

    expect(handler).toHaveBeenCalledTimes(1);
  });

  it("should remove old event listeners", () => {
    const dom = document.createElement("button");
    const handler = vi.fn();

    updateDom(dom, {}, { onClick: handler });
    updateDom(dom, { onClick: handler }, {});
    dom.click();

    expect(handler).not.toHaveBeenCalled();
  });

  it("should replace changed event listeners", () => {
    const dom = document.createElement("button");
    const oldHandler = vi.fn();
    const newHandler = vi.fn();

    updateDom(dom, {}, { onClick: oldHandler });
    updateDom(dom, { onClick: oldHandler }, { onClick: newHandler });
    dom.click();

    expect(oldHandler).not.toHaveBeenCalled();
    expect(newHandler).toHaveBeenCalledTimes(1);
  });

  it("should skip the children key", () => {
    const dom = document.createElement("div");

    updateDom(dom, {}, { children: [], id: "ok" });

    expect(dom.id).toBe("ok");
    expect((dom as any).children).not.toEqual([]);
  });
});

describe("render", () => {
  let container: HTMLElement;

  beforeEach(() => {
    container = document.createElement("div");
  });

  it("should render a simple text element", () => {
    const vnode = createElement("p", null, "Hello");
    render(vnode, container);

    expect(container.innerHTML).toBe("<p>Hello</p>");
  });

  it("should render nested elements", () => {
    const vnode = createElement(
      "div",
      { id: "root" },
      createElement("h1", null, "Title"),
      createElement("p", null, "Body"),
    );

    render(vnode, container);

    const root = container.querySelector("#root");
    expect(root).toBeTruthy();
    expect(root!.querySelector("h1")!.textContent).toBe("Title");
    expect(root!.querySelector("p")!.textContent).toBe("Body");
  });

  it("should render elements with properties", () => {
    const vnode = createElement("input", {
      type: "text",
      value: "hello",
    });

    render(vnode, container);
    const input = container.querySelector("input") as HTMLInputElement;

    expect(input.type).toBe("text");
    expect(input.value).toBe("hello");
  });

  it("should render deeply nested trees", () => {
    const vnode = createElement(
      "div",
      null,
      createElement(
        "ul",
        null,
        createElement("li", null, "A"),
        createElement("li", null, "B"),
        createElement("li", null, "C"),
      ),
    );

    render(vnode, container);

    const items = container.querySelectorAll("li");
    expect(items).toHaveLength(3);
    expect(items[0].textContent).toBe("A");
    expect(items[1].textContent).toBe("B");
    expect(items[2].textContent).toBe("C");
  });

  it("should handle multiple renders into the same container", () => {
    render(createElement("p", null, "First"), container);
    render(createElement("p", null, "Second"), container);

    const paragraphs = container.querySelectorAll("p");
    expect(paragraphs).toHaveLength(2);
  });
});

