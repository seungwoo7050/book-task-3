import {
  readIssues,
  resetRuntimeConfig,
  updateRuntimeConfig,
  writeIssues,
} from "@/lib/storage";
import { type DemoRuntimeConfig, type Issue } from "@/lib/types";
import { cloneValue } from "@/lib/utils";

export async function restoreIssuesSnapshot(snapshot: Issue[]): Promise<void> {
  const snapshotMap = new Map(snapshot.map((issue) => [issue.id, cloneValue(issue)]));
  const nextIssues = readIssues().map((issue) => snapshotMap.get(issue.id) ?? issue);
  writeIssues(nextIssues);
}

export function configureDemoRuntime(
  patch: Partial<DemoRuntimeConfig>,
): DemoRuntimeConfig {
  return updateRuntimeConfig(patch);
}

export function resetDemoRuntime(): DemoRuntimeConfig {
  return resetRuntimeConfig();
}
