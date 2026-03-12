/**
 * Book entity - Book 데이터 구조를 정의한다.
 */
export class Book {
  id!: string;
  title!: string;
  author!: string;
  publishedYear!: number;
  genre!: string;
  price!: number;
}
