import { describe, it, expect, vi } from "vitest";
import { BookEventListener } from "../../src/events/book-event.listener";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "../../src/events/events";

describe("BookEventListener", () => {
  const listener = new BookEventListener();

  it("should handle book.created event", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const event = new BookCreatedEvent("1", "Test Book", "Test Author");

    listener.handleBookCreated(event);

    expect(spy).toHaveBeenCalledWith(expect.stringContaining("Test Book"));
    spy.mockRestore();
  });

  it("should handle book.updated event", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const event = new BookUpdatedEvent("1", ["title", "price"]);

    listener.handleBookUpdated(event);

    expect(spy).toHaveBeenCalledWith(expect.stringContaining("title, price"));
    spy.mockRestore();
  });

  it("should handle book.deleted event", () => {
    const spy = vi.spyOn(console, "log").mockImplementation(() => {});
    const event = new BookDeletedEvent("1");

    listener.handleBookDeleted(event);

    expect(spy).toHaveBeenCalledWith(expect.stringContaining("id=1"));
    spy.mockRestore();
  });
});
