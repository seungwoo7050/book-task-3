import type {
  ChecklistItem,
  Invite,
  OnboardingStep,
  WorkspaceProfile,
} from "@/lib/types";

export const onboardingSteps: OnboardingStep[] = ["workspace", "invites", "review"];

export function coerceStep(value: string | null | undefined): OnboardingStep {
  if (value === "workspace" || value === "invites" || value === "review") {
    return value;
  }

  return "workspace";
}

export function isWorkspaceReady(profile: WorkspaceProfile): boolean {
  return Boolean(
    profile.workspaceName.trim() &&
      profile.industry.trim() &&
      profile.region.trim() &&
      profile.teamSize.trim() &&
      profile.complianceEmail.trim(),
  );
}

export function isChecklistComplete(checklist: ChecklistItem[], id: ChecklistItem["id"]): boolean {
  return checklist.some((item) => item.id === id && item.completed);
}

export function canSubmitOnboarding(
  profile: WorkspaceProfile,
  invites: Invite[],
  checklist: ChecklistItem[],
): boolean {
  return (
    isWorkspaceReady(profile) &&
    invites.length > 0 &&
    isChecklistComplete(checklist, "profile") &&
    isChecklistComplete(checklist, "invite") &&
    isChecklistComplete(checklist, "review")
  );
}
