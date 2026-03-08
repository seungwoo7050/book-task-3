import { Injectable, Inject, ConflictException, UnauthorizedException } from "@nestjs/common";
import { JwtService } from "@nestjs/jwt";
import { randomUUID } from "crypto";
import * as bcrypt from "bcryptjs";
import { RegisterDto } from "./dto/register.dto";

interface User {
  id: string;
  username: string;
  password: string;
  role: "USER" | "ADMIN";
}

@Injectable()
export class AuthService {
  private readonly users = new Map<string, User>();

  constructor(
    @Inject(JwtService)
    private readonly jwtService: JwtService,
  ) {}

  async register(dto: RegisterDto) {
    const existing = Array.from(this.users.values()).find(
      (u) => u.username === dto.username,
    );
    if (existing) {
      throw new ConflictException("Username already exists");
    }

    const hashed = await bcrypt.hash(dto.password, 10);
    const user: User = {
      id: randomUUID(),
      username: dto.username,
      password: hashed,
      role: dto.role || "USER",
    };

    this.users.set(user.id, user);
    return { id: user.id, username: user.username, role: user.role };
  }

  async login(username: string, password: string) {
    const user = Array.from(this.users.values()).find(
      (u) => u.username === username,
    );
    if (!user) {
      throw new UnauthorizedException("Invalid credentials");
    }

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new UnauthorizedException("Invalid credentials");
    }

    const payload = { sub: user.id, username: user.username, role: user.role };
    const token = this.jwtService.sign(payload);

    return {
      token,
      user: { id: user.id, username: user.username, role: user.role },
    };
  }
}
