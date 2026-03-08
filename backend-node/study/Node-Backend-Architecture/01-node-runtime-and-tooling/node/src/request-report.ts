import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import path from "node:path";
import readline from "node:readline";

export type RequestRecord = {
  timestamp: string;
  userId: string;
  route: string;
  status: number;
};

export type RequestSummary = {
  filePath: string;
  totalRequests: number;
  uniqueUsers: number;
  errorCount: number;
  perRoute: Record<string, number>;
};

export async function readRequestLog(filePath: string): Promise<RequestRecord[]> {
  const resolvedPath = path.resolve(filePath);
  await stat(resolvedPath);

  const stream = createReadStream(resolvedPath, { encoding: "utf8" });
  const lineReader = readline.createInterface({
    input: stream,
    crlfDelay: Number.POSITIVE_INFINITY,
  });

  const records: RequestRecord[] = [];
  let lineNumber = 0;

  for await (const line of lineReader) {
    lineNumber += 1;
    if (line.trim().length === 0) {
      continue;
    }

    try {
      records.push(JSON.parse(line) as RequestRecord);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown JSON parsing error";
      throw new Error(`Invalid JSON at line ${lineNumber}: ${message}`);
    }
  }

  return records;
}

export function summarizeRequests(filePath: string, records: RequestRecord[]): RequestSummary {
  const perRoute: Record<string, number> = {};
  const uniqueUsers = new Set<string>();
  let errorCount = 0;

  for (const record of records) {
    uniqueUsers.add(record.userId);
    perRoute[record.route] = (perRoute[record.route] ?? 0) + 1;

    if (record.status >= 400) {
      errorCount += 1;
    }
  }

  return {
    filePath: path.resolve(filePath),
    totalRequests: records.length,
    uniqueUsers: uniqueUsers.size,
    errorCount,
    perRoute,
  };
}

export function formatSummary(summary: RequestSummary, format: "text" | "json"): string {
  if (format === "json") {
    return JSON.stringify(summary, null, 2);
  }

  const routes = Object.entries(summary.perRoute)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([route, count]) => `- ${route}: ${count}`)
    .join("\n");

  return [
    `File: ${summary.filePath}`,
    `Total requests: ${summary.totalRequests}`,
    `Unique users: ${summary.uniqueUsers}`,
    `Error count: ${summary.errorCount}`,
    "Per route:",
    routes,
  ].join("\n");
}
