import express, { Application } from "express";
import { createBookRouter } from "./routes/book.router";
import { requestLogger, responseWrapper, errorHandler } from "./middleware";

export function createApp(): Application {
  const app = express();

  // --- 라우트 전 middleware (파이프라인: 위 -> 아래) ---
  app.use(requestLogger);
  app.use(express.json());
  app.use(responseWrapper);

  // --- 라우트 ---
  app.use("/books", createBookRouter());

  // --- 라우트 이후 middleware ---
  app.use(errorHandler);

  return app;
}
