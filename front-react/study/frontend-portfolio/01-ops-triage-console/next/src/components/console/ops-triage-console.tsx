"use client";

import Link from "next/link";
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
  type RowSelectionState,
} from "@tanstack/react-table";
import { startTransition, useDeferredValue, useState } from "react";
import { IssueDetailDialog } from "@/components/console/issue-detail-dialog";
import { RuntimeControls } from "@/components/console/runtime-controls";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Popover } from "@/components/ui/popover";
import { Select } from "@/components/ui/select";
import { Toast } from "@/components/ui/toast";
import { Tooltip } from "@/components/ui/tooltip";
import { Badge } from "@/components/ui/badge";
import {
  defaultIssueQuery,
  issueLabels,
  issuePriorities,
  issueSortLabel,
  issueSorts,
  issueSources,
  issueStatuses,
  priorityLabel,
  slaRiskLabel,
  slaRisks,
  sourceLabel,
  statusLabel,
  teamRouteLabel,
  teamRoutes,
} from "@/lib/constants";
import { mergeSavedView } from "@/lib/query";
import {
  type BulkIssuePatch,
  type Issue,
  type IssueLabel,
  type IssuePriority,
  type IssueQuery,
  type IssueSource,
  type IssueStatus,
  type SlaRisk,
  type TeamRoute,
} from "@/lib/types";
import { formatDateTime, formatRelativeMinutes } from "@/lib/utils";
import {
  useBulkIssueMutation,
  useDashboardSummary,
  useIssueDetail,
  useIssueList,
  useIssueMutation,
  useOpsRuntime,
  useResetDemoMutation,
  useSavedViews,
  type ConsoleToast,
} from "@/hooks/use-ops-triage";

function issueTone(status: IssueStatus): "neutral" | "warning" | "danger" | "success" {
  if (status === "resolved") {
    return "success";
  }

  if (status === "escalated") {
    return "danger";
  }

  if (status === "untriaged") {
    return "warning";
  }

  return "neutral";
}

function priorityTone(priority: IssuePriority): "neutral" | "warning" | "danger" | "success" {
  if (priority === "p0") {
    return "danger";
  }

  if (priority === "p1") {
    return "warning";
  }

  return "neutral";
}

function slaTone(slaRisk: SlaRisk): "neutral" | "warning" | "danger" | "success" {
  if (slaRisk === "breach") {
    return "danger";
  }

  if (slaRisk === "watch") {
    return "warning";
  }

  return "success";
}

function toggleFacetValue<T extends string>(values: T[], value: T): T[] {
  return values.includes(value)
    ? values.filter((item) => item !== value)
    : [...values, value];
}

function renderMiniBar(value: number, total: number, toneClassName: string) {
  const width = total > 0 ? `${Math.max(8, Math.round((value / total) * 100))}%` : "8%";

  return (
    <div className="h-2 w-full rounded-full bg-slate-100">
      <div className={`h-full rounded-full ${toneClassName}`} style={{ width }} />
    </div>
  );
}

export function OpsTriageConsole() {
  const [query, setQuery] = useState<IssueQuery>(defaultIssueQuery);
  const [selectedIssueId, setSelectedIssueId] = useState<string | null>(null);
  const [toast, setToast] = useState<ConsoleToast | null>(null);
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});
  const [activeViewId, setActiveViewId] = useState("all");
  const [bulkDraft, setBulkDraft] = useState<BulkIssuePatch>({});
  const [runtime, setRuntime] = useOpsRuntime();

  const deferredSearch = useDeferredValue(query.search);
  const effectiveQuery = {
    ...query,
    search: deferredSearch,
  };

  const summaryQuery = useDashboardSummary();
  const viewsQuery = useSavedViews();
  const issueListQuery = useIssueList(effectiveQuery);
  const detailQuery = useIssueDetail(selectedIssueId);
  const updateMutation = useIssueMutation(setToast);
  const bulkMutation = useBulkIssueMutation(selectedIssueId, setToast, () => {
    setRowSelection({});
    setBulkDraft({});
  });
  const resetMutation = useResetDemoMutation(setToast);

  const columns: ColumnDef<Issue>[] = [
    {
      id: "select",
      header: ({ table }) => (
        <Checkbox
          checked={table.getIsAllPageRowsSelected()}
          onCheckedChange={(checked) => table.toggleAllPageRowsSelected(!!checked)}
          aria-label="Select all rows"
        />
      ),
      cell: ({ row }) => (
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(checked) => row.toggleSelected(!!checked)}
          aria-label={`Select ${row.original.id}`}
        />
      ),
      size: 48,
    },
    {
      accessorKey: "title",
      header: "Issue",
      cell: ({ row }) => {
        const issue = row.original;

        return (
          <div className="min-w-[18rem]">
            <button
              type="button"
              className="text-left"
              onClick={() => setSelectedIssueId(issue.id)}
            >
              <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-slate-500">
                {issue.id}
              </p>
              <p className="mt-1 text-sm font-semibold text-slate-950">{issue.title}</p>
              <p className="mt-1 line-clamp-2 text-sm leading-5 text-slate-600">
                {issue.summary}
              </p>
            </button>
          </div>
        );
      },
    },
    {
      accessorKey: "source",
      header: "Source",
      cell: ({ row }) => (
        <div className="space-y-1 text-sm">
          <p className="font-medium text-slate-900">{sourceLabel[row.original.source]}</p>
          <p className="text-xs text-slate-500">{row.original.customer}</p>
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "Status",
      cell: ({ row }) => (
        <Badge tone={issueTone(row.original.status)}>{statusLabel[row.original.status]}</Badge>
      ),
    },
    {
      accessorKey: "priority",
      header: "Priority",
      cell: ({ row }) => (
        <Badge tone={priorityTone(row.original.priority)}>
          {priorityLabel[row.original.priority]}
        </Badge>
      ),
    },
    {
      accessorKey: "slaRisk",
      header: "SLA",
      cell: ({ row }) => (
        <Badge tone={slaTone(row.original.slaRisk)}>
          {slaRiskLabel[row.original.slaRisk]}
        </Badge>
      ),
    },
    {
      accessorKey: "routeTeam",
      header: "Route",
      cell: ({ row }) => (
        <div>
          <p className="text-sm font-medium text-slate-900">
            {teamRouteLabel[row.original.routeTeam]}
          </p>
          <p className="mt-1 text-xs text-slate-500">{row.original.owner}</p>
        </div>
      ),
    },
    {
      accessorKey: "updatedAt",
      header: "Updated",
      cell: ({ row }) => (
        <div className="space-y-1 text-right">
          <p className="font-mono text-xs text-slate-700">
            {formatRelativeMinutes(row.original.updatedAt)}
          </p>
          <p className="text-xs text-slate-500">{formatDateTime(row.original.updatedAt)}</p>
        </div>
      ),
    },
    {
      id: "actions",
      header: "",
      cell: ({ row }) => {
        const isPending =
          updateMutation.pendingIds.includes(row.original.id) ||
          bulkMutation.pendingIds.includes(row.original.id);

        return (
          <div className="flex justify-end gap-2">
            {isPending ? (
              <Badge tone="warning">Saving</Badge>
            ) : null}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSelectedIssueId(row.original.id)}
            >
              Open
            </Button>
          </div>
        );
      },
    },
  ];

  const table = useReactTable({
    data: issueListQuery.data?.items ?? [],
    columns,
    state: {
      rowSelection,
    },
    getCoreRowModel: getCoreRowModel(),
    getRowId: (row) => row.id,
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
  });

  const selectedIssueIds = table
    .getSelectedRowModel()
    .rows.map((row) => row.original.id);

  const activeFilters = [
    ...query.status.map((value) => ({
      key: `status:${value}`,
      label: `Status ${statusLabel[value]}`,
      onRemove: () =>
        updateQuery({
          status: query.status.filter((item) => item !== value),
        }),
    })),
    ...query.priority.map((value) => ({
      key: `priority:${value}`,
      label: `Priority ${priorityLabel[value]}`,
      onRemove: () =>
        updateQuery({
          priority: query.priority.filter((item) => item !== value),
        }),
    })),
    ...query.source.map((value) => ({
      key: `source:${value}`,
      label: `Source ${sourceLabel[value]}`,
      onRemove: () =>
        updateQuery({
          source: query.source.filter((item) => item !== value),
        }),
    })),
    ...query.slaRisk.map((value) => ({
      key: `sla:${value}`,
      label: `SLA ${slaRiskLabel[value]}`,
      onRemove: () =>
        updateQuery({
          slaRisk: query.slaRisk.filter((item) => item !== value),
        }),
    })),
    ...query.label.map((value) => ({
      key: `label:${value}`,
      label: `Label ${value}`,
      onRemove: () =>
        updateQuery({
          label: query.label.filter((item) => item !== value),
        }),
    })),
  ];

  function updateQuery(patch: Partial<IssueQuery>) {
    startTransition(() => {
      setActiveViewId("custom");
      setQuery((current) => ({
        ...current,
        ...patch,
        page: patch.page ?? 1,
      }));
    });
  }

  function toggleStatus(value: IssueStatus) {
    updateQuery({ status: toggleFacetValue(query.status, value) });
  }

  function togglePriority(value: IssuePriority) {
    updateQuery({ priority: toggleFacetValue(query.priority, value) });
  }

  function toggleSource(value: IssueSource) {
    updateQuery({ source: toggleFacetValue(query.source, value) });
  }

  function toggleSlaRisk(value: SlaRisk) {
    updateQuery({ slaRisk: toggleFacetValue(query.slaRisk, value) });
  }

  function toggleLabel(value: IssueLabel) {
    updateQuery({ label: toggleFacetValue(query.label, value) });
  }

  function applySavedView(viewId: string) {
    const view = viewsQuery.data?.find((item) => item.id === viewId);

    if (!view) {
      return;
    }

    startTransition(() => {
      setActiveViewId(view.id);
      setQuery((current) => mergeSavedView(current, view));
    });
  }

  function clearAllFilters() {
    startTransition(() => {
      setActiveViewId("all");
      setQuery(defaultIssueQuery);
    });
  }

  function renderFacetGroup<T extends string>(
    title: string,
    values: T[],
    selectedValues: T[],
    labelMap: Record<T, string>,
    onToggle: (value: T) => void,
  ) {
    return (
      <div className="space-y-2">
        <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
          {title}
        </p>
        <div className="grid gap-2 sm:grid-cols-2">
          {values.map((value) => {
            const selected = selectedValues.includes(value);

            return (
              <button
                key={value}
                type="button"
                className={
                  selected
                    ? "flex items-center justify-between rounded-2xl border border-slate-950 bg-slate-950 px-3 py-2 text-left text-sm text-white"
                    : "flex items-center justify-between rounded-2xl border border-slate-200 bg-slate-50 px-3 py-2 text-left text-sm text-slate-700"
                }
                onClick={() => onToggle(value)}
                aria-pressed={selected}
              >
                <span>{labelMap[value]}</span>
                <span className="font-mono text-xs">{selected ? "on" : "off"}</span>
              </button>
            );
          })}
        </div>
      </div>
    );
  }

  const totalIssues = summaryQuery.data?.totalIssues ?? 0;

  return (
    <div className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(241,245,249,0.9),transparent_40%),radial-gradient(circle_at_top_right,rgba(253,230,138,0.2),transparent_32%),radial-gradient(circle_at_bottom_left,rgba(226,232,240,0.8),transparent_34%)]" />
      <div className="relative mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <header className="rounded-[2rem] border border-white/80 bg-white/85 px-6 py-6 shadow-[0_30px_80px_-60px_rgba(15,23,42,0.6)] backdrop-blur">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-slate-500">
                Frontend Portfolio / Dense but calm ops UI
              </p>
              <h1 className="mt-3 text-4xl font-semibold tracking-[-0.04em] text-slate-950 sm:text-5xl">
                Ops Triage Console
              </h1>
              <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-600 sm:text-base">
                A single-operator B2B console for sorting support, QA, feedback, and
                monitoring issues without losing queue context.
              </p>
            </div>
            <div className="flex flex-col gap-3 lg:items-end">
              <div className="flex flex-wrap items-center gap-2">
                <Tooltip content="Custom runtime work stays in the study track. This app prioritizes product-facing UI signals.">
                  <Badge tone="neutral">Main hiring portfolio</Badge>
                </Tooltip>
                <Tooltip content="Saved views, optimistic updates, retry and rollback are all demoed locally.">
                  <Badge tone="ink">Async mock service</Badge>
                </Tooltip>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <RuntimeControls
                  runtime={runtime}
                  setRuntime={setRuntime}
                  onResetDemo={() => resetMutation.mutate()}
                  isResetPending={resetMutation.isPending}
                />
                <Link href="/case-study">
                  <Button variant="primary">Open case study</Button>
                </Link>
              </div>
            </div>
          </div>
        </header>

        <section className="mt-6 grid gap-4 lg:grid-cols-4">
          <Card className="p-5">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
              Queue health
            </p>
            {summaryQuery.isLoading ? (
              <div className="mt-4 h-24 animate-pulse rounded-2xl bg-slate-100" />
            ) : summaryQuery.isError ? (
              <div className="mt-4 space-y-3">
                <p className="text-sm text-slate-600">
                  Summary is unavailable right now.
                </p>
                <Button size="sm" variant="secondary" onClick={() => summaryQuery.refetch()}>
                  Retry summary
                </Button>
              </div>
            ) : (
              <>
                <div className="mt-4 flex items-end justify-between gap-4">
                  <p className="text-4xl font-semibold tracking-[-0.04em] text-slate-950">
                    {summaryQuery.data?.totalIssues}
                  </p>
                  <p className="text-sm text-slate-500">Open items</p>
                </div>
                <div className="mt-4 flex items-center justify-between text-sm">
                  <span className="text-slate-500">Untriaged</span>
                  <span className="font-semibold text-slate-950">
                    {summaryQuery.data?.untriagedCount}
                  </span>
                </div>
                <div className="mt-2 flex items-center justify-between text-sm">
                  <span className="text-slate-500">Escalated</span>
                  <span className="font-semibold text-slate-950">
                    {summaryQuery.data?.escalatedCount}
                  </span>
                </div>
              </>
            )}
          </Card>

          <Card className="p-5">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
              SLA pressure
            </p>
            {summaryQuery.data ? (
              <div className="mt-4 space-y-4">
                <div className="rounded-2xl bg-amber-50 px-4 py-4">
                  <p className="text-xs uppercase tracking-[0.16em] text-amber-700">
                    At risk
                  </p>
                  <p className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-slate-950">
                    {summaryQuery.data.atRiskCount}
                  </p>
                </div>
                <div className="rounded-2xl bg-red-50 px-4 py-4">
                  <p className="text-xs uppercase tracking-[0.16em] text-red-700">
                    Breach / escalated
                  </p>
                  <p className="mt-2 text-3xl font-semibold tracking-[-0.04em] text-slate-950">
                    {summaryQuery.data.escalatedCount}
                  </p>
                </div>
              </div>
            ) : (
              <div className="mt-4 h-32 animate-pulse rounded-2xl bg-slate-100" />
            )}
          </Card>

          <Card className="p-5">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
              Priority mix
            </p>
            {summaryQuery.data ? (
              <div className="mt-4 space-y-4">
                {issuePriorities.map((priority) => (
                  <div key={priority} className="space-y-2">
                    <div className="flex items-center justify-between gap-3 text-sm">
                      <span className="font-medium text-slate-700">
                        {priorityLabel[priority]}
                      </span>
                      <span className="font-mono text-xs text-slate-500">
                        {summaryQuery.data.priorityCounts[priority]}
                      </span>
                    </div>
                    {renderMiniBar(
                      summaryQuery.data.priorityCounts[priority],
                      totalIssues,
                      priority === "p0"
                        ? "bg-red-500"
                        : priority === "p1"
                          ? "bg-amber-500"
                          : "bg-slate-400",
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="mt-4 h-32 animate-pulse rounded-2xl bg-slate-100" />
            )}
          </Card>

          <Card className="p-5">
            <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
              Recent changes
            </p>
            {summaryQuery.data ? (
              <div className="mt-4 space-y-3">
                {summaryQuery.data.recentChanges.map((change) => (
                  <div
                    key={change.label}
                    className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <p className="text-sm font-medium text-slate-900">{change.label}</p>
                      <Badge tone={change.tone}>{change.value}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="mt-4 h-32 animate-pulse rounded-2xl bg-slate-100" />
            )}
          </Card>
        </section>

        <section className="mt-6 grid gap-6 lg:grid-cols-[minmax(0,1.8fr)_minmax(18rem,0.9fr)]">
          <Card className="overflow-hidden">
            <div className="border-b border-slate-200 px-5 py-5">
              <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
                <div>
                  <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                    Queue
                  </p>
                  <h2 className="mt-2 text-2xl font-semibold tracking-[-0.03em] text-slate-950">
                    Issue inbox
                  </h2>
                  <p className="mt-2 text-sm text-slate-600">
                    Search, filter, bulk route, and keep detail context in reach.
                  </p>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                    {issueListQuery.data?.total ?? 0} visible
                  </span>
                  {issueListQuery.isFetching ? (
                    <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-800">
                      Syncing
                    </span>
                  ) : null}
                </div>
              </div>

              <div className="mt-5 flex flex-wrap gap-2">
                {viewsQuery.data?.map((view) => (
                  <button
                    key={view.id}
                    type="button"
                    className={
                      activeViewId === view.id
                        ? "rounded-full bg-slate-950 px-4 py-2 text-sm font-semibold text-white"
                        : "rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700"
                    }
                    onClick={() => applySavedView(view.id)}
                  >
                    {view.name}
                  </button>
                ))}
              </div>

              <div className="mt-5 grid gap-3 xl:grid-cols-[minmax(0,1.6fr)_minmax(0,0.65fr)_auto_auto]">
                <div className="space-y-2">
                  <label
                    htmlFor="issue-search"
                    className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500"
                  >
                    Search queue
                  </label>
                  <Input
                    id="issue-search"
                    data-testid="issue-search"
                    placeholder="Search issue title, customer, route team, or labels"
                    value={query.search}
                    onChange={(event) => updateQuery({ search: event.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    Sort
                  </label>
                  <Select
                    ariaLabel="Issue sort"
                    value={query.sort}
                    onValueChange={(value) =>
                      updateQuery({ sort: value as IssueQuery["sort"] })
                    }
                    placeholder="Sort queue"
                    options={issueSorts.map((value) => ({
                      value,
                      label: issueSortLabel[value],
                    }))}
                  />
                </div>
                <div className="space-y-2">
                  <span className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    Facets
                  </span>
                  <Popover
                    trigger={
                      <Button variant="secondary" className="w-full xl:w-auto">
                        Filters ({activeFilters.length})
                      </Button>
                    }
                  >
                    <div className="max-h-[70vh] space-y-4 overflow-y-auto pr-1">
                      {renderFacetGroup("Status", issueStatuses, query.status, statusLabel, toggleStatus)}
                      {renderFacetGroup(
                        "Priority",
                        issuePriorities,
                        query.priority,
                        priorityLabel,
                        togglePriority,
                      )}
                      {renderFacetGroup("Source", issueSources, query.source, sourceLabel, toggleSource)}
                      {renderFacetGroup("SLA risk", slaRisks, query.slaRisk, slaRiskLabel, toggleSlaRisk)}
                      {renderFacetGroup(
                        "Labels",
                        issueLabels,
                        query.label,
                        {
                          billing: "billing",
                          checkout: "checkout",
                          latency: "latency",
                          mobile: "mobile",
                          search: "search",
                          retention: "retention",
                        },
                        toggleLabel,
                      )}
                    </div>
                  </Popover>
                </div>
                <div className="space-y-2">
                  <span className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                    Bulk
                  </span>
                  <Button
                    variant="primary"
                    className="w-full xl:w-auto"
                    disabled={selectedIssueIds.length === 0}
                  >
                    Bulk actions ({selectedIssueIds.length})
                  </Button>
                </div>
              </div>

              {activeFilters.length > 0 ? (
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  {activeFilters.map((filter) => (
                    <button
                      key={filter.key}
                      type="button"
                      className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-700"
                      onClick={filter.onRemove}
                    >
                      {filter.label} x
                    </button>
                  ))}
                  <Button size="sm" variant="ghost" onClick={clearAllFilters}>
                    Clear all
                  </Button>
                </div>
              ) : null}

              {selectedIssueIds.length > 0 ? (
                <div className="mt-4 rounded-[1.5rem] border border-slate-200 bg-slate-50/80 p-4">
                  <div className="flex flex-col gap-4 xl:flex-row xl:items-end">
                    <div className="grid flex-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
                      <div className="space-y-2">
                        <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                          Status
                        </label>
                        <Select
                          ariaLabel="Bulk status"
                          value={bulkDraft.status}
                          onValueChange={(value) =>
                            setBulkDraft((current) => ({
                              ...current,
                              status: value as IssueStatus,
                            }))
                          }
                          placeholder="Optional status"
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
                          ariaLabel="Bulk priority"
                          value={bulkDraft.priority}
                          onValueChange={(value) =>
                            setBulkDraft((current) => ({
                              ...current,
                              priority: value as IssuePriority,
                            }))
                          }
                          placeholder="Optional priority"
                          options={issuePriorities.map((value) => ({
                            value,
                            label: priorityLabel[value],
                          }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                          Route team
                        </label>
                        <Select
                          ariaLabel="Bulk route team"
                          value={bulkDraft.routeTeam}
                          onValueChange={(value) =>
                            setBulkDraft((current) => ({
                              ...current,
                              routeTeam: value as TeamRoute,
                            }))
                          }
                          placeholder="Optional route team"
                          options={teamRoutes.map((value) => ({
                            value,
                            label: teamRouteLabel[value],
                          }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                          Add label
                        </label>
                        <Select
                          ariaLabel="Bulk label"
                          value={bulkDraft.addLabel}
                          onValueChange={(value) =>
                            setBulkDraft((current) => ({
                              ...current,
                              addLabel: value as IssueLabel,
                            }))
                          }
                          placeholder="Optional label"
                          options={issueLabels.map((value) => ({
                            value,
                            label: value,
                          }))}
                        />
                      </div>
                    </div>
                    <Button
                      variant="primary"
                      className="xl:min-w-48"
                      data-testid="apply-bulk-action"
                      onClick={() =>
                        bulkMutation.applyBulk({
                          issueIds: selectedIssueIds,
                          patch: bulkDraft,
                        })
                      }
                      disabled={
                        selectedIssueIds.length === 0 ||
                        bulkMutation.isPending ||
                        Object.keys(bulkDraft).length === 0
                      }
                    >
                      {bulkMutation.isPending
                        ? "Applying bulk update..."
                        : "Apply bulk action"}
                    </Button>
                  </div>
                </div>
              ) : null}
            </div>

            {issueListQuery.isLoading ? (
              <div className="space-y-3 px-5 py-5">
                {Array.from({ length: 6 }).map((_, index) => (
                  <div
                    key={index}
                    className="h-16 animate-pulse rounded-2xl bg-slate-100"
                  />
                ))}
              </div>
            ) : issueListQuery.isError ? (
              <div className="px-5 py-8">
                <Card className="border-dashed p-6">
                  <p className="text-base font-semibold text-slate-950">
                    Queue sync failed
                  </p>
                  <p className="mt-2 max-w-xl text-sm leading-6 text-slate-600">
                    The local async layer returned a retryable error. Keep the draft
                    state and retry the query.
                  </p>
                  <div className="mt-4 flex gap-2">
                    <Button variant="primary" onClick={() => issueListQuery.refetch()}>
                      Retry queue
                    </Button>
                    <Button variant="secondary" onClick={clearAllFilters}>
                      Reset filters
                    </Button>
                  </div>
                </Card>
              </div>
            ) : issueListQuery.data && issueListQuery.data.items.length === 0 ? (
              <div className="px-5 py-8">
                <Card className="border-dashed p-6">
                  <p className="text-base font-semibold text-slate-950">No matching issues</p>
                  <p className="mt-2 max-w-xl text-sm leading-6 text-slate-600">
                    The current combination of search and facets is too narrow for the
                    seeded demo queue.
                  </p>
                  <div className="mt-4 flex gap-2">
                    <Button variant="primary" onClick={clearAllFilters}>
                      Clear filters
                    </Button>
                    <Button
                      variant="secondary"
                      onClick={() => updateQuery({ search: "" })}
                    >
                      Clear search only
                    </Button>
                  </div>
                </Card>
              </div>
            ) : (
              <>
                <div className="overflow-x-auto px-2 py-2">
                  <table
                    className="min-w-full border-separate border-spacing-y-2"
                    data-testid="issue-table"
                  >
                    <thead>
                      {table.getHeaderGroups().map((headerGroup) => (
                        <tr key={headerGroup.id}>
                          {headerGroup.headers.map((header) => (
                            <th
                              key={header.id}
                              className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-[0.16em] text-slate-500"
                            >
                              {header.isPlaceholder
                                ? null
                                : flexRender(
                                    header.column.columnDef.header,
                                    header.getContext(),
                                  )}
                            </th>
                          ))}
                        </tr>
                      ))}
                    </thead>
                    <tbody>
                      {table.getRowModel().rows.map((row) => (
                        <tr
                          key={row.id}
                          className={
                            row.getIsSelected()
                              ? "rounded-2xl bg-slate-50 shadow-[0_12px_24px_-24px_rgba(15,23,42,0.6)]"
                              : "rounded-2xl bg-white shadow-[0_12px_24px_-24px_rgba(15,23,42,0.45)]"
                          }
                        >
                          {row.getVisibleCells().map((cell) => (
                            <td
                              key={cell.id}
                              className="border-y border-slate-200 px-3 py-4 first:rounded-l-2xl first:border-l last:rounded-r-2xl last:border-r"
                            >
                              {flexRender(
                                cell.column.columnDef.cell,
                                cell.getContext(),
                              )}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="flex flex-col gap-3 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                  <p className="text-sm text-slate-600">
                    Page {issueListQuery.data?.page} of {issueListQuery.data?.totalPages}
                  </p>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => updateQuery({ page: Math.max(1, query.page - 1) })}
                      disabled={query.page === 1}
                    >
                      Previous
                    </Button>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() =>
                        updateQuery({
                          page: Math.min(
                            issueListQuery.data?.totalPages ?? query.page,
                            query.page + 1,
                          ),
                        })
                      }
                      disabled={query.page >= (issueListQuery.data?.totalPages ?? 1)}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              </>
            )}
          </Card>

          <div className="space-y-4">
            <Card className="p-5">
              <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                Case study entry
              </p>
              <h3 className="mt-3 text-xl font-semibold tracking-[-0.03em] text-slate-950">
                Product framing for hiring review
              </h3>
              <p className="mt-3 text-sm leading-6 text-slate-600">
                The case study explains why this app optimizes density, async trust, and
                keyboard-friendly routing instead of polished marketing chrome.
              </p>
              <div className="mt-4 space-y-3">
                <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                  Problem definition and operator context
                </div>
                <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                  UX and state-flow tradeoffs
                </div>
                <div className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
                  Testing, accessibility, and performance bar
                </div>
              </div>
              <div className="mt-5">
                <Link href="/case-study">
                  <Button variant="primary" className="w-full">
                    Read case study
                  </Button>
                </Link>
              </div>
            </Card>

            <Card className="p-5">
              <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                Triage playbook
              </p>
              <div className="mt-4 space-y-4 text-sm text-slate-600">
                <div>
                  <p className="font-semibold text-slate-950">1. Scan saved views</p>
                  <p className="mt-1">
                    Start with At Risk or Needs Escalation to collapse decision time when
                    queues spike.
                  </p>
                </div>
                <div>
                  <p className="font-semibold text-slate-950">2. Route fast, note lightly</p>
                  <p className="mt-1">
                    Keep operator notes short enough to review from the timeline during a
                    handoff.
                  </p>
                </div>
                <div>
                  <p className="font-semibold text-slate-950">3. Trust but verify async state</p>
                  <p className="mt-1">
                    Optimistic updates keep the grid moving. Retry and Undo protect data
                    confidence when the mock API fails.
                  </p>
                </div>
              </div>
            </Card>

            <Card className="p-5">
              <p className="font-mono text-xs uppercase tracking-[0.18em] text-slate-500">
                Selected rows
              </p>
              <div className="mt-4 space-y-3">
                <div className="flex items-end justify-between gap-3">
                  <p className="text-3xl font-semibold tracking-[-0.04em] text-slate-950">
                    {selectedIssueIds.length}
                  </p>
                  <p className="text-sm text-slate-500">Ready for bulk action</p>
                </div>
                <p className="text-sm leading-6 text-slate-600">
                  Use row selection to apply route, priority, status, or label changes
                  without opening every issue individually.
                </p>
              </div>
            </Card>
          </div>
        </section>

        <IssueDetailDialog
          open={!!selectedIssueId}
          onOpenChange={(open) => {
            if (!open) {
              setSelectedIssueId(null);
            }
          }}
          issue={detailQuery.data}
          isLoading={detailQuery.isLoading}
          isPending={
            !!selectedIssueId && updateMutation.pendingIds.includes(selectedIssueId)
          }
          onSubmit={(patch) => {
            if (!selectedIssueId) {
              return;
            }

            updateMutation.updateOne({
              issueId: selectedIssueId,
              patch,
            });
          }}
        />
      </div>

      {toast ? (
        <Toast
          tone={toast.tone}
          title={toast.title}
          description={toast.description}
          actionLabel={toast.actionLabel}
          onAction={toast.onAction}
          onDismiss={() => setToast(null)}
        />
      ) : null}
    </div>
  );
}
