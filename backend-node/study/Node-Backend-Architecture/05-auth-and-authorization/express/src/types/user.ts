export interface User {
  id: string;
  username: string;
  password: string; // hashed
  role: "USER" | "ADMIN";
}

export type CreateUserDto = {
  username: string;
  password: string;
  role?: "USER" | "ADMIN";
};

export type UserResponse = Omit<User, "password">;

export interface JwtPayload {
  sub: string;
  username: string;
  role: string;
}
