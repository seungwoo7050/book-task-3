# Original Problem Spec

Source: `legacy/virtual-dom/problem/README.md`
Provenance: `original`

---

# Problem: Implement a Virtual DOM Engine

## Objective

Build the foundational layer of a React-like framework by implementing:

1. **`createElement(type, props, ...children)`** — Converts JSX-like function calls into plain JavaScript objects (VDOM nodes).
2. **`createTextElement(text)`** — Wraps primitive values (strings, numbers) into VDOM nodes with type `"TEXT_ELEMENT"`.
3. **`createDom(vnode)`** — Converts a single VDOM node into a real DOM node (HTMLElement or Text).
4. **`updateDom(dom, prevProps, nextProps)`** — Applies property and event listener changes to an existing DOM node.
5. **`render(element, container)`** — Recursively renders an entire VDOM tree into a DOM container.

## Specification

### 1. VNode Structure

Every VDOM node must conform to the following shape:

```typescript
interface VNode {
  type: string | Function;
  props: {
    [key: string]: any;
    children: VNode[];
  };
}
```

- `type` is a tag name string (e.g., `"div"`, `"span"`) or a function component.
- `props.children` is **always** an array, even when empty.

### 2. createElement

```typescript
function createElement(
  type: string,
  props: Record<string, any> | null,
  ...children: any[]
): VNode
```

**Rules:**
- When `props` is `null`, treat it as `{}`.
- Each child that is **not** an object must be wrapped with `createTextElement`.
- Numeric children must be converted to their string representation before wrapping.

### 3. createTextElement

```typescript
function createTextElement(text: string): VNode
```

**Rules:**
- Returns a VNode with `type: "TEXT_ELEMENT"`.
- Sets `props.nodeValue` to the text value.
- Sets `props.children` to an empty array `[]`.

### 4. createDom

```typescript
function createDom(vnode: VNode): HTMLElement | Text
```

**Rules:**
- If `vnode.type === "TEXT_ELEMENT"`, create a `Text` node via `document.createTextNode("")`.
- Otherwise, create an element via `document.createElement(vnode.type)`.
- Apply all properties from `vnode.props` to the created node using `updateDom`.

### 5. updateDom

```typescript
function updateDom(
  dom: HTMLElement | Text,
  prevProps: Record<string, any>,
  nextProps: Record<string, any>
): void
```

**Rules:**
- **Remove** old event listeners (keys starting with `"on"`) that are absent or changed in `nextProps`.
- **Remove** old properties (set to `""`) that are absent in `nextProps`.
- **Set** new or changed properties via direct assignment (`dom[key] = value`).
- **Add** new or changed event listeners via `addEventListener`.
- Always skip the `children` key — it is handled by the render function.

### 6. render

```typescript
function render(element: VNode, container: HTMLElement | Text): void
```

**Rules:**
- Create a DOM node for `element` using `createDom`.
- Recursively call `render` for each child in `element.props.children`.
- Append the created DOM node to `container`.

## Starter Code

Skeleton files are provided in `code/`. They contain the type definitions, function signatures, and `TODO` markers where your implementation should go.

## Acceptance Criteria

All tests in `../solve/test/` must pass:

```bash
make test
```

| Test File | What it verifies |
|-----------|-----------------|
| `element.test.ts` | `createElement` and `createTextElement` produce correct VDOM structures |
| `dom-utils.test.ts` | `createDom`, `updateDom`, and `render` produce correct DOM output |

