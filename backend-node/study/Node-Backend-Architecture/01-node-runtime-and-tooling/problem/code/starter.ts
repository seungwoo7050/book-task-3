export type RequestRecord = {
  timestamp: string;
  userId: string;
  route: string;
  status: number;
};

export type RequestSummary = {
  totalRequests: number;
  uniqueUsers: number;
  errorCount: number;
  perRoute: Record<string, number>;
};

export async function readRequestLog(_filePath: string): Promise<RequestRecord[]> {
  throw new Error("TODO: implement readRequestLog");
}

export function summarizeRequests(_records: RequestRecord[]): RequestSummary {
  throw new Error("TODO: implement summarizeRequests");
}

export function formatSummary(_summary: RequestSummary, _format: "text" | "json"): string {
  throw new Error("TODO: implement formatSummary");
}
