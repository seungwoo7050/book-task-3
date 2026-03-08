/**
 * DTO for updating an existing book.
 * All fields are optional — only provided fields are updated.
 */
export class UpdateBookDto {
  title?: string;
  author?: string;
  publishedYear?: number;
  genre?: string;
  price?: number;
}
