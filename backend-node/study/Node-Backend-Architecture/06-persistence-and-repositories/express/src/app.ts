import express, { Application } from "express";
import Database from "better-sqlite3";
import { createBookRouter } from "./routes/book.router";
import { requestLogger } from "./middleware/request-logger";
import { responseWrapper } from "./middleware/response-wrapper";
import { errorHandler } from "./middleware/error-handler";

export function createApp(db: Database.Database): Application {
  const app = express();

  app.use(requestLogger);
  app.use(express.json());
  app.use(responseWrapper);

  app.use("/books", createBookRouter(db));

  app.use(errorHandler);

  return app;
}
