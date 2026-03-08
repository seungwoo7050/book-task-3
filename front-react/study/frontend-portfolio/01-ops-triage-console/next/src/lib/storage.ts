import {
  defaultDemoRuntimeConfig,
  defaultSavedViews,
  storageKeys,
} from "@/lib/constants";
import { createSeedIssues } from "@/lib/demo-data";
import { type DemoRuntimeConfig, type Issue, type SavedView } from "@/lib/types";
import { cloneValue } from "@/lib/utils";

let memoryIssues = createSeedIssues();
let memoryRuntimeConfig = cloneValue(defaultDemoRuntimeConfig);

function canUseStorage(): boolean {
  return typeof window !== "undefined" && !!window.localStorage;
}

function readJson<T>(key: string): T | null {
  if (!canUseStorage()) {
    return null;
  }

  const value = window.localStorage.getItem(key);
  return value ? (JSON.parse(value) as T) : null;
}

function writeJson<T>(key: string, value: T): void {
  if (canUseStorage()) {
    window.localStorage.setItem(key, JSON.stringify(value));
  }
}

export function readIssues(): Issue[] {
  const storedIssues = readJson<Issue[]>(storageKeys.issues);
  if (storedIssues) {
    memoryIssues = cloneValue(storedIssues);
    return cloneValue(storedIssues);
  }

  if (canUseStorage()) {
    writeJson(storageKeys.issues, memoryIssues);
  }

  return cloneValue(memoryIssues);
}

export function writeIssues(issues: Issue[]): void {
  memoryIssues = cloneValue(issues);
  writeJson(storageKeys.issues, memoryIssues);
}

export function resetIssues(): Issue[] {
  const seeded = createSeedIssues();
  writeIssues(seeded);
  return seeded;
}

export function readRuntimeConfig(): DemoRuntimeConfig {
  const stored = readJson<DemoRuntimeConfig>(storageKeys.runtime);
  if (stored) {
    memoryRuntimeConfig = { ...memoryRuntimeConfig, ...stored };
    return cloneValue(memoryRuntimeConfig);
  }

  if (canUseStorage()) {
    writeJson(storageKeys.runtime, memoryRuntimeConfig);
  }

  return cloneValue(memoryRuntimeConfig);
}

export function writeRuntimeConfig(nextConfig: DemoRuntimeConfig): void {
  memoryRuntimeConfig = cloneValue(nextConfig);
  writeJson(storageKeys.runtime, memoryRuntimeConfig);
}

export function updateRuntimeConfig(
  patch: Partial<DemoRuntimeConfig>,
): DemoRuntimeConfig {
  const nextConfig = {
    ...readRuntimeConfig(),
    ...patch,
  };
  writeRuntimeConfig(nextConfig);
  return nextConfig;
}

export function resetRuntimeConfig(): DemoRuntimeConfig {
  writeRuntimeConfig(defaultDemoRuntimeConfig);
  return cloneValue(defaultDemoRuntimeConfig);
}

export function readSavedViews(): SavedView[] {
  return cloneValue(defaultSavedViews);
}

