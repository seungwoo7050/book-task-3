import { ApiProperty } from "@nestjs/swagger";
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
  @ApiProperty({ example: "Clean Architecture" })
  @IsString()
  @MinLength(1)
  @MaxLength(200)
  title!: string;

  @ApiProperty({ example: "Robert C. Martin" })
  @IsString()
  @MinLength(1)
  @MaxLength(100)
  author!: string;

  @ApiProperty({ example: 2017 })
  @IsInt()
  @Min(1000)
  @Max(2100)
  publishedYear!: number;

  @ApiProperty({ example: "Engineering" })
  @IsString()
  @MinLength(1)
  @MaxLength(50)
  genre!: string;

  @ApiProperty({ example: 32.0 })
  @IsNumber()
  @IsPositive()
  price!: number;
}
