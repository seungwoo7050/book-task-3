import { Injectable } from "@nestjs/common";
import { OnEvent } from "@nestjs/event-emitter";
import { BookCreatedEvent, BookUpdatedEvent, BookDeletedEvent } from "./events";

@Injectable()
export class BookEventListener {
  @OnEvent("book.created")
  handleBookCreated(event: BookCreatedEvent): void {
    try {
      console.log(`[Event] Book created: "${event.title}" by ${event.author} (id=${event.bookId})`);
    } catch (error) {
      console.error("[Event] Error handling book.created:", error);
    }
  }

  @OnEvent("book.updated")
  handleBookUpdated(event: BookUpdatedEvent): void {
    try {
      console.log(`[Event] Book updated: id=${event.bookId}, changes=[${event.changes.join(", ")}]`);
    } catch (error) {
      console.error("[Event] Error handling book.updated:", error);
    }
  }

  @OnEvent("book.deleted")
  handleBookDeleted(event: BookDeletedEvent): void {
    try {
      console.log(`[Event] Book deleted: id=${event.bookId}`);
    } catch (error) {
      console.error("[Event] Error handling book.deleted:", error);
    }
  }
}
