export class RegisterDto {
  username!: string;
  password!: string;
  role?: "USER" | "ADMIN";
}
