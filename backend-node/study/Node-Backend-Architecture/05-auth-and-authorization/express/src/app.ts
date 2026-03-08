import express, { Request, Response, NextFunction } from "express";
import { AuthService } from "./services/auth.service";
import { BookService } from "./services/book.service";
import { AuthController } from "./controllers/auth.controller";
import { BookController } from "./controllers/book.controller";
import { createAuthRouter } from "./routes/auth.router";
import { createBookRouter } from "./routes/book.router";

export function createApp(): express.Application {
  const app = express();
  app.use(express.json());

  // Manual DI
  const authService = new AuthService();
  const bookService = new BookService();
  const authController = new AuthController(authService);
  const bookController = new BookController(bookService);

  // Routes
  app.use("/auth", createAuthRouter(authController));
  app.use("/books", createBookRouter(bookController));

  // Global error handler
  app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
    console.error(`[Error] ${err.message}`);
    res.status(500).json({ error: "Internal Server Error" });
  });

  return app;
}
