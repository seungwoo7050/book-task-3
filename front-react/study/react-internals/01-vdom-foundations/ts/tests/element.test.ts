import { describe, expect, it } from "vitest";
import { createElement, createTextElement } from "../src/element";

describe("createTextElement", () => {
  it("should create a text VNode with type TEXT_ELEMENT", () => {
    const node = createTextElement("Hello");

    expect(node.type).toBe("TEXT_ELEMENT");
    expect(node.props.nodeValue).toBe("Hello");
    expect(node.props.children).toEqual([]);
  });

  it("should handle empty strings", () => {
    const node = createTextElement("");

    expect(node.type).toBe("TEXT_ELEMENT");
    expect(node.props.nodeValue).toBe("");
  });
});

describe("createElement", () => {
  it("should create a VNode with the given type", () => {
    const node = createElement("div", null);

    expect(node.type).toBe("div");
  });

  it("should merge props into the VNode", () => {
    const node = createElement("div", { id: "app", className: "container" });

    expect(node.props.id).toBe("app");
    expect(node.props.className).toBe("container");
  });

  it("should treat null props as an empty object", () => {
    const node = createElement("div", null);

    expect(node.props.children).toEqual([]);
    const keys = Object.keys(node.props);
    expect(keys).toEqual(["children"]);
  });

  it("should always include a children array", () => {
    const node = createElement("span", { id: "x" });

    expect(Array.isArray(node.props.children)).toBe(true);
    expect(node.props.children).toHaveLength(0);
  });

  it("should wrap string children as TEXT_ELEMENT VNodes", () => {
    const node = createElement("p", null, "Hello");

    expect(node.props.children).toHaveLength(1);

    const child = node.props.children[0];
    expect(child.type).toBe("TEXT_ELEMENT");
    expect(child.props.nodeValue).toBe("Hello");
  });

  it("should wrap number children as TEXT_ELEMENT VNodes", () => {
    const node = createElement("span", null, 42);

    const child = node.props.children[0];
    expect(child.type).toBe("TEXT_ELEMENT");
    expect(child.props.nodeValue).toBe("42");
  });

  it("should keep VNode children as-is", () => {
    const child = createElement("span", null, "inner");
    const parent = createElement("div", null, child);

    expect(parent.props.children).toHaveLength(1);
    expect(parent.props.children[0]).toBe(child);
    expect(parent.props.children[0].type).toBe("span");
  });

  it("should handle multiple mixed children", () => {
    const span = createElement("span", null, "bold");
    const node = createElement("p", null, "Hello ", span, " world");

    expect(node.props.children).toHaveLength(3);
    expect(node.props.children[0].type).toBe("TEXT_ELEMENT");
    expect(node.props.children[1].type).toBe("span");
    expect(node.props.children[2].type).toBe("TEXT_ELEMENT");
  });

  it("should handle deeply nested structures", () => {
    const tree = createElement(
      "div",
      { id: "root" },
      createElement(
        "ul",
        null,
        createElement("li", null, "One"),
        createElement("li", null, "Two"),
      ),
    );

    expect(tree.type).toBe("div");
    const ul = tree.props.children[0];
    expect(ul.type).toBe("ul");
    expect(ul.props.children).toHaveLength(2);
    expect(ul.props.children[0].props.children[0].props.nodeValue).toBe("One");
  });
});

