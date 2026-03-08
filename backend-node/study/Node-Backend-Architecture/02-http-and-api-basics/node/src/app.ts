import http, { type IncomingMessage, type ServerResponse } from "node:http";

import { BookStore, validateCreateBookPayload } from "./book-store";

type JsonResponse = Record<string, unknown> | Record<string, unknown>[];

async function readJsonBody(request: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];

  for await (const chunk of request) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }

  const body = Buffer.concat(chunks).toString("utf8");
  if (body.trim().length === 0) {
    return {};
  }

  return JSON.parse(body);
}

function sendJson(response: ServerResponse, statusCode: number, payload: JsonResponse): void {
  response.statusCode = statusCode;
  response.setHeader("content-type", "application/json; charset=utf-8");
  response.end(JSON.stringify(payload));
}

function matchBookId(url: string): string | null {
  const match = /^\/books\/([^/]+)$/.exec(url);

  return match?.[1] ?? null;
}

export function createApp(store = new BookStore()): http.Server {
  return http.createServer(async (request, response) => {
    const method = request.method ?? "GET";
    const url = request.url ?? "/";

    try {
      if (method === "GET" && url === "/health") {
        sendJson(response, 200, { status: "ok" });

        return;
      }

      if (method === "GET" && url === "/books") {
        sendJson(response, 200, store.list());

        return;
      }

      if (method === "GET") {
        const bookId = matchBookId(url);
        if (bookId) {
          const book = store.getById(bookId);

          if (!book) {
            sendJson(response, 404, { message: "Book not found" });

            return;
          }

          sendJson(response, 200, book);

          return;
        }
      }

      if (method === "POST" && url === "/books") {
        const contentType = request.headers["content-type"];
        if (!contentType?.startsWith("application/json")) {
          sendJson(response, 415, { message: "content-type must be application/json" });

          return;
        }

        const rawPayload = await readJsonBody(request);
        const payload = validateCreateBookPayload(rawPayload);
        const book = store.create(payload);
        sendJson(response, 201, book);

        return;
      }

      sendJson(response, 404, { message: "Route not found" });
    } catch (error) {
      if (error instanceof SyntaxError) {
        sendJson(response, 400, { message: "Request body must be valid JSON" });

        return;
      }

      if (error instanceof Error) {
        sendJson(response, 400, { message: error.message });

        return;
      }

      sendJson(response, 500, { message: "Internal server error" });
    }
  });
}
