export interface Book {
  id: string;
  title: string;
  author: string;
  publishedYear: number;
  genre: string;
  price: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface BookRow {
  id: string;
  title: string;
  author: string;
  published_year: number;
  genre: string;
  price: number;
  created_at: string;
  updated_at: string;
}
