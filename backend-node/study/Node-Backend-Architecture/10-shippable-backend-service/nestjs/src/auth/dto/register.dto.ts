import { ApiProperty, ApiPropertyOptional } from "@nestjs/swagger";
import { IsString, MinLength, MaxLength, IsOptional, IsEnum } from "class-validator";
import { Role } from "../entities/user.entity";

export class RegisterDto {
  @ApiProperty({ example: "reader01" })
  @IsString()
  @MinLength(3)
  @MaxLength(30)
  username!: string;

  @ApiProperty({ example: "password123" })
  @IsString()
  @MinLength(6)
  @MaxLength(100)
  password!: string;

  @ApiPropertyOptional({ enum: Role, enumName: "Role" })
  @IsOptional()
  @IsEnum(Role)
  role?: Role;
}
