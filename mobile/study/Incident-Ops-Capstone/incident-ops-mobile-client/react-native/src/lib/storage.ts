import AsyncStorage from '@react-native-async-storage/async-storage';

import type { AppSession, AppSettings, QueuedMutation } from './types';
import { DEFAULT_BASE_URL } from './types';

const STORAGE_KEYS = {
  session: 'incident-ops-mobile-client/session',
  settings: 'incident-ops-mobile-client/settings',
  outbox: 'incident-ops-mobile-client/outbox',
  lastEventId: 'incident-ops-mobile-client/last-event-id',
} as const;

export interface StorageAdapter {
  getItem(key: string): Promise<string | null>;
  setItem(key: string, value: string): Promise<void>;
  removeItem(key: string): Promise<void>;
}

export const appStorage: StorageAdapter = AsyncStorage;

export const defaultSettings: AppSettings = {
  baseUrl: DEFAULT_BASE_URL,
};

async function readJson<T>(
  storage: StorageAdapter,
  key: string,
  fallback: T,
): Promise<T> {
  const raw = await storage.getItem(key);

  if (!raw) {
    return fallback;
  }

  try {
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

async function saveJson<T>(
  storage: StorageAdapter,
  key: string,
  value: T,
): Promise<void> {
  await storage.setItem(key, JSON.stringify(value));
}

export async function loadSession(
  storage: StorageAdapter = appStorage,
): Promise<AppSession | null> {
  return readJson<AppSession | null>(storage, STORAGE_KEYS.session, null);
}

export async function saveSession(
  session: AppSession | null,
  storage: StorageAdapter = appStorage,
): Promise<void> {
  if (!session) {
    await storage.removeItem(STORAGE_KEYS.session);
    return;
  }

  await saveJson(storage, STORAGE_KEYS.session, session);
}

export async function loadSettings(
  storage: StorageAdapter = appStorage,
): Promise<AppSettings> {
  return readJson<AppSettings>(storage, STORAGE_KEYS.settings, defaultSettings);
}

export async function saveSettings(
  settings: AppSettings,
  storage: StorageAdapter = appStorage,
): Promise<void> {
  await saveJson(storage, STORAGE_KEYS.settings, settings);
}

export async function loadOutbox(
  storage: StorageAdapter = appStorage,
): Promise<QueuedMutation[]> {
  return readJson<QueuedMutation[]>(storage, STORAGE_KEYS.outbox, []);
}

export async function saveOutbox(
  outbox: QueuedMutation[],
  storage: StorageAdapter = appStorage,
): Promise<void> {
  await saveJson(storage, STORAGE_KEYS.outbox, outbox);
}

export async function loadLastEventId(
  storage: StorageAdapter = appStorage,
): Promise<number> {
  const value = await readJson<number>(storage, STORAGE_KEYS.lastEventId, 0);
  return Number.isFinite(value) ? value : 0;
}

export async function saveLastEventId(
  lastEventId: number,
  storage: StorageAdapter = appStorage,
): Promise<void> {
  await saveJson(storage, STORAGE_KEYS.lastEventId, lastEventId);
}

export function createMemoryStorage(
  initial: Record<string, string> = {},
): StorageAdapter {
  const store = new Map(Object.entries(initial));

  return {
    async getItem(key: string) {
      return store.get(key) ?? null;
    },
    async setItem(key: string, value: string) {
      store.set(key, value);
    },
    async removeItem(key: string) {
      store.delete(key);
    },
  };
}
