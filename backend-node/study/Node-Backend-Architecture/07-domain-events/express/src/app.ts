import express, { Application } from "express";
import Database from "better-sqlite3";
import { EventBus } from "./events/event-bus";
import { BookEventListener } from "./events/book-event-listener";
import { createBookRouter } from "./routes/book.router";
import { requestLogger } from "./middleware/request-logger";
import { responseWrapper } from "./middleware/response-wrapper";
import { errorHandler } from "./middleware/error-handler";

export function createApp(db: Database.Database, eventBus?: EventBus): Application {
  const bus = eventBus ?? new EventBus();

  // Register event listeners
  new BookEventListener(bus);

  const app = express();

  app.use(requestLogger);
  app.use(express.json());
  app.use(responseWrapper);

  app.use("/books", createBookRouter(db, bus));

  app.use(errorHandler);

  return app;
}
