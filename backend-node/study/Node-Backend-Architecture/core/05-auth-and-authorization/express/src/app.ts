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

  // 수동 DI
  const authService = new AuthService();
  const bookService = new BookService();
  const authController = new AuthController(authService);
  const bookController = new BookController(bookService);

  // 라우트
  app.use("/auth", createAuthRouter(authController));
  app.use("/books", createBookRouter(bookController));

  // 전역 오류 처리기
  app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
    console.error(`[Error] ${err.message}`);
    res.status(500).json({ error: "Internal Server Error" });
  });

  return app;
}
