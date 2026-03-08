import type { BoardItem } from "./types";

export const DEFAULT_ITEMS: BoardItem[] = [
  {
    id: "task-101",
    title: "Reconcile queue ownership",
    workspace: "Ops North",
    owner: "Jin",
    status: "open",
    priority: 4,
  },
  {
    id: "task-102",
    title: "Refresh escalation macros",
    workspace: "Support West",
    owner: "Mina",
    status: "blocked",
    priority: 5,
  },
  {
    id: "task-103",
    title: "Close onboarding checklist gaps",
    workspace: "Customer Success",
    owner: "Evan",
    status: "done",
    priority: 2,
  },
  {
    id: "task-104",
    title: "Audit queue retention rules",
    workspace: "Ops North",
    owner: "Hana",
    status: "open",
    priority: 3,
  },
];
