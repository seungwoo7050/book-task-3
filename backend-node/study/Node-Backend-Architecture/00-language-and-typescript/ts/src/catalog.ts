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

function toSlugPart(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function normalizeTags(tags: string[]): string[] {
  return [...new Set(tags.map(toSlugPart).filter((tag) => tag.length > 0))].sort();
}

export function toNormalizedBook(draft: BookDraft): NormalizedBook {
  const title = draft.title.trim();
  const author = draft.author.trim();
  const slug = `${toSlugPart(draft.title)}-${draft.publishedYear}`;
  const description = draft.description?.trim();
  const summary = description && description.length > 0
    ? description
    : `${author} wrote ${title} in ${draft.publishedYear}.`;

  return {
    slug,
    title,
    author,
    publishedYear: draft.publishedYear,
    tags: normalizeTags(draft.tags),
    summary,
  };
}

export async function fetchInventorySnapshot(
  slugs: string[],
  client: InventoryClient,
): Promise<InventorySnapshot[]> {
  return Promise.all(
    slugs.map(async (slug) => {
      try {
        const inStock = await client.fetchStock(slug);

        return {
          slug,
          inStock,
        };
      } catch (error) {
        return {
          slug,
          inStock: null,
          error: error instanceof Error ? error.message : "Unknown inventory error",
        };
      }
    }),
  );
}

export function formatBookCard(book: NormalizedBook, snapshot?: InventorySnapshot): string {
  const stockLine = snapshot === undefined
    ? "Inventory: not requested"
    : snapshot.error
      ? `Inventory: unavailable (${snapshot.error})`
      : `Inventory: ${snapshot.inStock}`;

  return [
    `${book.title} (${book.publishedYear})`,
    `Author: ${book.author}`,
    `Slug: ${book.slug}`,
    `Tags: ${book.tags.join(", ") || "none"}`,
    `Summary: ${book.summary}`,
    stockLine,
  ].join("\n");
}
