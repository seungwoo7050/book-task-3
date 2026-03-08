/**
 * DTO for creating a new book.
 * Excludes `id` since it is generated server-side.
 */
export class CreateBookDto {
  title!: string;
  author!: string;
  publishedYear!: number;
  genre!: string;
  price!: number;
}
