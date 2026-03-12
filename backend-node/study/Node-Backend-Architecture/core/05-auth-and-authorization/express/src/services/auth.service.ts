import { randomUUID } from "crypto";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { User, CreateUserDto, UserResponse, JwtPayload } from "../types";

const JWT_SECRET = process.env.JWT_SECRET || "super-secret";
const JWT_EXPIRES_IN = "1h";

/**
 * AuthService - 사용자 등록, 로그인, JWT 처리를 담당한다.
 */
export class AuthService {
  private readonly users = new Map<string, User>();

  async register(dto: CreateUserDto): Promise<UserResponse | null> {
    // 중복 사용자 이름인지 확인한다
    const existing = Array.from(this.users.values()).find(
      (u) => u.username === dto.username
    );
    if (existing) {
      return null; // Username already taken
    }

    const hashedPassword = await bcrypt.hash(dto.password, 10);
    const user: User = {
      id: randomUUID(),
      username: dto.username,
      password: hashedPassword,
      role: dto.role || "USER",
    };

    this.users.set(user.id, user);
    return this.toResponse(user);
  }

  async login(
    username: string,
    password: string
  ): Promise<{ token: string; user: UserResponse } | null> {
    const user = Array.from(this.users.values()).find(
      (u) => u.username === username
    );
    if (!user) {
      return null;
    }

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      return null;
    }

    const payload: JwtPayload = {
      sub: user.id,
      username: user.username,
      role: user.role,
    };

    const token = jwt.sign(payload, JWT_SECRET, { expiresIn: JWT_EXPIRES_IN });
    return { token, user: this.toResponse(user) };
  }

  private toResponse(user: User): UserResponse {
    return { id: user.id, username: user.username, role: user.role };
  }
}
