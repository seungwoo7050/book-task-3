/**
 * 새 책 생성을 위한 DTO.
 * `id`는 서버에서 생성하므로 제외한다.
 */
export class CreateBookDto {
  title!: string;
  author!: string;
  publishedYear!: number;
  genre!: string;
  price!: number;
}
