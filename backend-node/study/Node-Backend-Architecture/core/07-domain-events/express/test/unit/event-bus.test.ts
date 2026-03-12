import { describe, it, expect, beforeEach, vi } from "vitest";
import { EventBus } from "../../src/events/event-bus";

describe("EventBus", () => {
  let bus: EventBus;

  beforeEach(() => {
    bus = new EventBus();
  });

  it("should emit and receive book.created events", () => {
    const handler = vi.fn();
    bus.on("book.created", handler);

    const event = { bookId: "1", title: "Test", author: "Author", timestamp: new Date() };
    bus.emit("book.created", event);

    expect(handler).toHaveBeenCalledOnce();
    expect(handler).toHaveBeenCalledWith(event);
  });

  it("should emit and receive book.updated events", () => {
    const handler = vi.fn();
    bus.on("book.updated", handler);

    bus.emit("book.updated", { bookId: "1", changes: ["title"], timestamp: new Date() });

    expect(handler).toHaveBeenCalledOnce();
  });

  it("should emit and receive book.deleted events", () => {
    const handler = vi.fn();
    bus.on("book.deleted", handler);

    bus.emit("book.deleted", { bookId: "1", timestamp: new Date() });

    expect(handler).toHaveBeenCalledOnce();
  });

  it("should support multiple listeners", () => {
    const handler1 = vi.fn();
    const handler2 = vi.fn();
    bus.on("book.created", handler1);
    bus.on("book.created", handler2);

    bus.emit("book.created", { bookId: "1", title: "T", author: "A", timestamp: new Date() });

    expect(handler1).toHaveBeenCalledOnce();
    expect(handler2).toHaveBeenCalledOnce();
  });

  it("should allow removing listeners", () => {
    const handler = vi.fn();
    bus.on("book.created", handler);
    bus.off("book.created", handler);

    bus.emit("book.created", { bookId: "1", title: "T", author: "A", timestamp: new Date() });

    expect(handler).not.toHaveBeenCalled();
  });
});
