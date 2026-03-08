export type DirectoryCategory = "all" | "runbook" | "policy" | "guide";
export type AsyncState = "idle" | "loading" | "success" | "empty" | "error";

export interface DirectoryItem {
  id: string;
  title: string;
  category: Exclude<DirectoryCategory, "all">;
  owner: string;
  summary: string;
  body: string;
}

export interface DirectoryQuery {
  search: string;
  category: DirectoryCategory;
}

export interface ExplorerUrlState extends DirectoryQuery {
  item: string | null;
}

export interface ExplorerService {
  listDirectory(
    query: DirectoryQuery & { simulateFailure?: boolean },
    signal: AbortSignal,
  ): Promise<DirectoryItem[]>;
  getDirectoryItem(
    id: string,
    signal: AbortSignal,
  ): Promise<DirectoryItem>;
}
