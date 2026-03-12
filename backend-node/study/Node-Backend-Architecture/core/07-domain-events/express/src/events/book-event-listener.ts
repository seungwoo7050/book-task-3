import { EventBus } from "./event-bus";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "../types/events";

export class BookEventListener {
  constructor(private readonly eventBus: EventBus) {
    this.registerListeners();
  }

  private registerListeners(): void {
    this.eventBus.on("book.created", this.onBookCreated.bind(this));
    this.eventBus.on("book.updated", this.onBookUpdated.bind(this));
    this.eventBus.on("book.deleted", this.onBookDeleted.bind(this));
  }

  private onBookCreated(event: BookCreatedEvent): void {
    try {
      console.log(
        `[Event] Book created: "${event.title}" by ${event.author} (${event.bookId})`,
      );
    } catch (err) {
      console.error("[Event Listener Error] book.created:", err);
    }
  }

  private onBookUpdated(event: BookUpdatedEvent): void {
    try {
      console.log(
        `[Event] Book updated: ${event.bookId} — changed: ${event.changes.join(", ")}`,
      );
    } catch (err) {
      console.error("[Event Listener Error] book.updated:", err);
    }
  }

  private onBookDeleted(event: BookDeletedEvent): void {
    try {
      console.log(`[Event] Book deleted: ${event.bookId}`);
    } catch (err) {
      console.error("[Event Listener Error] book.deleted:", err);
    }
  }
}
