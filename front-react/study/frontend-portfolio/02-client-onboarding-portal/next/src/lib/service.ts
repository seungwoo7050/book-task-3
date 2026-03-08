import { canSubmitOnboarding } from "@/lib/guards";
import { inviteInputSchema, signInSchema, workspaceProfileSchema } from "@/lib/schemas";
import {
  readChecklist,
  readInvites,
  readMeta,
  readSession,
  readWorkspaceProfile,
  setFailNextSubmit,
  writeChecklist,
  writeInvites,
  writeMeta,
  writeSession,
  writeWorkspaceProfile,
} from "@/lib/storage";
import type {
  ChecklistItem,
  Invite,
  InviteInput,
  Session,
  SignInCredentials,
  SubmitResult,
  WorkspaceProfile,
} from "@/lib/types";

const LATENCY_MS = 80;

function wait(ms = LATENCY_MS): Promise<void> {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function createRetryableError(message: string): Error & { retryable: true } {
  const error = new Error(message) as Error & { retryable: true };
  error.retryable = true;
  return error;
}

export async function getSession(): Promise<Session | null> {
  await wait();
  return readSession();
}

export async function signIn(credentials: SignInCredentials): Promise<Session> {
  const parsed = signInSchema.parse(credentials);
  await wait();

  const session: Session = {
    userId: "client-01",
    name: parsed.email.split("@")[0].replace(/[._-]/g, " "),
    email: parsed.email,
  };

  writeSession(session);
  return session;
}

export async function signOut(): Promise<void> {
  await wait();
  writeSession(null);
}

export async function getWorkspaceProfile(): Promise<WorkspaceProfile> {
  await wait();
  return readWorkspaceProfile();
}

export async function saveWorkspaceProfile(
  patch: Partial<WorkspaceProfile>,
): Promise<WorkspaceProfile> {
  const nextProfile = workspaceProfileSchema.parse({
    ...readWorkspaceProfile(),
    ...patch,
  });

  await wait();
  writeWorkspaceProfile(nextProfile);
  return nextProfile;
}

export async function listInvites(): Promise<Invite[]> {
  await wait();
  return readInvites();
}

export async function createInvite(input: InviteInput): Promise<Invite> {
  const parsed = inviteInputSchema.parse(input);
  await wait();

  const nextInvite: Invite = {
    id: `invite-${Math.random().toString(36).slice(2, 8)}`,
    email: parsed.email,
    role: parsed.role,
    status: "pending",
  };

  writeInvites([...readInvites(), nextInvite]);
  return nextInvite;
}

export async function listChecklistItems(): Promise<ChecklistItem[]> {
  await wait();
  return readChecklist();
}

export async function completeChecklistItem(id: ChecklistItem["id"]): Promise<ChecklistItem[]> {
  await wait();

  const nextChecklist = readChecklist().map((item) =>
    item.id === id ? { ...item, completed: true } : item,
  );

  writeChecklist(nextChecklist);
  return nextChecklist;
}

export async function submitOnboarding(): Promise<SubmitResult> {
  await wait(120);

  const profile = readWorkspaceProfile();
  const invites = readInvites();
  const checklist = readChecklist();
  const meta = readMeta();

  if (meta.failNextSubmit) {
    setFailNextSubmit(false);
    throw createRetryableError("Submission failed. Retry after checking the review summary.");
  }

  if (!canSubmitOnboarding(profile, invites, checklist)) {
    throw new Error("Complete the workspace profile, invite list, and review checklist first.");
  }

  const submittedAt = new Date().toISOString();
  writeMeta({
    ...meta,
    submittedAt,
  });

  return {
    submittedAt,
    workspaceName: profile.workspaceName,
    inviteCount: invites.length,
  };
}
