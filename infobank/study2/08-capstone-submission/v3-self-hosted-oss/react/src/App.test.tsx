import { fireEvent, render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { App } from "./App";
import { mockFetchRoutes } from "./testUtils";

describe("App", () => {
  it("renders the login gate and then the product shell", async () => {
    mockFetchRoutes([
      {
        path: "/api/auth/session",
        body: { authenticated: false, email: null },
      },
      {
        method: "POST",
        path: "/api/auth/login",
        body: { authenticated: true, email: "admin@example.com" },
      },
      {
        path: "/api/jobs",
        body: { items: [] },
      },
    ]);

    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>,
    );

    expect(await screen.findByText("Self-Hosted QA Ops")).toBeDefined();

    fireEvent.click(screen.getByText("로그인"));

    expect(await screen.findByText("single-team self-hosted QA Ops workflow")).toBeDefined();
    expect(screen.getByText("Datasets")).toBeDefined();
    expect(screen.getByText("Knowledge Base")).toBeDefined();
  });
});
