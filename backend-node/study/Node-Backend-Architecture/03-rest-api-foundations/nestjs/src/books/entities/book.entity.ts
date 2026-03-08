/**
 * Book entity — defines the data structure for a Book.
 */
export class Book {
  id!: string;
  title!: string;
  author!: string;
  publishedYear!: number;
  genre!: string;
  price!: number;
}
