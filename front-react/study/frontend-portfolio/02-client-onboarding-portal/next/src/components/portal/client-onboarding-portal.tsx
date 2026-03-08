"use client";

import Link from "next/link";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";
import { canSubmitOnboarding, onboardingSteps } from "@/lib/guards";
import { inviteInputSchema, workspaceProfileSchema, type InviteInputSchema, type WorkspaceProfileSchema } from "@/lib/schemas";
import {
  completeChecklistItem,
  createInvite,
  getSession,
  getWorkspaceProfile,
  listChecklistItems,
  listInvites,
  saveWorkspaceProfile,
  signOut,
  submitOnboarding,
} from "@/lib/service";
import { defaultWorkspaceProfile, setFailNextSubmit } from "@/lib/storage";
import type { Invite, OnboardingStep, SubmitResult } from "@/lib/types";

interface ClientOnboardingPortalProps {
  step: OnboardingStep;
  onStepChange(step: OnboardingStep): void;
}

const stepTitles: Record<OnboardingStep, string> = {
  workspace: "Workspace profile",
  invites: "Team invites",
  review: "Review and submit",
};

export function ClientOnboardingPortal({
  step,
  onStepChange,
}: ClientOnboardingPortalProps) {
  const queryClient = useQueryClient();
  const [saveMessage, setSaveMessage] = useState("");
  const [submitResult, setSubmitResult] = useState<SubmitResult | null>(null);
  const [submitError, setSubmitError] = useState("");
  const [shouldFailNextSubmit, setShouldFailNextSubmit] = useState(false);

  const sessionQuery = useQuery({
    queryKey: ["session"],
    queryFn: getSession,
  });
  const profileQuery = useQuery({
    enabled: Boolean(sessionQuery.data),
    queryKey: ["workspace-profile"],
    queryFn: getWorkspaceProfile,
  });
  const invitesQuery = useQuery({
    enabled: Boolean(sessionQuery.data),
    queryKey: ["invites"],
    queryFn: listInvites,
  });
  const checklistQuery = useQuery({
    enabled: Boolean(sessionQuery.data),
    queryKey: ["checklist"],
    queryFn: listChecklistItems,
  });

  const workspaceForm = useForm<WorkspaceProfileSchema>({
    resolver: zodResolver(workspaceProfileSchema),
    defaultValues: defaultWorkspaceProfile,
  });
  const inviteForm = useForm<InviteInputSchema>({
    resolver: zodResolver(inviteInputSchema),
    defaultValues: {
      email: "",
      role: "Collaborator",
    },
  });

  useEffect(() => {
    if (profileQuery.data) {
      workspaceForm.reset(profileQuery.data);
    }
  }, [profileQuery.data, workspaceForm]);

  const profile = profileQuery.data ?? defaultWorkspaceProfile;
  const invites = invitesQuery.data ?? [];
  const checklist = checklistQuery.data ?? [];
  const canSubmit = useMemo(
    () => canSubmitOnboarding(profile, invites, checklist),
    [profile, invites, checklist],
  );

  const refreshPortalData = async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ["workspace-profile"] }),
      queryClient.invalidateQueries({ queryKey: ["invites"] }),
      queryClient.invalidateQueries({ queryKey: ["checklist"] }),
      queryClient.invalidateQueries({ queryKey: ["session"] }),
    ]);
  };

  const saveProfileMutation = useMutation({
    mutationFn: async (values: WorkspaceProfileSchema) => {
      const nextProfile = await saveWorkspaceProfile(values);
      await completeChecklistItem("profile");
      return nextProfile;
    },
    onSuccess: async () => {
      setSaveMessage("Draft saved to the local demo workspace.");
      await refreshPortalData();
    },
  });

  const addInviteMutation = useMutation({
    mutationFn: async (values: InviteInputSchema) => {
      const invite = await createInvite(values);
      await completeChecklistItem("invite");
      return invite;
    },
    onSuccess: async () => {
      inviteForm.reset({ email: "", role: "Collaborator" });
      await refreshPortalData();
    },
  });

  const completeReviewMutation = useMutation({
    mutationFn: () => completeChecklistItem("review"),
    onSuccess: refreshPortalData,
  });

  const submitMutation = useMutation({
    mutationFn: async () => {
      if (shouldFailNextSubmit) {
        setFailNextSubmit(true);
      }
      return submitOnboarding();
    },
    onSuccess: async (result) => {
      setSubmitResult(result);
      setSubmitError("");
      setShouldFailNextSubmit(false);
      await refreshPortalData();
    },
    onError: (error: Error) => {
      setSubmitError(error.message);
      setSubmitResult(null);
      setShouldFailNextSubmit(false);
    },
  });

  const signOutMutation = useMutation({
    mutationFn: signOut,
    onSuccess: refreshPortalData,
  });

  const selectedInviteCount = invites.length;

  if (sessionQuery.isLoading) {
    return <main className="mx-auto min-h-screen max-w-6xl px-4 py-10">Loading session...</main>;
  }

  if (!sessionQuery.data) {
    return (
      <main className="mx-auto flex min-h-screen max-w-4xl flex-col justify-center px-4 py-10 sm:px-6">
        <section className="rounded-[2rem] border border-white/80 bg-[rgba(255,251,245,0.92)] p-8 shadow-[0_30px_80px_-60px_rgba(24,34,24,0.65)]">
          <p className="font-mono text-xs uppercase tracking-[0.28em] text-stone-500">
            Route Guard
          </p>
          <h1 className="mt-3 text-3xl font-semibold tracking-[-0.04em] text-stone-950">
            Sign in before opening the onboarding flow
          </h1>
          <p className="mt-4 text-sm leading-7 text-stone-600">
            This route is intentionally protected so the demo can show session gating and
            direct-link fallback behavior.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href="/"
              className="rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white"
            >
              Back to sign-in
            </Link>
            <Link
              href="/case-study"
              className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
            >
              Open case study
            </Link>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <header className="rounded-[2rem] border border-white/80 bg-[rgba(255,251,245,0.92)] px-6 py-6 shadow-[0_30px_80px_-60px_rgba(24,34,24,0.62)] backdrop-blur">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl">
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-stone-500">
              Customer onboarding
            </p>
            <h1 className="mt-3 text-4xl font-semibold tracking-[-0.05em] text-stone-950">
              Guide the first workspace from sign-in to launch review
            </h1>
            <p className="mt-4 text-sm leading-7 text-stone-600">
              Signed in as {sessionQuery.data.email}. This flow emphasizes validation,
              draft restore, route guard, and submit retry handling.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => signOutMutation.mutate()}
              className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
            >
              Sign out
            </button>
            <Link
              href="/case-study"
              className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
            >
              Case study
            </Link>
          </div>
        </div>
      </header>

      <div className="mt-6 grid gap-5 xl:grid-cols-[18rem_minmax(0,1fr)]">
        <aside className="rounded-[1.8rem] border border-white/80 bg-[rgba(255,251,245,0.9)] p-5 shadow-[0_20px_50px_-40px_rgba(24,34,24,0.6)]">
          <p className="font-mono text-xs uppercase tracking-[0.22em] text-stone-500">
            Progress
          </p>
          <div className="mt-4 space-y-3">
            {onboardingSteps.map((candidateStep, index) => (
              <button
                key={candidateStep}
                type="button"
                onClick={() => onStepChange(candidateStep)}
                aria-current={candidateStep === step ? "step" : undefined}
                className={`flex w-full items-start gap-3 rounded-[1.2rem] border px-4 py-3 text-left transition ${
                  candidateStep === step
                    ? "border-stone-900 bg-stone-950 text-white"
                    : "border-stone-200 bg-white/70 text-stone-800 hover:border-stone-400"
                }`}
              >
                <span className="font-mono text-xs">{String(index + 1).padStart(2, "0")}</span>
                <span>
                  <span className="block text-sm font-semibold">{stepTitles[candidateStep]}</span>
                  <span className={`mt-1 block text-xs ${candidateStep === step ? "text-stone-200" : "text-stone-500"}`}>
                    {candidateStep === "workspace"
                      ? "Profile, region, and compliance owner"
                      : candidateStep === "invites"
                        ? "Invite the first collaborators"
                        : "Review checklist and submit"}
                  </span>
                </span>
              </button>
            ))}
          </div>

          <div className="mt-6 rounded-[1.3rem] border border-stone-200 bg-white/70 p-4">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-stone-500">
              Checklist
            </p>
            <ul className="mt-3 space-y-2 text-sm text-stone-700">
              {checklist.map((item) => (
                <li key={item.id} className="flex items-center gap-3">
                  <span
                    aria-hidden="true"
                    className={`inline-flex h-5 w-5 items-center justify-center rounded-full text-xs ${
                      item.completed
                        ? "bg-emerald-100 text-emerald-700"
                        : "bg-stone-100 text-stone-500"
                    }`}
                  >
                    {item.completed ? "✓" : "•"}
                  </span>
                  <span>{item.label}</span>
                </li>
              ))}
            </ul>
          </div>
        </aside>

        <section className="rounded-[1.8rem] border border-white/80 bg-[rgba(255,251,245,0.92)] p-6 shadow-[0_20px_50px_-40px_rgba(24,34,24,0.62)]">
          {step === "workspace" ? (
            <form
              className="space-y-5"
              onSubmit={workspaceForm.handleSubmit((values) => saveProfileMutation.mutate(values))}
            >
              <div>
                <p className="font-mono text-xs uppercase tracking-[0.22em] text-stone-500">
                  Workspace step
                </p>
                <h2 className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-stone-950">
                  Capture the launch-ready workspace profile
                </h2>
              </div>

              <div className="grid gap-4 md:grid-cols-2">
                <Field label="Workspace name" error={workspaceForm.formState.errors.workspaceName?.message}>
                  <input
                    {...workspaceForm.register("workspaceName")}
                    placeholder="Lattice Cloud"
                    className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                  />
                </Field>
                <Field label="Industry" error={workspaceForm.formState.errors.industry?.message}>
                  <input
                    {...workspaceForm.register("industry")}
                    placeholder="Developer tooling"
                    className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                  />
                </Field>
                <Field label="Region" error={workspaceForm.formState.errors.region?.message}>
                  <select
                    {...workspaceForm.register("region")}
                    className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                  >
                    <option value="">Select a region</option>
                    <option value="Seoul">Seoul</option>
                    <option value="Singapore">Singapore</option>
                    <option value="Frankfurt">Frankfurt</option>
                    <option value="Oregon">Oregon</option>
                  </select>
                </Field>
                <Field label="Team size" error={workspaceForm.formState.errors.teamSize?.message}>
                  <select
                    {...workspaceForm.register("teamSize")}
                    className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                  >
                    <option value="">Select team size</option>
                    <option value="1-10">1-10</option>
                    <option value="11-50">11-50</option>
                    <option value="51-200">51-200</option>
                    <option value="200+">200+</option>
                  </select>
                </Field>
              </div>

              <Field label="Compliance contact" error={workspaceForm.formState.errors.complianceEmail?.message}>
                <input
                  {...workspaceForm.register("complianceEmail")}
                  placeholder="compliance@latticecloud.dev"
                  className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                />
              </Field>

              {saveMessage ? (
                <p className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
                  {saveMessage}
                </p>
              ) : null}

              <div className="flex flex-wrap gap-3">
                <button
                  type="submit"
                  className="rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white"
                >
                  {saveProfileMutation.isPending ? "Saving..." : "Save draft"}
                </button>
                <button
                  type="button"
                  onClick={() => onStepChange("invites")}
                  className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
                >
                  Go to invites
                </button>
              </div>
            </form>
          ) : null}

          {step === "invites" ? (
            <div className="space-y-6">
              <div>
                <p className="font-mono text-xs uppercase tracking-[0.22em] text-stone-500">
                  Invite step
                </p>
                <h2 className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-stone-950">
                  Bring the first operators into the workspace
                </h2>
              </div>

              <form
                className="grid gap-4 rounded-[1.5rem] border border-stone-200 bg-white/70 p-4 md:grid-cols-[minmax(0,1fr)_12rem_10rem]"
                onSubmit={inviteForm.handleSubmit((values) => addInviteMutation.mutate(values))}
              >
                <Field label="Invite email" error={inviteForm.formState.errors.email?.message}>
                  <input
                    {...inviteForm.register("email")}
                    placeholder="teammate@latticecloud.dev"
                    className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                  />
                </Field>
                <Field label="Role" error={inviteForm.formState.errors.role?.message}>
                  <select
                    {...inviteForm.register("role")}
                    className="rounded-2xl border border-stone-300 bg-white px-4 py-3 outline-none focus:border-stone-500"
                  >
                    <option value="Collaborator">Collaborator</option>
                    <option value="Billing">Billing</option>
                    <option value="Admin">Admin</option>
                  </select>
                </Field>
                <div className="flex items-end">
                  <button
                    type="submit"
                    className="w-full rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white"
                  >
                    {addInviteMutation.isPending ? "Adding..." : "Add invite"}
                  </button>
                </div>
              </form>

              <div className="rounded-[1.5rem] border border-stone-200 bg-white/70 p-4">
                <p className="font-mono text-xs uppercase tracking-[0.18em] text-stone-500">
                  Pending invites
                </p>
                <ul className="mt-4 space-y-3">
                  {invites.map((invite: Invite) => (
                    <li
                      key={invite.id}
                      className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-stone-200 px-4 py-3"
                    >
                      <div>
                        <p className="text-sm font-semibold text-stone-900">{invite.email}</p>
                        <p className="text-sm text-stone-600">{invite.role}</p>
                      </div>
                      <span className="rounded-full bg-stone-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.12em] text-stone-500">
                        {invite.status}
                      </span>
                    </li>
                  ))}
                </ul>
                {selectedInviteCount === 0 ? (
                  <p className="mt-4 text-sm text-stone-600">
                    No invites yet. Add one teammate to unlock submit readiness.
                  </p>
                ) : null}
              </div>

              <div className="flex flex-wrap gap-3">
                <button
                  type="button"
                  onClick={() => onStepChange("workspace")}
                  className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
                >
                  Back to workspace
                </button>
                <button
                  type="button"
                  onClick={() => onStepChange("review")}
                  className="rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white"
                >
                  Continue to review
                </button>
              </div>
            </div>
          ) : null}

          {step === "review" ? (
            <div className="space-y-6">
              <div>
                <p className="font-mono text-xs uppercase tracking-[0.22em] text-stone-500">
                  Review step
                </p>
                <h2 className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-stone-950">
                  Confirm readiness and submit the onboarding packet
                </h2>
              </div>

              <div className="grid gap-4 lg:grid-cols-2">
                <SummaryCard
                  title="Workspace summary"
                  lines={[
                    profile.workspaceName || "No workspace name saved",
                    `${profile.industry || "Industry missing"} / ${profile.region || "Region missing"}`,
                    `Team size: ${profile.teamSize || "Not selected"}`,
                    `Compliance: ${profile.complianceEmail || "Missing"}`,
                  ]}
                />
                <SummaryCard
                  title="Invite summary"
                  lines={
                    invites.length > 0
                      ? invites.map((invite) => `${invite.email} (${invite.role})`)
                      : ["No teammate invites yet"]
                  }
                />
              </div>

              <div className="rounded-[1.5rem] border border-stone-200 bg-white/70 p-4">
                <label className="flex items-center gap-3 text-sm text-stone-700">
                  <input
                    type="checkbox"
                    checked={shouldFailNextSubmit}
                    onChange={(event) => setShouldFailNextSubmit(event.target.checked)}
                  />
                  Simulate the next submit failure to demo retry handling
                </label>
                <div className="mt-4 flex flex-wrap gap-3">
                  <button
                    type="button"
                    onClick={() => completeReviewMutation.mutate()}
                    className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
                  >
                    Mark review complete
                  </button>
                  <button
                    type="button"
                    onClick={() => submitMutation.mutate()}
                    disabled={!canSubmit || submitMutation.isPending}
                    className="rounded-full bg-stone-950 px-5 py-3 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {submitMutation.isPending ? "Submitting..." : "Submit onboarding"}
                  </button>
                </div>
              </div>

              {submitError ? (
                <p className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {submitError}
                </p>
              ) : null}

              {submitResult ? (
                <p className="rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
                  Submitted {submitResult.workspaceName} at {submitResult.submittedAt}. {submitResult.inviteCount} invite(s) included.
                </p>
              ) : null}

              <div className="flex flex-wrap gap-3">
                <button
                  type="button"
                  onClick={() => onStepChange("invites")}
                  className="rounded-full border border-stone-300 px-5 py-3 text-sm font-semibold text-stone-700"
                >
                  Back to invites
                </button>
              </div>
            </div>
          ) : null}
        </section>
      </div>
    </main>
  );
}

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="grid gap-2 text-sm font-semibold text-stone-800">
      {label}
      {children}
      {error ? <span className="text-sm font-normal text-red-700">{error}</span> : null}
    </label>
  );
}

function SummaryCard({ title, lines }: { title: string; lines: string[] }) {
  return (
    <article className="rounded-[1.5rem] border border-stone-200 bg-white/70 p-4">
      <p className="font-mono text-xs uppercase tracking-[0.18em] text-stone-500">{title}</p>
      <ul className="mt-4 space-y-2 text-sm text-stone-700">
        {lines.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
    </article>
  );
}
