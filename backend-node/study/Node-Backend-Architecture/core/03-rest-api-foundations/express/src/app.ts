import express, { Request, Response, NextFunction } from "express";
import { BookService } from "./services/book.service";
import { BookController } from "./controllers/book.controller";
import { createBookRouter } from "./routes/book.router";

/**
 * Express 애플리케이션을 만들고 설정한다.
 *
 * 여기가 COMPOSITION ROOT이며 모든 의존성 연결이 여기서 일어난다.
 * 의존성 흐름: Service -> Controller -> Router -> App
 */
export function createApp(): express.Application {
  const app = express();

  // --- middleware ---
  app.use(express.json());

  // --- 수동 Dependency Injection ---
  const bookService = new BookService();
  const bookController = new BookController(bookService);
  const bookRouter = createBookRouter(bookController);

  // --- 라우트 mount ---
  app.use("/books", bookRouter);

  // --- 전역 오류 처리기 ---
  app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
    console.error(`[Error] ${err.message}`);
    res.status(500).json({ error: "Internal Server Error" });
  });

  return app;
}
