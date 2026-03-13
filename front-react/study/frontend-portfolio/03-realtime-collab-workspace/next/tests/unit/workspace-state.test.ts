import { describe, expect, it } from "vitest";
import { createViewerIdentity } from "@/lib/storage";
import {
  applyOptimisticPatch,
  applyPresencePing,
  applyRemotePatch,
  clearConflictBanner,
  createInitialWorkspaceState,
  createPatchEnvelope,
  flushQueuedPatches,
  queuePatch,
} from "@/lib/workspace-state";

describe("workspace-state", () => {
  it("merges optimistic patches into the board immediately", () => {
    const viewer = createViewerIdentity("atlas");
    const state = createInitialWorkspaceState(viewer);
    const patch = createPatchEnvelope({
      clientId: viewer.clientId,
      clientLabel: viewer.label,
      entityType: "card",
      entityId: "card-1",
      field: "title",
      value: "Atlas board update",
      createdAt: 10,
    });

    const next = applyOptimisticPatch(state, patch);

    expect(next.cards.find((card) => card.id === "card-1")?.title).toBe(
      "Atlas board update",
    );
    expect(next.activity[0]?.summary).toContain("Optimistic card patch");
  });

  it("updates presence from remote heartbeats", () => {
    const viewer = createViewerIdentity("atlas");
    const state = createInitialWorkspaceState(viewer);

    const next = applyPresencePing(state, {
      clientId: "rio-remote",
      label: "Rio",
      color: "#1f6f7a",
      lastSeenAt: 20,
      status: "online",
    });

    expect(next.presence["rio-remote"]?.label).toBe("Rio");
    expect(next.presence["rio-remote"]?.status).toBe("online");
  });

  it("queues and flushes reconnect replay work", () => {
    const viewer = createViewerIdentity("atlas");
    const base = createInitialWorkspaceState(viewer);
    const patch = createPatchEnvelope({
      clientId: viewer.clientId,
      clientLabel: viewer.label,
      entityType: "doc",
      entityId: "doc-1",
      field: "text",
      value: "Queued offline patch",
      createdAt: 30,
    });

    const queued = queuePatch(base, patch);
    const flushed = flushQueuedPatches(queued);

    expect(queued.queuedPatches).toHaveLength(1);
    expect(flushed.queuedPatches).toHaveLength(0);
    expect(flushed.activity[0]?.summary).toContain("Replayed queued patches");
  });

  it("raises and clears the conflict banner for overlapping edits", () => {
    const viewer = createViewerIdentity("atlas");
    const local = applyOptimisticPatch(
      createInitialWorkspaceState(viewer),
      createPatchEnvelope({
        clientId: viewer.clientId,
        clientLabel: viewer.label,
        entityType: "card",
        entityId: "card-1",
        field: "title",
        value: "Atlas version",
        createdAt: 100,
      }),
    );

    const conflicted = applyRemotePatch(
      local,
      createPatchEnvelope({
        clientId: "rio-remote",
        clientLabel: "Rio",
        entityType: "card",
        entityId: "card-1",
        field: "title",
        value: "Rio version",
        createdAt: 105,
      }),
    );

    expect(conflicted.conflicts.bannerVisible).toBe(true);
    expect(conflicted.conflicts.message).toContain("Conflict detected");

    const cleared = clearConflictBanner(conflicted);
    expect(cleared.conflicts.bannerVisible).toBe(false);
  });
});
