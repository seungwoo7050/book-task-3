export interface PaginationState {
  cursor: number;
  pageSize: number;
  total: number;
}

export function createPaginationState(total: number, pageSize: number): PaginationState {
  return {
    cursor: pageSize,
    pageSize,
    total,
  };
}

export function loadNextPage(state: PaginationState): PaginationState {
  return {
    ...state,
    cursor: Math.min(state.total, state.cursor + state.pageSize),
  };
}

export function isPaginationComplete(state: PaginationState): boolean {
  return state.cursor >= state.total;
}
