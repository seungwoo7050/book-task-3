import { Injectable } from "@nestjs/common";
import { OnEvent } from "@nestjs/event-emitter";
import {
  BookCreatedEvent,
  BookUpdatedEvent,
  BookDeletedEvent,
  UserRegisteredEvent,
} from "./events";

@Injectable()
export class AppEventListener {
  @OnEvent("book.created")
  handleBookCreated(event: BookCreatedEvent): void {
    try {
      this.writeLog("book.created", event);
    } catch (error) {
      this.writeError("book.created", error);
    }
  }

  @OnEvent("book.updated")
  handleBookUpdated(event: BookUpdatedEvent): void {
    try {
      this.writeLog("book.updated", event);
    } catch (error) {
      this.writeError("book.updated", error);
    }
  }

  @OnEvent("book.deleted")
  handleBookDeleted(event: BookDeletedEvent): void {
    try {
      this.writeLog("book.deleted", event);
    } catch (error) {
      this.writeError("book.deleted", error);
    }
  }

  @OnEvent("user.registered")
  handleUserRegistered(event: UserRegisteredEvent): void {
    try {
      this.writeLog("user.registered", event);
    } catch (error) {
      this.writeError("user.registered", error);
    }
  }

  private writeLog(name: string, payload: unknown): void {
    process.stdout.write(`${JSON.stringify({ level: "info", event: name, payload })}\n`);
  }

  private writeError(name: string, error: unknown): void {
    process.stderr.write(
      `${JSON.stringify({ level: "error", event: name, error: String(error) })}\n`,
    );
  }
}
