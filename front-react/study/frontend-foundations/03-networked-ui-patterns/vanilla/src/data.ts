import type { DirectoryItem } from "./types";

export const DIRECTORY_ITEMS: DirectoryItem[] = [
  {
    id: "doc-101",
    title: "Incident response runbook",
    category: "runbook",
    owner: "Platform Ops",
    summary: "Checklist for triaging high-severity incidents and assigning responders.",
    body: "Start with impact confirmation, page the current responder rotation, then create a running incident timeline.",
  },
  {
    id: "doc-102",
    title: "Escalation policy handbook",
    category: "policy",
    owner: "Support Strategy",
    summary: "Defines paging thresholds and handoff rules across support queues.",
    body: "Escalations move to the duty manager after the second blocked SLA window or any customer-visible outage.",
  },
  {
    id: "doc-103",
    title: "Queue audit guide",
    category: "guide",
    owner: "Operations Enablement",
    summary: "How to inspect filters, ownership, and duplicate routing rules in shared queues.",
    body: "Review saved filters first, then compare queue membership and historical escalations before changing ownership.",
  },
  {
    id: "doc-104",
    title: "Change freeze policy",
    category: "policy",
    owner: "Release Operations",
    summary: "Release windows and rollback criteria during sensitive periods.",
    body: "Freeze begins 24 hours before the event window. Only incident mitigations and pre-approved fixes may ship.",
  },
  {
    id: "doc-105",
    title: "On-call onboarding runbook",
    category: "runbook",
    owner: "Developer Experience",
    summary: "Preparation steps for new responders joining the on-call rotation.",
    body: "Complete tooling access, shadow one weekly review, and verify escalation contacts before taking a primary shift.",
  },
];
