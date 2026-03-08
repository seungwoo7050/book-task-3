import {
  IsString,
  IsNumber,
  IsInt,
  IsPositive,
  Min,
  Max,
  MinLength,
  MaxLength,
} from "class-validator";

export class CreateBookDto {
  @IsString()
  @MinLength(1, { message: "Title is required" })
  @MaxLength(200)
  title!: string;

  @IsString()
  @MinLength(1, { message: "Author is required" })
  @MaxLength(100)
  author!: string;

  @IsInt({ message: "Published year must be an integer" })
  @Min(1000)
  @Max(2100)
  publishedYear!: number;

  @IsString()
  @MinLength(1, { message: "Genre is required" })
  @MaxLength(50)
  genre!: string;

  @IsNumber({}, { message: "Price must be a number" })
  @IsPositive({ message: "Price must be positive" })
  price!: number;
}
