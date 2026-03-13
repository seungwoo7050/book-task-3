import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { WorkspaceShell } from "@/components/workspace-shell";
import { MemoryCollabTransport } from "@/lib/transport";
import { createPatchEnvelope } from "@/lib/workspace-state";

describe("WorkspaceShell", () => {
  it("applies optimistic local edits and reacts to remote collaboration events", async () => {
    const transport = new MemoryCollabTransport();

    render(
      <WorkspaceShell
        disableHeartbeat
        transport={transport}
        viewerHint="atlas"
      />,
    );

    expect(screen.getByTestId("connection-status")).toHaveTextContent(
      "Connected",
    );

    fireEvent.change(screen.getByTestId("card-input-card-1"), {
      target: { value: "Atlas local patch" },
    });

    expect(screen.getByTestId("card-input-card-1")).toHaveValue(
      "Atlas local patch",
    );

    act(() => {
      transport.emitPresence({
        clientId: "rio-remote",
        label: "Rio",
        color: "#1f6f7a",
        lastSeenAt: 50,
        status: "online",
      });
      transport.emitPatch(
        createPatchEnvelope({
          clientId: "rio-remote",
          clientLabel: "Rio",
          entityType: "card",
          entityId: "card-1",
          field: "title",
          value: "Rio overwrite",
          createdAt: 55,
        }),
      );
    });

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Conflict detected");
    });
    expect(screen.getByTestId("presence-list")).toHaveTextContent("Rio");
    expect(screen.getByTestId("activity-log")).toHaveTextContent("Remote card patch");
  });
});
