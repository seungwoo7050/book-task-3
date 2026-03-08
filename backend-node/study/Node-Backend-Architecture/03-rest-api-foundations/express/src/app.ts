import express, { Request, Response, NextFunction } from "express";
import { BookService } from "./services/book.service";
import { BookController } from "./controllers/book.controller";
import { createBookRouter } from "./routes/book.router";

/**
 * Creates and configures the Express application.
 *
 * This is the COMPOSITION ROOT — all dependency wiring happens here.
 * Dependencies flow: Service → Controller → Router → App
 */
export function createApp(): express.Application {
  const app = express();

  // --- Middleware ---
  app.use(express.json());

  // --- Manual Dependency Injection ---
  const bookService = new BookService();
  const bookController = new BookController(bookService);
  const bookRouter = createBookRouter(bookController);

  // --- Route Mounting ---
  app.use("/books", bookRouter);

  // --- Global Error Handler ---
  app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
    console.error(`[Error] ${err.message}`);
    res.status(500).json({ error: "Internal Server Error" });
  });

  return app;
}
