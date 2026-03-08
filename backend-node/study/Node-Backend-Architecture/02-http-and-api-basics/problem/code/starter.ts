export type BookRecord = {
  id: string;
  title: string;
  author: string;
  publishedYear: number;
};

export type CreateBookPayload = {
  title: string;
  author: string;
  publishedYear: number;
};

export const ROUTES = {
  health: "/health",
  books: "/books",
  bookById: "/books/:id",
} as const;

export function validateCreateBookPayload(_payload: unknown): CreateBookPayload {
  throw new Error("TODO: implement validateCreateBookPayload");
}
