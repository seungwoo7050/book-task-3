export type BookDraft = {
  title: string;
  author: string;
  publishedYear: number;
  tags: string[];
  description?: string;
};

export type NormalizedBook = {
  slug: string;
  title: string;
  author: string;
  publishedYear: number;
  tags: string[];
  summary: string;
};

export type InventoryClient = {
  fetchStock(slug: string): Promise<number>;
};

export type InventorySnapshot = {
  slug: string;
  inStock: number | null;
  error?: string;
};

export function normalizeTags(_tags: string[]): string[] {
  throw new Error("TODO: implement normalizeTags");
}

export function toNormalizedBook(_draft: BookDraft): NormalizedBook {
  throw new Error("TODO: implement toNormalizedBook");
}

export async function fetchInventorySnapshot(
  _slugs: string[],
  _client: InventoryClient,
): Promise<InventorySnapshot[]> {
  throw new Error("TODO: implement fetchInventorySnapshot");
}

export function formatBookCard(_book: NormalizedBook, _snapshot?: InventorySnapshot): string {
  throw new Error("TODO: implement formatBookCard");
}
