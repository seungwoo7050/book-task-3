export type BoardStatus = "open" | "blocked" | "done";
export type BoardSort = "priority-desc" | "priority-asc" | "title-asc";

export interface BoardItem {
  id: string;
  title: string;
  workspace: string;
  owner: string;
  status: BoardStatus;
  priority: number;
}

export interface BoardQuery {
  search: string;
  status: BoardStatus | "all";
  sort: BoardSort;
}

export interface SelectionState {
  selectedId: string | null;
  editingId: string | null;
}

export interface BoardState {
  items: BoardItem[];
  query: BoardQuery;
  selection: SelectionState;
  notice: string;
}

export interface PersistedBoardState {
  items: BoardItem[];
  query: BoardQuery;
  selectedId: string | null;
}
