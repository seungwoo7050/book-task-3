"use client";

import { useState } from "react";
import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryKey,
} from "@tanstack/react-query";
import { applyBulkPatch, applyIssuePatch } from "@/lib/optimistic";
import {
  configureDemoRuntime,
  restoreIssuesSnapshot,
} from "@/lib/service-admin";
import {
  bulkUpdateIssues,
  getDashboardSummary,
  getIssue,
  getDemoRuntimeConfig,
  listIssues,
  listSavedViews,
  resetDemoData,
  updateIssue,
} from "@/lib/service";
import {
  type BulkIssuePatch,
  type DashboardSummary,
  type DemoRuntimeConfig,
  type Issue,
  type IssueListResult,
  type IssuePatch,
  type IssueQuery,
  type SavedView,
} from "@/lib/types";

export interface ConsoleToast {
  tone: "success" | "error";
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => Promise<void> | void;
}

export const issueKeys = {
  lists: () => ["issues"] as const,
  list: (query: IssueQuery) => ["issues", query] as const,
  detail: (issueId: string) => ["issue", issueId] as const,
  summary: () => ["dashboard-summary"] as const,
  views: () => ["saved-views"] as const,
};

async function invalidateOpsQueries(
  queryClient: ReturnType<typeof useQueryClient>,
): Promise<void> {
  await Promise.all([
    queryClient.invalidateQueries({ queryKey: issueKeys.lists() }),
    queryClient.invalidateQueries({ queryKey: ["issue"] }),
    queryClient.invalidateQueries({ queryKey: issueKeys.summary() }),
  ]);
}

export function useOpsRuntime(): [
  DemoRuntimeConfig,
  (nextValue: DemoRuntimeConfig) => void,
] {
  const [runtime, setRuntime] = useState<DemoRuntimeConfig>(getDemoRuntimeConfig());
  return [
    runtime,
    (nextValue) => {
      const updated = configureDemoRuntime(nextValue);
      setRuntime(updated);
    },
  ];
}

export function useIssueList(query: IssueQuery) {
  return useQuery({
    queryKey: issueKeys.list(query),
    queryFn: () => listIssues(query),
  });
}

export function useIssueDetail(issueId: string | null) {
  return useQuery({
    queryKey: issueKeys.detail(issueId ?? "none"),
    queryFn: () => getIssue(issueId!),
    enabled: !!issueId,
  });
}

export function useDashboardSummary() {
  return useQuery({
    queryKey: issueKeys.summary(),
    queryFn: getDashboardSummary,
  });
}

export function useSavedViews() {
  return useQuery({
    queryKey: issueKeys.views(),
    queryFn: listSavedViews,
  });
}

export function useIssueMutation(
  setToast: (toast: ConsoleToast | null) => void,
) {
  const queryClient = useQueryClient();
  const [pendingIds, setPendingIds] = useState<string[]>([]);

  const mutation = useMutation({
    mutationFn: ({
      issueId,
      patch,
    }: {
      issueId: string;
      patch: IssuePatch;
    }) => updateIssue(issueId, patch),
    onMutate: async ({ issueId, patch }) => {
      setPendingIds([issueId]);

      const issueLists = queryClient.getQueriesData<IssueListResult>({
        queryKey: issueKeys.lists(),
      });
      const detailSnapshot = queryClient.getQueryData<Issue | undefined>(
        issueKeys.detail(issueId),
      );

      for (const [key, listResult] of issueLists) {
        if (!listResult) {
          continue;
        }

        queryClient.setQueryData<IssueListResult>(key, {
          ...listResult,
          items: listResult.items.map((issue) =>
            issue.id === issueId ? applyIssuePatch(issue, patch) : issue,
          ),
        });
      }

      if (detailSnapshot) {
        queryClient.setQueryData(issueKeys.detail(issueId), applyIssuePatch(detailSnapshot, patch));
      }

      return { issueLists, detailSnapshot };
    },
    onError: (error, variables, context) => {
      context?.issueLists.forEach(([key, value]) => {
        queryClient.setQueryData(key as QueryKey, value);
      });

      if (context?.detailSnapshot) {
        queryClient.setQueryData(
          issueKeys.detail(variables.issueId),
          context.detailSnapshot,
        );
      }

      setToast({
        tone: "error",
        title: "Update failed",
        description: "The queue was rolled back. Retry the change.",
        actionLabel: "Retry",
        onAction: async () => {
          mutation.mutate(variables);
        },
      });

      console.error(error);
    },
    onSuccess: async (result) => {
      await invalidateOpsQueries(queryClient);
      setToast({
        tone: "success",
        title: "Issue updated",
        description: "The issue was triaged and synced across the console.",
        actionLabel: "Undo",
        onAction: async () => {
          await restoreIssuesSnapshot([result.previousIssue]);
          await invalidateOpsQueries(queryClient);
          setToast(null);
        },
      });
    },
    onSettled: () => {
      setPendingIds([]);
    },
  });

  return {
    updateOne: mutation.mutate,
    isPending: mutation.isPending,
    pendingIds,
  };
}

export function useBulkIssueMutation(
  selectedIssueId: string | null,
  setToast: (toast: ConsoleToast | null) => void,
  onApplied?: () => void,
) {
  const queryClient = useQueryClient();
  const [pendingIds, setPendingIds] = useState<string[]>([]);

  const mutation = useMutation({
    mutationFn: ({
      issueIds,
      patch,
    }: {
      issueIds: string[];
      patch: BulkIssuePatch;
    }) => bulkUpdateIssues(issueIds, patch),
    onMutate: async ({ issueIds, patch }) => {
      setPendingIds(issueIds);

      const issueLists = queryClient.getQueriesData<IssueListResult>({
        queryKey: issueKeys.lists(),
      });
      const detailSnapshot =
        selectedIssueId &&
        queryClient.getQueryData<Issue | undefined>(
          issueKeys.detail(selectedIssueId),
        );

      for (const [key, listResult] of issueLists) {
        if (!listResult) {
          continue;
        }

        queryClient.setQueryData<IssueListResult>(key, {
          ...listResult,
          items: applyBulkPatch(listResult.items, issueIds, patch),
        });
      }

      if (selectedIssueId && detailSnapshot && issueIds.includes(selectedIssueId)) {
        queryClient.setQueryData(
          issueKeys.detail(selectedIssueId),
          applyBulkPatch([detailSnapshot], [selectedIssueId], patch)[0],
        );
      }

      return { issueLists, detailSnapshot };
    },
    onError: (error, variables, context) => {
      context?.issueLists.forEach(([key, value]) => {
        queryClient.setQueryData(key as QueryKey, value);
      });

      if (selectedIssueId && context?.detailSnapshot) {
        queryClient.setQueryData(
          issueKeys.detail(selectedIssueId),
          context.detailSnapshot,
        );
      }

      setToast({
        tone: "error",
        title: "Bulk update failed",
        description: "The selected rows were rolled back. Retry the bulk action.",
        actionLabel: "Retry",
        onAction: async () => {
          mutation.mutate(variables);
        },
      });

      console.error(error);
    },
    onSuccess: async (result) => {
      await invalidateOpsQueries(queryClient);
      setToast({
        tone: "success",
        title: "Bulk update applied",
        description: "Selected issues were updated together.",
        actionLabel: "Undo",
        onAction: async () => {
          await restoreIssuesSnapshot(result.previousIssues);
          await invalidateOpsQueries(queryClient);
          setToast(null);
        },
      });
      onApplied?.();
    },
    onSettled: () => {
      setPendingIds([]);
    },
  });

  return {
    applyBulk: mutation.mutate,
    isPending: mutation.isPending,
    pendingIds,
  };
}

export function useResetDemoMutation(setToast: (toast: ConsoleToast | null) => void) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: resetDemoData,
    onSuccess: async () => {
      await invalidateOpsQueries(queryClient);
      setToast({
        tone: "success",
        title: "Demo data reset",
        description: "The console is back to its seeded state.",
      });
    },
  });
}
