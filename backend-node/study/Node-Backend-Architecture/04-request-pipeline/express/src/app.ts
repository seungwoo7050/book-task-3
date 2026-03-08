import express, { Application } from "express";
import { createBookRouter } from "./routes/book.router";
import { requestLogger, responseWrapper, errorHandler } from "./middleware";

export function createApp(): Application {
  const app = express();

  // --- Pre-route middleware (Pipeline: top → bottom) ---
  app.use(requestLogger);
  app.use(express.json());
  app.use(responseWrapper);

  // --- Routes ---
  app.use("/books", createBookRouter());

  // --- Post-route middleware ---
  app.use(errorHandler);

  return app;
}
