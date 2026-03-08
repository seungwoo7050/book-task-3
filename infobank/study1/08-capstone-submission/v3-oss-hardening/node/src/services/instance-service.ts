import type { InstanceSettings } from "@study1-v3/shared";

export function buildDefaultInstanceSettings(updatedBy: string): InstanceSettings {
  return {
    id: "default",
    workspaceName: "Study1 OSS Team",
    defaultLocale: "ko-KR",
    defaultClientVersion: "1.2.0",
    evalMinTop3Recall: 0.9,
    compareMinUplift: 0.02,
    updatedAt: new Date().toISOString(),
    updatedBy
  };
}
