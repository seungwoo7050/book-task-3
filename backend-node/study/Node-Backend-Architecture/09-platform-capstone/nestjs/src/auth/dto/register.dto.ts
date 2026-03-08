import { IsString, MinLength, MaxLength, IsOptional, IsEnum } from "class-validator";
import { Role } from "../entities/user.entity";

export class RegisterDto {
  @IsString()
  @MinLength(3)
  @MaxLength(30)
  username!: string;

  @IsString()
  @MinLength(6)
  @MaxLength(100)
  password!: string;

  @IsOptional()
  @IsEnum(Role)
  role?: Role;
}
