export interface Book {
  id: string;
  title: string;
  author: string;
  publishedYear: number;
  genre: string;
  price: number;
}

export type CreateBookDto = Omit<Book, "id">;
export type UpdateBookDto = Partial<CreateBookDto>;
