"use client";

import { startTransition, useEffect, useEffectEvent, useRef, useState } from "react";
import { createViewerIdentity } from "@/lib/storage";
import {
  applyOptimisticPatch,
  applyPresencePing,
  applyRemotePatch,
  clearConflictBanner,
  createInitialWorkspaceState,
  createPatchEnvelope,
  flushQueuedPatches,
  markConnected,
  markDisconnected,
  queuePatch,
} from "@/lib/workspace-state";
import { BroadcastChannelTransport } from "@/lib/transport";
import type { CollabTransport, PresenceState } from "@/lib/types";

type Options = {
  viewerHint?: string;
  transport?: CollabTransport;
  disableHeartbeat?: boolean;
};

export function useRealtimeWorkspace(options: Options) {
  const [viewer] = useState(() => createViewerIdentity(options.viewerHint));
  const [transport] = useState(
    () => options.transport ?? new BroadcastChannelTransport(),
  );
  const [state, setState] = useState(() => createInitialWorkspaceState(viewer));
  const stateRef = useRef(state);

  useEffect(() => {
    stateRef.current = state;
  }, [state]);

  const handleTransportEvent = useEffectEvent((event: {
    type: "patch" | "presence";
    patch?: Parameters<typeof applyRemotePatch>[1];
    presence?: PresenceState;
  }) => {
    if (event.type === "patch" && event.patch) {
      startTransition(() => {
        setState((current) => applyRemotePatch(current, event.patch!));
      });
      return;
    }
    if (event.type === "presence" && event.presence) {
      startTransition(() => {
        setState((current) => applyPresencePing(current, event.presence!));
      });
    }
  });

  useEffect(() => {
    const unsubscribe = transport.subscribe(handleTransportEvent);
    transport.connect();

    const onlinePresence = {
      ...viewer,
      status: "online" as const,
      lastSeenAt: Date.now(),
    };
    transport.sendPresence(onlinePresence);
    startTransition(() => {
      setState((current) =>
        markConnected(applyPresencePing(current, onlinePresence)),
      );
    });

    return () => {
      if (transport.isConnected()) {
        transport.sendPresence({
          ...viewer,
          status: "offline",
          lastSeenAt: Date.now(),
        });
      }
      unsubscribe();
      transport.destroy();
    };
  }, [transport, viewer]);

  useEffect(() => {
    if (options.disableHeartbeat || typeof window === "undefined") {
      return;
    }
    const heartbeat = window.setInterval(() => {
      if (!transport.isConnected()) {
        return;
      }
      const ping = {
        ...viewer,
        status: "online" as const,
        lastSeenAt: Date.now(),
      };
      transport.sendPresence(ping);
      startTransition(() => {
        setState((current) => applyPresencePing(current, ping));
      });
    }, 2_500);
    return () => {
      window.clearInterval(heartbeat);
    };
  }, [options.disableHeartbeat, transport, viewer]);

  function sendPatch(
    entityType: "card" | "doc",
    entityId: string,
    field: "title" | "text",
    value: string,
  ) {
    const patch = createPatchEnvelope({
      clientId: viewer.clientId,
      clientLabel: viewer.label,
      entityType,
      entityId,
      field,
      value,
      createdAt: Date.now(),
    });

    startTransition(() => {
      setState((current) => {
        const optimistic = applyOptimisticPatch(current, patch);
        if (!transport.isConnected()) {
          return queuePatch(markDisconnected(optimistic), patch);
        }
        return optimistic;
      });
    });

    if (transport.isConnected()) {
      transport.sendPatch(patch);
    }
  }

  function disconnect() {
    if (transport.isConnected()) {
      transport.sendPresence({
        ...viewer,
        status: "offline",
        lastSeenAt: Date.now(),
      });
    }
    transport.disconnect();
    startTransition(() => {
      setState((current) =>
        markDisconnected(
          applyPresencePing(current, {
            ...viewer,
            status: "offline",
            lastSeenAt: Date.now(),
          }),
        ),
      );
    });
  }

  function reconnect() {
    transport.connect();
    const onlinePresence = {
      ...viewer,
      status: "online" as const,
      lastSeenAt: Date.now(),
    };
    transport.sendPresence(onlinePresence);
    for (const patch of stateRef.current.queuedPatches) {
      transport.sendPatch(patch);
    }
    startTransition(() => {
      setState((current) =>
        flushQueuedPatches(
          markConnected(applyPresencePing(current, onlinePresence)),
        ),
      );
    });
  }

  return {
    state,
    viewer,
    setCardTitle(cardId: string, value: string) {
      sendPatch("card", cardId, "title", value);
    },
    setDocText(docId: string, value: string) {
      sendPatch("doc", docId, "text", value);
    },
    disconnect,
    reconnect,
    dismissConflict() {
      startTransition(() => {
        setState((current) => clearConflictBanner(current));
      });
    },
  };
}
