export type OnboardingStep = "workspace" | "invites" | "review";

export interface Session {
  userId: string;
  name: string;
  email: string;
}

export interface SignInCredentials {
  email: string;
  password: string;
}

export interface WorkspaceProfile {
  workspaceName: string;
  industry: string;
  region: string;
  teamSize: string;
  complianceEmail: string;
}

export interface Invite {
  id: string;
  email: string;
  role: "Admin" | "Billing" | "Collaborator";
  status: "pending";
}

export interface InviteInput {
  email: string;
  role: Invite["role"];
}

export interface ChecklistItem {
  id: "profile" | "invite" | "review";
  label: string;
  completed: boolean;
}

export interface OnboardingDraft {
  profile: WorkspaceProfile;
  invites: Invite[];
}

export interface SubmitResult {
  submittedAt: string;
  workspaceName: string;
  inviteCount: number;
}

export interface OnboardingMeta {
  failNextSubmit: boolean;
  submittedAt: string | null;
}
