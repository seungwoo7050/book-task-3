import type {
  ChecklistItem,
  Invite,
  OnboardingMeta,
  Session,
  WorkspaceProfile,
} from "@/lib/types";

const STORAGE_KEYS = {
  session: "front-react:onboarding:session",
  profile: "front-react:onboarding:profile",
  invites: "front-react:onboarding:invites",
  checklist: "front-react:onboarding:checklist",
  meta: "front-react:onboarding:meta",
};

export const defaultWorkspaceProfile: WorkspaceProfile = {
  workspaceName: "",
  industry: "",
  region: "",
  teamSize: "",
  complianceEmail: "",
};

export const defaultChecklist: ChecklistItem[] = [
  { id: "profile", label: "Save workspace profile", completed: false },
  { id: "invite", label: "Invite at least one teammate", completed: false },
  { id: "review", label: "Review submission summary", completed: false },
];

export const defaultMeta: OnboardingMeta = {
  failNextSubmit: false,
  submittedAt: null,
};

function canUseStorage(): boolean {
  return typeof window !== "undefined";
}

function readJson<T>(key: string, fallback: T): T {
  if (!canUseStorage()) {
    return fallback;
  }

  const raw = window.localStorage.getItem(key);
  if (!raw) {
    return fallback;
  }

  try {
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

function writeJson<T>(key: string, value: T): void {
  if (!canUseStorage()) {
    return;
  }

  window.localStorage.setItem(key, JSON.stringify(value));
}

export function readSession(): Session | null {
  return readJson<Session | null>(STORAGE_KEYS.session, null);
}

export function writeSession(session: Session | null): void {
  if (!session) {
    if (canUseStorage()) {
      window.localStorage.removeItem(STORAGE_KEYS.session);
    }
    return;
  }

  writeJson(STORAGE_KEYS.session, session);
}

export function readWorkspaceProfile(): WorkspaceProfile {
  return readJson(STORAGE_KEYS.profile, defaultWorkspaceProfile);
}

export function writeWorkspaceProfile(profile: WorkspaceProfile): void {
  writeJson(STORAGE_KEYS.profile, profile);
}

export function readInvites(): Invite[] {
  return readJson<Invite[]>(STORAGE_KEYS.invites, []);
}

export function writeInvites(invites: Invite[]): void {
  writeJson(STORAGE_KEYS.invites, invites);
}

export function readChecklist(): ChecklistItem[] {
  return readJson<ChecklistItem[]>(STORAGE_KEYS.checklist, defaultChecklist);
}

export function writeChecklist(checklist: ChecklistItem[]): void {
  writeJson(STORAGE_KEYS.checklist, checklist);
}

export function readMeta(): OnboardingMeta {
  return readJson(STORAGE_KEYS.meta, defaultMeta);
}

export function writeMeta(meta: OnboardingMeta): void {
  writeJson(STORAGE_KEYS.meta, meta);
}

export function setFailNextSubmit(failNextSubmit: boolean): void {
  writeMeta({
    ...readMeta(),
    failNextSubmit,
  });
}

export function resetPortalState(): void {
  writeSession(null);
  writeWorkspaceProfile(defaultWorkspaceProfile);
  writeInvites([]);
  writeChecklist(defaultChecklist);
  writeMeta(defaultMeta);
}
