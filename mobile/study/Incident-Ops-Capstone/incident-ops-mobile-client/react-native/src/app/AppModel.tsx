import React, { createContext, useContext, useEffect, useRef, useState } from 'react';
import { useInfiniteQuery, useQuery, useQueryClient } from '@tanstack/react-query';

import type {
  ApprovalDecision,
  CreateIncidentRequest,
  QueueAction,
  RequestResolutionBody,
} from '../contracts';
import {
  acknowledgeIncidentRequest,
  createIncidentRequest,
  decideApprovalRequest,
  listAudit,
  listIncidents,
  loginRequest,
  normalizeBaseUrl,
  requestResolutionRequest,
} from '../lib/api';
import { auditKeys, incidentKeys } from '../lib/queries';
import { openIncidentStream } from '../lib/stream';
import {
  buildIncidentList,
  createQueuedMutation,
  markQueuedMutationFailed,
  markQueuedMutationSynced,
  retryQueuedMutation,
} from '../lib/outbox';
import {
  appStorage,
  defaultSettings,
  loadLastEventId,
  loadOutbox,
  loadSession,
  loadSettings,
  saveLastEventId,
  saveOutbox,
  saveSession,
  saveSettings,
} from '../lib/storage';
import { fetchCurrentConnection, subscribeToConnectivity } from '../lib/connectivity';
import type {
  AppSession,
  AppSettings,
  ConnectionState,
  IncidentListItem,
  QueuedMutation,
  StreamStatus,
} from '../lib/types';
import { DEFAULT_BASE_URL } from '../lib/types';

type BootstrapState = 'loading' | 'ready';

interface AppModelValue {
  bootstrapState: BootstrapState;
  settings: AppSettings;
  session: AppSession | null;
  connection: ConnectionState;
  streamStatus: StreamStatus;
  outbox: QueuedMutation[];
  lastEventId: number;
  login: (input: {
    userId: string;
    role: 'REPORTER' | 'OPERATOR' | 'APPROVER';
    baseUrl: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
  updateBaseUrl: (baseUrl: string) => Promise<void>;
  queueCreateIncident: (payload: CreateIncidentRequest) => void;
  queueAckIncident: (incidentId: string) => void;
  queueRequestResolution: (
    incidentId: string,
    body: RequestResolutionBody,
  ) => void;
  queueApprovalDecision: (input: {
    incidentId: string;
    approvalId: string;
    decision: ApprovalDecision;
    note?: string;
  }) => void;
  retryFailedMutation: (jobId: string) => void;
  clearSyncedMutations: () => void;
  flushPendingMutations: () => Promise<void>;
}

const AppModelContext = createContext<AppModelValue | null>(null);

function createId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function defaultConnectionState(): ConnectionState {
  return {
    isConnected: true,
    typeLabel: 'unknown',
    updatedAt: new Date().toISOString(),
  };
}

function getIncidentId(payload: Record<string, unknown>): string | null {
  const incidentId = payload.incidentId;
  return typeof incidentId === 'string' ? incidentId : null;
}

async function executeQueuedMutation(input: {
  item: QueuedMutation;
  session: AppSession;
  settings: AppSettings;
}): Promise<void> {
  const { item, session, settings } = input;

  switch (item.action) {
    case 'POST /incidents':
      await createIncidentRequest({
        baseUrl: settings.baseUrl,
        token: session.token,
        idempotencyKey: item.idempotencyKey,
        body: item.payload as unknown as CreateIncidentRequest,
      });
      return;
    case 'POST /incidents/:id/ack': {
      const incidentId = getIncidentId(item.payload);
      if (!incidentId) {
        throw new Error('missing incident id for ack');
      }

      await acknowledgeIncidentRequest({
        baseUrl: settings.baseUrl,
        token: session.token,
        idempotencyKey: item.idempotencyKey,
        incidentId,
      });
      return;
    }
    case 'POST /incidents/:id/request-resolution': {
      const incidentId = getIncidentId(item.payload);
      const reason = item.payload.reason;

      if (!incidentId || typeof reason !== 'string') {
        throw new Error('missing request-resolution payload');
      }

      await requestResolutionRequest({
        baseUrl: settings.baseUrl,
        token: session.token,
        idempotencyKey: item.idempotencyKey,
        incidentId,
        body: { reason },
      });
      return;
    }
    case 'POST /approvals/:id/decision': {
      const approvalId = item.payload.approvalId;
      const decision = item.payload.decision;
      const note = item.payload.note;

      if (
        typeof approvalId !== 'string' ||
        (decision !== 'APPROVE' && decision !== 'REJECT')
      ) {
        throw new Error('missing approval decision payload');
      }

      await decideApprovalRequest({
        baseUrl: settings.baseUrl,
        token: session.token,
        idempotencyKey: item.idempotencyKey,
        approvalId,
        decision,
        note: typeof note === 'string' ? note : undefined,
      });
      return;
    }
  }
}

export function AppModelProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const queryClient = useQueryClient();
  const [bootstrapState, setBootstrapState] = useState<BootstrapState>('loading');
  const [settings, setSettings] = useState<AppSettings>(defaultSettings);
  const [session, setSession] = useState<AppSession | null>(null);
  const [outbox, setOutbox] = useState<QueuedMutation[]>([]);
  const [lastEventId, setLastEventId] = useState(0);
  const [connection, setConnection] = useState<ConnectionState>(
    defaultConnectionState(),
  );
  const [streamStatus, setStreamStatus] = useState<StreamStatus>('idle');

  const flushInFlightRef = useRef(false);
  const lastEventIdRef = useRef(0);

  useEffect(() => {
    lastEventIdRef.current = lastEventId;
  }, [lastEventId]);

  useEffect(() => {
    let active = true;

    const bootstrap = async (): Promise<void> => {
      const [savedSettings, savedSession, savedOutbox, savedLastEventId] =
        await Promise.all([
          loadSettings(appStorage),
          loadSession(appStorage),
          loadOutbox(appStorage),
          loadLastEventId(appStorage),
        ]);

      if (!active) {
        return;
      }

      setSettings(savedSettings);
      setSession(savedSession);
      setOutbox(savedOutbox);
      setLastEventId(savedLastEventId);
      lastEventIdRef.current = savedLastEventId;
      setBootstrapState('ready');
    };

    void bootstrap();

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    const unsubscribe = subscribeToConnectivity(setConnection);
    void fetchCurrentConnection().then(setConnection);

    return unsubscribe;
  }, []);

  useEffect(() => {
    if (bootstrapState !== 'ready') {
      return;
    }

    void saveSettings(settings, appStorage);
  }, [bootstrapState, settings]);

  useEffect(() => {
    if (bootstrapState !== 'ready') {
      return;
    }

    void saveSession(session, appStorage);
  }, [bootstrapState, session]);

  useEffect(() => {
    if (bootstrapState !== 'ready') {
      return;
    }

    void saveOutbox(outbox, appStorage);
  }, [bootstrapState, outbox]);

  useEffect(() => {
    if (bootstrapState !== 'ready') {
      return;
    }

    void saveLastEventId(lastEventId, appStorage);
  }, [bootstrapState, lastEventId]);

  async function login(input: {
    userId: string;
    role: 'REPORTER' | 'OPERATOR' | 'APPROVER';
    baseUrl: string;
  }): Promise<void> {
    const baseUrl = normalizeBaseUrl(input.baseUrl || DEFAULT_BASE_URL);
    const response = await loginRequest({
      baseUrl,
      userId: input.userId,
      role: input.role,
    });

    setSettings({ baseUrl });
    setSession(response);
    setLastEventId(0);
    lastEventIdRef.current = 0;
    queryClient.clear();
  }

  async function logout(): Promise<void> {
    setSession(null);
    setOutbox([]);
    setLastEventId(0);
    lastEventIdRef.current = 0;
    queryClient.clear();
  }

  async function updateBaseUrl(baseUrl: string): Promise<void> {
    const normalized = normalizeBaseUrl(baseUrl || DEFAULT_BASE_URL);
    setSettings({ baseUrl: normalized });
    setLastEventId(0);
    lastEventIdRef.current = 0;
    queryClient.clear();
  }

  function pushMutation(
    action: QueueAction,
    payload: Record<string, unknown>,
    label: string,
  ): void {
    const next = createQueuedMutation({
      action,
      payload,
      label,
      createdAt: new Date().toISOString(),
      idGenerator: createId,
    });

    setOutbox(current => [next, ...current]);
  }

  function queueCreateIncident(payload: CreateIncidentRequest): void {
    pushMutation(
      'POST /incidents',
      payload as unknown as Record<string, unknown>,
      `Create ${payload.title}`,
    );
  }

  function queueAckIncident(incidentId: string): void {
    pushMutation(
      'POST /incidents/:id/ack',
      { incidentId },
      `Ack ${incidentId.slice(0, 8)}`,
    );
  }

  function queueRequestResolution(
    incidentId: string,
    body: RequestResolutionBody,
  ): void {
    pushMutation(
      'POST /incidents/:id/request-resolution',
      { incidentId, reason: body.reason },
      `Request resolution ${incidentId.slice(0, 8)}`,
    );
  }

  function queueApprovalDecision(input: {
    incidentId: string;
    approvalId: string;
    decision: ApprovalDecision;
    note?: string;
  }): void {
    pushMutation(
      'POST /approvals/:id/decision',
      {
        incidentId: input.incidentId,
        approvalId: input.approvalId,
        decision: input.decision,
        note: input.note,
      },
      `${input.decision} ${input.incidentId.slice(0, 8)}`,
    );
  }

  function retryFailedMutation(jobId: string): void {
    setOutbox(current =>
      current.map(item => (item.id === jobId ? retryQueuedMutation(item) : item)),
    );
  }

  function clearSyncedMutations(): void {
    setOutbox(current => current.filter(item => item.state !== 'synced'));
  }

  async function flushPendingMutations(): Promise<void> {
    if (flushInFlightRef.current || !session || !connection.isConnected) {
      return;
    }

    flushInFlightRef.current = true;
    let nextOutbox = outbox;
    let shouldRefreshIncidents = false;
    let shouldRefreshAudit = false;

    try {
      for (const item of nextOutbox) {
        if (item.state !== 'pending') {
          continue;
        }

        try {
          await executeQueuedMutation({
            item,
            session,
            settings,
          });
          nextOutbox = nextOutbox.map(current =>
            current.id === item.id ? markQueuedMutationSynced(current) : current,
          );
          shouldRefreshIncidents = true;
          shouldRefreshAudit = true;
        } catch (error) {
          nextOutbox = nextOutbox.map(current =>
            current.id === item.id
              ? markQueuedMutationFailed(current, error)
              : current,
          );
        }

        setOutbox(nextOutbox);
      }
    } finally {
      flushInFlightRef.current = false;
    }

    if (shouldRefreshIncidents) {
      await queryClient.invalidateQueries({ queryKey: incidentKeys.all });
    }

    if (shouldRefreshAudit) {
      await queryClient.invalidateQueries({ queryKey: auditKeys.all });
    }
  }

  useEffect(() => {
    if (
      bootstrapState !== 'ready' ||
      !session ||
      !connection.isConnected ||
      !outbox.some(item => item.state === 'pending')
    ) {
      return;
    }

    void flushPendingMutations();
  }, [bootstrapState, connection.isConnected, outbox, session]);

  useEffect(() => {
    if (bootstrapState !== 'ready' || !session || !connection.isConnected) {
      setStreamStatus('idle');
      return;
    }

    setStreamStatus('connecting');

    const disconnect = openIncidentStream({
      baseUrl: settings.baseUrl,
      lastEventId: lastEventIdRef.current,
      onOpen: () => {
        setStreamStatus('live');
      },
      onClose: () => {
        setStreamStatus('idle');
      },
      onError: () => {
        setStreamStatus('error');
      },
      onEvent: event => {
        lastEventIdRef.current = Math.max(lastEventIdRef.current, event.eventId);
        setLastEventId(current => Math.max(current, event.eventId));
        void queryClient.invalidateQueries({ queryKey: incidentKeys.all });

        if (event.type !== 'incident.created') {
          void queryClient.invalidateQueries({ queryKey: auditKeys.all });
        }
      },
    });

    return disconnect;
  }, [bootstrapState, connection.isConnected, queryClient, session, settings.baseUrl]);

  return (
    <AppModelContext.Provider
      value={{
        bootstrapState,
        settings,
        session,
        connection,
        streamStatus,
        outbox,
        lastEventId,
        login,
        logout,
        updateBaseUrl,
        queueCreateIncident,
        queueAckIncident,
        queueRequestResolution,
        queueApprovalDecision,
        retryFailedMutation,
        clearSyncedMutations,
        flushPendingMutations,
      }}>
      {children}
    </AppModelContext.Provider>
  );
}

export function useAppModel(): AppModelValue {
  const context = useContext(AppModelContext);
  if (!context) {
    throw new Error('useAppModel must be used within AppModelProvider');
  }

  return context;
}

export function useIncidentItems(): ReturnType<typeof useInfiniteQuery> & {
  items: IncidentListItem[];
} {
  const { bootstrapState, session, settings, outbox } = useAppModel();
  const query = useInfiniteQuery({
    queryKey: incidentKeys.feed(settings.baseUrl, session?.actor.userId ?? 'guest'),
    enabled: bootstrapState === 'ready' && Boolean(session),
    initialPageParam: null as string | null,
    queryFn: ({ pageParam }) =>
      listIncidents({
        baseUrl: settings.baseUrl,
        token: session!.token,
        cursor: pageParam,
      }),
    getNextPageParam: lastPage => lastPage.nextCursor,
    retry: false,
    staleTime: 10_000,
  });

  const incidents = query.data?.pages.flatMap(page => page.incidents) ?? [];

  return {
    ...query,
    items: buildIncidentList(incidents, outbox),
  };
}

export function usePendingApprovalItems(): ReturnType<typeof useIncidentItems> & {
  items: IncidentListItem[];
} {
  const feed = useIncidentItems();
  return {
    ...feed,
    items: feed.items.filter(item => item.status === 'RESOLUTION_PENDING'),
  };
}

export function useIncidentAudit(incidentId: string | undefined) {
  const { bootstrapState, session, settings } = useAppModel();

  return useQuery({
    queryKey: auditKeys.detail(settings.baseUrl, incidentId ?? 'none'),
    enabled:
      bootstrapState === 'ready' &&
      Boolean(session) &&
      Boolean(incidentId) &&
      !incidentId?.startsWith('local-'),
    queryFn: () =>
      listAudit({
        baseUrl: settings.baseUrl,
        token: session!.token,
        incidentId: incidentId!,
      }),
    retry: false,
  });
}
