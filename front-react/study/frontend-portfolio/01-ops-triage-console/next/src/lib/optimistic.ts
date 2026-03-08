import { type BulkIssuePatch, type Issue, type IssuePatch } from "@/lib/types";

function pushActivity(issue: Issue, message: string, type: Issue["activity"][number]["type"]): Issue {
  const timestamp = new Date().toISOString();

  return {
    ...issue,
    updatedAt: timestamp,
    lastSeenAt: timestamp,
    activity: [
      {
        id: `${issue.id}-${type}-${timestamp}`,
        type,
        actor: "Ops operator",
        message,
        timestamp,
      },
      ...issue.activity,
    ],
  };
}

export function applyIssuePatch(issue: Issue, patch: IssuePatch): Issue {
  let nextIssue = { ...issue };

  if (patch.status && patch.status !== issue.status) {
    nextIssue = pushActivity(
      { ...nextIssue, status: patch.status },
      `Status set to ${patch.status}.`,
      "status_changed",
    );
  }

  if (patch.priority && patch.priority !== issue.priority) {
    nextIssue = pushActivity(
      { ...nextIssue, priority: patch.priority },
      `Priority set to ${patch.priority.toUpperCase()}.`,
      "priority_changed",
    );
  }

  if (
    patch.labels &&
    JSON.stringify(patch.labels.slice().sort()) !==
      JSON.stringify(issue.labels.slice().sort())
  ) {
    nextIssue = pushActivity(
      { ...nextIssue, labels: [...patch.labels] },
      `Labels updated to ${patch.labels.join(", ")}.`,
      "label_changed",
    );
  }

  if (patch.routeTeam && patch.routeTeam !== issue.routeTeam) {
    nextIssue = pushActivity(
      { ...nextIssue, routeTeam: patch.routeTeam },
      `Route team changed to ${patch.routeTeam}.`,
      "route_changed",
    );
  }

  if (patch.operatorNote && patch.operatorNote.trim().length > 0) {
    nextIssue = pushActivity(
      { ...nextIssue, operatorNote: patch.operatorNote.trim() },
      `Operator note updated.`,
      "note_added",
    );
  }

  return nextIssue;
}

export function applyBulkPatch(issues: Issue[], issueIds: string[], patch: BulkIssuePatch): Issue[] {
  return issues.map((issue) => {
    if (!issueIds.includes(issue.id)) {
      return issue;
    }

    return applyIssuePatch(issue, {
      status: patch.status,
      priority: patch.priority,
      routeTeam: patch.routeTeam,
      labels: patch.addLabel
        ? Array.from(new Set([...issue.labels, patch.addLabel]))
        : issue.labels,
    });
  });
}

