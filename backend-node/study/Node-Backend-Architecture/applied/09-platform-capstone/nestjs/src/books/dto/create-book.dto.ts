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
  @MinLength(1)
  @MaxLength(200)
  title!: string;

  @IsString()
  @MinLength(1)
  @MaxLength(100)
  author!: string;

  @IsInt()
  @Min(1000)
  @Max(2100)
  publishedYear!: number;

  @IsString()
  @MinLength(1)
  @MaxLength(50)
  genre!: string;

  @IsNumber()
  @IsPositive()
  price!: number;
}
