"use client";

import { useDeferredValue } from "react";
import type { CollabTransport } from "@/lib/types";
import { useRealtimeWorkspace } from "@/hooks/use-realtime-workspace";

type WorkspaceShellProps = {
  viewerHint?: string;
  transport?: CollabTransport;
  disableHeartbeat?: boolean;
};

function relativeTime(timestamp: number) {
  const delta = Math.max(0, Date.now() - timestamp);
  const seconds = Math.floor(delta / 1000);
  if (seconds < 60) {
    return `${seconds}s ago`;
  }
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) {
    return `${minutes}m ago`;
  }
  return `${Math.floor(minutes / 60)}h ago`;
}

export function WorkspaceShell({
  viewerHint,
  transport,
  disableHeartbeat = false,
}: WorkspaceShellProps) {
  const {
    state,
    viewer,
    setCardTitle,
    setDocText,
    disconnect,
    reconnect,
    dismissConflict,
  } = useRealtimeWorkspace({
    viewerHint,
    transport,
    disableHeartbeat,
  });
  const deferredActivity = useDeferredValue(state.activity);
  const presence = Object.values(state.presence).sort((left, right) =>
    left.label.localeCompare(right.label),
  );

  return (
    <main className="workspace-page">
      <div className="workspace-shell">
        <section className="hero">
          <div className="hero-top">
            <div>
              <p className="eyebrow">Frontend Portfolio Capstone</p>
              <h1>Realtime collab without hiding the tradeoffs.</h1>
            </div>
            <div className="action-row">
              <button
                className="secondary"
                data-testid="disconnect-button"
                onClick={disconnect}
                type="button"
              >
                Disconnect
              </button>
              <button
                data-testid="reconnect-button"
                onClick={reconnect}
                type="button"
              >
                Reconnect
              </button>
            </div>
          </div>
          <p className="hero-copy">
            Shared cards and document blocks travel over a same-origin mock
            transport. The point is not to hide the limitations, but to make
            optimistic patches, reconnect replay, and conflict surfaces visible
            enough that another engineer can explain the state model from the UI
            alone.
          </p>
          <div className="status-row">
            <div className="status-card">
              <span className="muted">Viewer</span>
              <strong>{viewer.label}</strong>
            </div>
            <div className="status-card">
              <span className="muted">Connection</span>
              <strong
                className={`status-pill ${
                  state.connection === "connected" ? "" : "offline"
                }`}
                data-testid="connection-status"
              >
                {state.connection === "connected" ? "Connected" : "Disconnected"}
              </strong>
            </div>
            <div className="status-card">
              <span className="muted">Queued patches</span>
              <strong data-testid="queued-count">{state.queuedPatches.length}</strong>
            </div>
            <div className="status-card">
              <span className="muted">Conflicts</span>
              <strong>{state.conflicts.entityKeys.length}</strong>
            </div>
          </div>
          <div className="metrics-row">
            <div className="metric">
              <span className="metric-label">Shared cards</span>
              <strong>{state.cards.length}</strong>
            </div>
            <div className="metric">
              <span className="metric-label">Doc blocks</span>
              <strong>{state.docs.length}</strong>
            </div>
            <div className="metric">
              <span className="metric-label">Visible collaborators</span>
              <strong data-testid="presence-count">{presence.length}</strong>
            </div>
          </div>
        </section>

        {state.conflicts.bannerVisible ? (
          <section className="banner" data-testid="conflict-banner" role="alert">
            <p>{state.conflicts.message}</p>
            <button onClick={dismissConflict} type="button">
              Dismiss
            </button>
          </section>
        ) : null}

        <section className="workspace-grid">
          <div className="stack">
            <article className="surface">
              <div className="surface-header">
                <div>
                  <h2>Shared board cards</h2>
                  <p className="muted">
                    Edit the same entity from two tabs to force a visible
                    conflict banner.
                  </p>
                </div>
                <span className="subtle-tag">Optimistic board</span>
              </div>
              <div className="stack">
                {state.cards.map((card) => (
                  <div className="card-tile" key={card.id}>
                    <div className="card-meta">
                      <span className="card-status">{card.lane}</span>
                      <span className="muted">
                        updated by {card.updatedBy}
                      </span>
                    </div>
                    <input
                      aria-label={`Card ${card.id} title`}
                      className="text-field"
                      data-testid={`card-input-${card.id}`}
                      onChange={(event) =>
                        setCardTitle(card.id, event.currentTarget.value)
                      }
                      value={card.title}
                    />
                  </div>
                ))}
              </div>
            </article>

            <article className="surface">
              <div className="surface-header">
                <div>
                  <h2>Shared doc blocks</h2>
                  <p className="muted">
                    The board and document use the same patch envelope and
                    reconnect flow.
                  </p>
                </div>
                <span className="subtle-tag">Unified patch shape</span>
              </div>
              <div className="stack">
                {state.docs.map((doc) => (
                  <div className="doc-tile" key={doc.id}>
                    <div className="doc-meta">
                      <span className="muted">{doc.id}</span>
                      <span className="muted">last by {doc.updatedBy}</span>
                    </div>
                    <textarea
                      aria-label={`Doc ${doc.id} text`}
                      className="text-area"
                      data-testid={`doc-input-${doc.id}`}
                      onChange={(event) =>
                        setDocText(doc.id, event.currentTarget.value)
                      }
                      value={doc.text}
                    />
                  </div>
                ))}
              </div>
            </article>
          </div>

          <article className="surface">
            <div className="surface-header">
              <div>
                <h2>Presence</h2>
                <p className="muted">
                  Same-origin collaborators announce themselves over the mock
                  transport.
                </p>
              </div>
              <span className="subtle-tag">Heartbeat</span>
            </div>
            <ul className="presence-list" data-testid="presence-list">
              {presence.map((person) => (
                <li className="presence-chip" key={person.clientId}>
                  <span className="presence-name">
                    <span
                      className="presence-dot"
                      style={{ background: person.color }}
                    />
                    <strong>{person.label}</strong>
                  </span>
                  <span className="presence-state">{person.status}</span>
                </li>
              ))}
            </ul>
          </article>

          <aside className="activity-panel">
            <div className="activity-header">
              <div>
                <h2>Activity log</h2>
                <p className="muted">
                  Recent local, remote, and system events stay explicit.
                </p>
              </div>
            </div>
            <ul className="activity-list" data-testid="activity-log">
              {deferredActivity.map((item) => (
                <li className="activity-item" key={item.id}>
                  <strong>{item.actor}</strong>
                  <div>{item.summary}</div>
                  <div className="activity-timestamp">
                    {relativeTime(item.createdAt)}
                  </div>
                </li>
              ))}
            </ul>
          </aside>
        </section>
      </div>
    </main>
  );
}
