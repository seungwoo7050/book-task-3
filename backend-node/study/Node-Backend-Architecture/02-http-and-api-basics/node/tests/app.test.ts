import request from "supertest";
import { describe, expect, it } from "vitest";

import { createApp } from "../src/app";

describe("frameworkless http server", () => {
  it("returns health information", async () => {
    await request(createApp())
      .get("/health")
      .expect(200)
      .expect("content-type", /json/)
      .expect({ status: "ok" });
  });

  it("creates and fetches a book", async () => {
    const app = createApp();

    const created = await request(app)
      .post("/books")
      .set("content-type", "application/json")
      .send({
        title: "Node for Backend Engineers",
        author: "Alice",
        publishedYear: 2026,
      })
      .expect(201);

    expect(created.body.id).toBe("1");

    await request(app)
      .get("/books")
      .expect(200)
      .expect(({ body }) => {
        expect(body).toHaveLength(1);
        expect(body[0]?.title).toBe("Node for Backend Engineers");
      });

    await request(app)
      .get("/books/1")
      .expect(200)
      .expect(({ body }) => {
        expect(body.author).toBe("Alice");
      });
  });

  it("returns 400 for invalid payloads", async () => {
    await request(createApp())
      .post("/books")
      .set("content-type", "application/json")
      .send({
        title: "",
        author: "Alice",
        publishedYear: 2026,
      })
      .expect(400)
      .expect(({ body }) => {
        expect(body.message).toContain("title is required");
      });
  });

  it("returns 415 when content-type is wrong", async () => {
    await request(createApp())
      .post("/books")
      .set("content-type", "text/plain")
      .send("plain text")
      .expect(415);
  });
});
