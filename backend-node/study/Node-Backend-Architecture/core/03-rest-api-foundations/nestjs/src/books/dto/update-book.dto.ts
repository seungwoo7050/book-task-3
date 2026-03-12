/**
 * 기존 책 수정을 위한 DTO.
 * 모든 필드는 선택 사항이며 전달된 필드만 수정한다.
 */
export class UpdateBookDto {
  title?: string;
  author?: string;
  publishedYear?: number;
  genre?: string;
  price?: number;
}
