"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog } from "@/components/ui/dialog";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  issueLabels,
  issuePriorities,
  issueStatuses,
  priorityLabel,
  slaRiskLabel,
  sourceLabel,
  statusLabel,
  teamRouteLabel,
  teamRoutes,
} from "@/lib/constants";
import { type Issue, type IssueLabel, type IssuePatch } from "@/lib/types";
import { formatDateTime, formatRelativeMinutes } from "@/lib/utils";

function arraysEqual(left: string[], right: string[]): boolean {
  return JSON.stringify(left.slice().sort()) === JSON.stringify(right.slice().sort());
}

export function IssueDetailDialog({
  open,
  onOpenChange,
  issue,
  isLoading,
  isPending,
  onSubmit,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  issue?: Issue;
  isLoading: boolean;
  isPending: boolean;
  onSubmit: (patch: IssuePatch) => void;
}) {
  const [status, setStatus] = useState<Issue["status"]>("untriaged");
  const [priority, setPriority] = useState<Issue["priority"]>("p2");
  const [routeTeam, setRouteTeam] = useState<Issue["routeTeam"]>("support");
  const [labels, setLabels] = useState<IssueLabel[]>([]);
  const [operatorNote, setOperatorNote] = useState("");

  useEffect(() => {
    if (!issue) {
      return;
    }

    setStatus(issue.status);
    setPriority(issue.priority);
    setRouteTeam(issue.routeTeam);
    setLabels(issue.labels);
    setOperatorNote(issue.operatorNote);
  }, [issue]);

  const hasChanges =
    !!issue &&
    (
      status !== issue.status ||
      priority !== issue.priority ||
      routeTeam !== issue.routeTeam ||
      !arraysEqual(labels, issue.labels) ||
      (operatorNote.trim().length > 0 &&
        operatorNote.trim() !== issue.operatorNote.trim())
    );

  function toggleLabel(label: IssueLabel) {
    setLabels((current) =>
      current.includes(label)
        ? current.filter((item) => item !== label)
        : [...current, label],
    );
  }

  function handleSubmit() {
    if (!issue || !hasChanges) {
      return;
    }

    const patch: IssuePatch = {};

    if (status !== issue.status) {
      patch.status = status;
    }

    if (priority !== issue.priority) {
      patch.priority = priority;
    }

    if (routeTeam !== issue.routeTeam) {
      patch.routeTeam = routeTeam;
    }

    if (!arraysEqual(labels, issue.labels)) {
      patch.labels = labels;
    }

    if (
      operatorNote.trim().length > 0 &&
      operatorNote.trim() !== issue.operatorNote.trim()
    ) {
      patch.operatorNote = operatorNote.trim();
    }

    onSubmit(patch);
  }

  return (
    <Dialog
      open={open}
      onOpenChange={onOpenChange}
      title={issue ? `${issue.id} issue detail` : "Issue detail"}
    >
      {isLoading ? (
        <div className="space-y-3">
          <div className="h-5 w-48 animate-pulse rounded-full bg-slate-200" />
          <div className="h-20 animate-pulse rounded-2xl bg-slate-100" />
          <div className="h-48 animate-pulse rounded-2xl bg-slate-100" />
        </div>
      ) : !issue ? (
        <Card className="p-5">
          <p className="text-sm font-semibold text-slate-950">Issue not found</p>
          <p className="mt-2 text-sm text-slate-600">
            The selected issue is no longer available in the queue.
          </p>
        </Card>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,0.9fr)]">
          <div className="space-y-5">
            <Card className="p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                    {issue.id}
                  </p>
                  <h2 className="mt-2 text-2xl font-semibold text-slate-950">
                    {issue.title}
                  </h2>
                  <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
                    {issue.summary}
                  </p>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-right">
                  <p className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    Last seen
                  </p>
                  <p className="mt-2 font-mono text-sm text-slate-950">
                    {formatRelativeMinutes(issue.lastSeenAt)}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    {formatDateTime(issue.lastSeenAt)}
                  </p>
                </div>
              </div>
              <dl className="mt-5 grid gap-3 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <dt className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    Customer
                  </dt>
                  <dd className="mt-2 text-sm font-medium text-slate-950">
                    {issue.customer}
                  </dd>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <dt className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    Source
                  </dt>
                  <dd className="mt-2 text-sm font-medium text-slate-950">
                    {sourceLabel[issue.source]}
                  </dd>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <dt className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    Status
                  </dt>
                  <dd className="mt-2 text-sm font-medium text-slate-950">
                    {statusLabel[issue.status]}
                  </dd>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <dt className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    SLA risk
                  </dt>
                  <dd className="mt-2 text-sm font-medium text-slate-950">
                    {slaRiskLabel[issue.slaRisk]}
                  </dd>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <dt className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    Priority
                  </dt>
                  <dd className="mt-2 text-sm font-medium text-slate-950">
                    {priorityLabel[issue.priority]}
                  </dd>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
                  <dt className="text-xs uppercase tracking-[0.14em] text-slate-500">
                    Route team
                  </dt>
                  <dd className="mt-2 text-sm font-medium text-slate-950">
                    {teamRouteLabel[issue.routeTeam]}
                  </dd>
                </div>
              </dl>
            </Card>

            <Card className="p-5">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <h3 className="text-sm font-semibold text-slate-950">Activity timeline</h3>
                  <p className="mt-1 text-sm text-slate-600">
                    Recent triage events remain visible for faster handoffs.
                  </p>
                </div>
                <p className="font-mono text-xs text-slate-500">
                  {issue.activity.length} events
                </p>
              </div>
              <ol className="mt-5 space-y-4">
                {issue.activity.map((entry) => (
                  <li
                    key={entry.id}
                    className="grid gap-2 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-sm font-medium text-slate-950">{entry.message}</p>
                      <p className="font-mono text-xs text-slate-500">
                        {formatRelativeMinutes(entry.timestamp)}
                      </p>
                    </div>
                    <div className="flex items-center justify-between gap-3 text-xs text-slate-500">
                      <span>{entry.actor}</span>
                      <span>{formatDateTime(entry.timestamp)}</span>
                    </div>
                  </li>
                ))}
              </ol>
            </Card>
          </div>

          <Card className="p-5">
            <div>
              <h3 className="text-sm font-semibold text-slate-950">Triage actions</h3>
              <p className="mt-1 text-sm text-slate-600">
                Apply operator changes with optimistic sync and rollback support.
              </p>
            </div>
            <div className="mt-5 space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    Status
                  </label>
                  <Select
                    ariaLabel="Issue status"
                    value={status}
                    onValueChange={(value) => setStatus(value as Issue["status"])}
                    placeholder="Select status"
                    options={issueStatuses.map((value) => ({
                      value,
                      label: statusLabel[value],
                    }))}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    Priority
                  </label>
                  <Select
                    ariaLabel="Issue priority"
                    value={priority}
                    onValueChange={(value) => setPriority(value as Issue["priority"])}
                    placeholder="Select priority"
                    options={issuePriorities.map((value) => ({
                      value,
                      label: priorityLabel[value],
                    }))}
                  />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Route team
                </label>
                <Select
                  ariaLabel="Route team"
                  value={routeTeam}
                  onValueChange={(value) => setRouteTeam(value as Issue["routeTeam"])}
                  placeholder="Select route team"
                  options={teamRoutes.map((value) => ({
                    value,
                    label: teamRouteLabel[value],
                  }))}
                />
              </div>
              <div className="space-y-2">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                  Labels
                </p>
                <div className="flex flex-wrap gap-2">
                  {issueLabels.map((label) => {
                    const selected = labels.includes(label);

                    return (
                      <button
                        key={label}
                        type="button"
                        className={
                          selected
                            ? "rounded-full bg-slate-950 px-3 py-1.5 text-xs font-semibold text-white"
                            : "rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700"
                        }
                        onClick={() => toggleLabel(label)}
                        aria-pressed={selected}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>
              </div>
              <div className="space-y-2">
                <label
                  htmlFor="operator-note"
                  className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500"
                >
                  Operator note
                </label>
                <Textarea
                  id="operator-note"
                  value={operatorNote}
                  onChange={(event) => setOperatorNote(event.target.value)}
                  placeholder="Capture the latest routing context or next verification step."
                  maxLength={180}
                />
                <p className="text-xs text-slate-500">
                  Notes are optimized for quick handoff, not long-form incident reports.
                </p>
              </div>
              <div className="flex items-center justify-between gap-3 border-t border-slate-200 pt-4">
                <p className="text-xs text-slate-500">
                  Changes sync optimistically. Failures will surface an inline retry toast.
                </p>
                <Button
                  variant="primary"
                  data-testid="apply-triage"
                  onClick={handleSubmit}
                  disabled={!hasChanges || isPending}
                >
                  {isPending ? "Applying..." : "Apply triage"}
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </Dialog>
  );
}
